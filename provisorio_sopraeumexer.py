from tkinter import filedialog
from collections import defaultdict
import pdfplumber
import re
import math
import os


# ======================================================
# Selecionar vários FullReports
# ======================================================
fullreports = filedialog.askopenfilenames(
    title="Selecione os FullReports",
    filetypes=[("FullReports", "*.pdf")]
)


# ======================================================
# Extrair backgrounds respeitando K e L
# ======================================================
def selecionar_arquivos_fullReport(caminho_pdf):

    with pdfplumber.open(caminho_pdf) as pdf:
        texto = ""
        for pagina in pdf.pages:
            texto += pagina.extract_text() + "\n"

    linhas = texto.splitlines()

    backgrounds_raw = defaultdict(lambda: {"K": [], "L": []})

    elemento_atual = None
    camada_atual = None

    for i, linha in enumerate(linhas):

        # ----------------------------------------------
        # Início de elemento (ex: 12Ni K ou 56Ba L)
        # ----------------------------------------------
        m_elem = re.match(r"\s*\d+\s*([A-Z][a-z]?)\s+(K|L)\b", linha)
        if m_elem:
            elemento_atual = m_elem.group(1)
            camada_atual = m_elem.group(2)
            continue

        # ----------------------------------------------
        # Camada K → KA1 / KA2 (exceto Escape)
        # ----------------------------------------------
        if elemento_atual and camada_atual == "K":
            if re.match(r"\s*KA[12]\b(?!\s*Escape)", linha):
                if i + 1 < len(linhas):
                    prox = linhas[i + 1]
                    m_bg = re.search(r"\d+\.\d+\d+\.\d+\s+(\d+)\b", prox)
                    if m_bg:
                        bg = int(m_bg.group(1))
                        backgrounds_raw[elemento_atual]["K"].append(bg)

        # ----------------------------------------------
        # Camada L → guardar (área, background)
        # ----------------------------------------------
        if elemento_atual and camada_atual == "L":
            m_area = re.search(r"(\d+)\s*±", linha)
            if m_area and i + 1 < len(linhas):
                prox = linhas[i + 1]
                m_bg = re.search(r"\d+\.\d+\d+\.\d+\s+(\d+)\b", prox)
                if m_bg:
                    area = int(m_area.group(1))
                    bg = int(m_bg.group(1))
                    backgrounds_raw[elemento_atual]["L"].append((area, bg))

    # ======================================================
    # Decisão final por elemento
    # ======================================================
    backgrounds = {}

    for elemento, dados in backgrounds_raw.items():

        # Prioridade: camada K
        if dados["K"]:
            if len(dados["K"]) == 1:
                backgrounds[elemento] = dados["K"][0]
            else:
                backgrounds[elemento] = round(sum(dados["K"]) / len(dados["K"]))

        # Caso não tenha K, usa L
        elif dados["L"]:
            dados_L_ordenados = sorted(dados["L"], key=lambda x: x[0], reverse=True)

            if len(dados_L_ordenados) >= 2:
                bg1 = dados_L_ordenados[0][1]
                bg2 = dados_L_ordenados[1][1]
                backgrounds[elemento] = round((bg1 + bg2) / 2)
            else:
                backgrounds[elemento] = dados_L_ordenados[0][1]
    print(backgrounds)
    return backgrounds


# ======================================================
# Limite de detecção
# ======================================================
def calcular_limite_deteccao(backgrounds):

    limites_area = {}

    for elemento, bg in backgrounds.items():
        limites_area[elemento] = round(3 * math.sqrt(bg))

    return limites_area


# ======================================================
# Execução
# ======================================================
for arquivo in fullreports:

    backgrounds = selecionar_arquivos_fullReport(arquivo)
    limites_area = calcular_limite_deteccao(backgrounds)

    nome_arquivo = os.path.basename(arquivo)

    resultado = ", ".join(
        [f"{elemento}: {ld}" for elemento, ld in limites_area.items()]
    )

    print(f"{nome_arquivo}: {resultado}")