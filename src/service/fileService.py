import os
import customtkinter as ctk
from tkinter.filedialog import askopenfilename, askopenfilenames
from tkinter import filedialog
import math
import pdfplumber
import re
from collections import defaultdict


class Service:
    def __init__(self, master):
        super().__init__()
        self.master = master

        self.pasta_txt = r"aquisicoes"
        self.pasta_pdf = r"reports"

    # Função para selecionar arquivo padrão
    def selecionar_arquivo_padrao(self):
        arquivo_padrao = askopenfilename(
            initialdir=self.pasta_txt,
            title="Selecione o arquivo.txt que deseja utilizar como PADRÃO!",
            filetypes=[("Arquivos de texto", "*.txt")],
        )
        texto_arquivo_padrao = ctk.CTkLabel(self.master, text="")
        texto_arquivo_padrao.configure(text=os.path.basename(arquivo_padrao))
        # arquivo = os.path.basename(arquivo_padrao)
        return arquivo_padrao

    # Função para selecionar arquivos das amostras
    def selecionar_arquivos_amostras(self):
        arquivos_amostras = askopenfilenames(
            initialdir=self.pasta_txt,
            title="Selecione os arquivos.txt que deseja utilizar como AMOSTRAS!",
            filetypes=[("Arquivos de texto", "*.txt")],
        )
        texto_arquivos_amostras = ctk.CTkLabel(self.master, text="")
        if arquivos_amostras:
            ultimo = os.path.basename(arquivos_amostras[-1])
            primeiro = os.path.basename(arquivos_amostras[0])
            texto_arquivos_amostras.configure(text=f"{primeiro} ... {ultimo}")
        else:
            texto_arquivos_amostras.configure(text="Nenhum arquivo selecionado")
        return arquivos_amostras

    def selecionar_arquivos_fullReport(self):
        # Abrir diálogo para selecionar o arquivo PDF do FullReport - tem que colocar em um botão para isso, mas por enquanto é só pra testar a função de extração dos backgrounds e cálculo do limite de detecção
        fullreport = filedialog.askopenfilename(
            initialdir=self.pasta_pdf,
            title="Selecione o FullReport",
            filetypes=[("FullReports", "*.pdf")]
            )

        # Função para extrair os valores de background do PDF do FullReport - Incluindo média dos backgrounds quando houver mais de um valor para o mesmo elemento
        with pdfplumber.open(fullreport) as pdf:
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
