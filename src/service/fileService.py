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

        fullreports = filedialog.askopenfilenames(
            title="Selecione os FullReports",
            filetypes=[("FullReports", "*.pdf")]
        )

        resultados = {}

        for caminho_pdf in fullreports:

            with pdfplumber.open(caminho_pdf) as pdf:
                texto = ""
                for pagina in pdf.pages:
                    texto += pagina.extract_text() + "\n"

            linhas = texto.splitlines()

            backgrounds_raw = defaultdict(lambda: {"K": [], "L": []})

            elemento_atual = None
            camada_atual = None

            for i, linha in enumerate(linhas):

                m_elem = re.match(r"\s*\d+\s*([A-Z][a-z]?)\s+(K|L)\b", linha)
                if m_elem:
                    elemento_atual = m_elem.group(1)
                    camada_atual = m_elem.group(2)
                    continue

                if elemento_atual and camada_atual == "K":
                    if re.match(r"\s*KA[12]\b(?!\s*Escape)", linha):
                        if i + 1 < len(linhas):
                            prox = linhas[i + 1]
                            m_bg = re.search(r"\d+\.\d+\d+\.\d+\s+(\d+)\b", prox)
                            if m_bg:
                                bg = int(m_bg.group(1))
                                backgrounds_raw[elemento_atual]["K"].append(bg)

                if elemento_atual and camada_atual == "L":
                    m_area = re.search(r"(\d+)\s*±", linha)
                    if m_area and i + 1 < len(linhas):
                        prox = linhas[i + 1]
                        m_bg = re.search(r"\d+\.\d+\d+\.\d+\s+(\d+)\b", prox)
                        if m_bg:
                            area = int(m_area.group(1))
                            bg = int(m_bg.group(1))
                            backgrounds_raw[elemento_atual]["L"].append((area, bg))

            backgrounds = {}

            for elemento, dados in backgrounds_raw.items():

                if dados["K"]:
                    if len(dados["K"]) == 1:
                        backgrounds[elemento] = dados["K"][0]
                    else:
                        backgrounds[elemento] = round(sum(dados["K"]) / len(dados["K"]))

                elif dados["L"]:
                    dados_L_ordenados = sorted(dados["L"], key=lambda x: x[0], reverse=True)

                    if len(dados_L_ordenados) >= 2:
                        bg1 = dados_L_ordenados[0][1]
                        bg2 = dados_L_ordenados[1][1]
                        backgrounds[elemento] = round((bg1 + bg2) / 2)
                    else:
                        backgrounds[elemento] = dados_L_ordenados[0][1]

            resultados[caminho_pdf] = backgrounds
        #print("Resultados dos FullReports:")
        #print(resultados)
        #print("=================================")

        return resultados