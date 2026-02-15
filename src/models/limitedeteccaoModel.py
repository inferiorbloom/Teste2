from tkinter import filedialog
import math

# Abrir diálogo para selecionar o arquivo PDF do FullReport - tem que colocar em um botão para isso, mas por enquanto é só pra testar a função de extração dos backgrounds e cálculo do limite de detecção
fullreport = filedialog.askopenfilename(
    title="Selecione o FullReport",
    filetypes=[("FullReports", "*.pdf")]
)

# Função para extrair os valores de background do PDF do FullReport - Incluindo média dos backgrounds quando houver mais de um valor para o mesmo elemento
def extrair_backgrounds_pdf(caminho_pdf):
    import pdfplumber
    import re
    from collections import defaultdict

    with pdfplumber.open(caminho_pdf) as pdf:
        texto = ""
        for pagina in pdf.pages:
            texto += pagina.extract_text() + "\n"

    linhas = texto.splitlines()

    backgrounds_raw = defaultdict(list)
    elemento_atual = None

    for i, linha in enumerate(linhas):

        # início de elemento (ex: 12Ni K)
        m_elem = re.match(r"\s*\d+\s*([A-Z][a-z]?)\s*K\b", linha)
        if m_elem:
            elemento_atual = m_elem.group(1)
            continue

        # KA1 ou KA2 (mas NÃO Escape)
        if elemento_atual and re.match(r"\s*KA[12]\b(?!\s*Escape)", linha):

            if i + 1 < len(linhas):
                prox = linhas[i + 1]

                m_bg = re.search(r"\d+\.\d+\d+\.\d+\s+(\d+)\b", prox)
                if m_bg:
                    bg = int(m_bg.group(1))
                    backgrounds_raw[elemento_atual].append(bg)

    backgrounds = {}
    for elemento, valores in backgrounds_raw.items():
        if len(valores) == 1:
            backgrounds[elemento] = valores[0]
        else:
            backgrounds[elemento] = round(sum(valores) / len(valores))

    return backgrounds

# só pra colocar em um dicionário
backgrounds = extrair_backgrounds_pdf(fullreport)
#print(backgrounds)

#função de calcular limite, ainda falta coisa
def calcular_limite_deteccao(backgrounds):
    limites_area = {}

    for elemento, bg in backgrounds.items():
        limites_area[elemento] = round(3 * math.sqrt(bg))

    return limites_area

limite_deteccao = calcular_limite_deteccao(backgrounds)
print(limite_deteccao)

