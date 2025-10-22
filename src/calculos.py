import os
import pandas as pd
from padroes import padroes, arquivos
from ui_config import botao_exportar
from exportar import exportar_para_excel

elementos = {
    12: "Mg", 13: "Al", 14: "Si", 15: "P", 16: "S", 17: "Cl", 18: "Ar",
    19: "K", 20: "Ca", 21: "Sc", 22: "Ti", 23: "V", 24: "Cr", 25: "Mn",
    26: "Fe", 27: "Co", 28: "Ni", 29: "Cu", 30: "Zn", 31: "Ga", 32: "Ge",
    33: "As", 34: "Se", 35: "Br", 36: "Kr", 37: "Rb", 38: "Sr", 39: "Y",
    40: "Zr", 41: "Nb", 42: "Mo", 43: "Tc", 44: "Ru", 45: "Rh", 46: "Pd",
    47: "Ag", 48: "Cd", 49: "In", 50: "Sn", 51: "Sb", 52: "Te", 53: "I",
    54: "Xe", 55: "Cs", 56: "Ba", 57: "La", 58: "Ce", 59: "Pr", 60: "Nd",
    61: "Pm", 62: "Sm", 63: "Eu", 64: "Gd", 65: "Tb", 66: "Dy", 67: "Ho",
    68: "Er", 69: "Tm", 70: "Yb", 71: "Lu", 72: "Hf", 73: "Ta", 74: "W",
    75: "Re", 76: "Os", 77: "Ir", 78: "Pt", 79: "Au", 80: "Hg", 81: "Tl",
    82: "Pb", 83: "Bi", 84: "Po", 85: "At", 86: "Rn", 87: "Fr", 88: "Ra",
    89: "Ac", 90: "Th", 91: "Pa", 92: "U", 93: "Np", 94: "Pu"
}

def habilitar_exportar():
    botao_exportar.configure(state="normal", command=exportar_para_excel)

def calcular_concentracoes():
    global padrao_escolhido, arquivos, arquivo_padrao, padroes, concentracoes

    if not padrao_escolhido:
        print("Nenhum padrão escolhido!")
        return

    c_padrao = padroes.get(padrao_escolhido, {})
    area_padrao = {}
    documentos = {}
    concentracoes = {}

    for i, arquivo in enumerate(arquivos, start=1):
        documentos[f"documento{i}"] = {"caminho": arquivo}
        nome_amostra = os.path.basename(arquivo).replace(".txt", "")
        concentracoes[f"concentracao{i}"] = {nome_amostra: {}}

    for doc in documentos.values():
        with open(doc["caminho"], "r", encoding="utf-8") as f:
            conteudo = f.readlines()[5:]
        doc["linhas"] = [ [float(x.strip()) for x in linha.split(",")] for linha in conteudo ]

        # Lê área do padrão
    with open(arquivo_padrao, "r", encoding="utf-8") as p:
        for line in p:
            line = line.strip()
            if line and line[0].isdigit():
                valores = [v.strip() for v in line.split(",")]
                try:
                    z = int(valores[0])
                    area = float(valores[2])
                    elemento = elementos.get(z, "-")
                    area_padrao[elemento] = area
                except:
                    continue
    #Normalizacao
    area_ar_padrao = area_padrao.get("Ar", None)
    fatores_normalizacao = {}
    for i, (doc_nome, info) in enumerate(documentos.items(), start=1):
        nome_amostra = list(concentracoes[f"concentracao{i}"].keys())[0]
        area_ar_amostra = None
        for linha in info["linhas"]:
            if int(linha[0]) == 18:  # Z do Ar
                area_ar_amostra = linha[2]
                break
        if area_ar_amostra and area_ar_padrao:
            fatores_normalizacao[nome_amostra] = area_ar_padrao / area_ar_amostra

    for i, (doc_nome, info) in enumerate(documentos.items(), start=1):
        nome_amostra = list(concentracoes[f"concentracao{i}"].keys())[0]
        fator = fatores_normalizacao.get(nome_amostra, 1)  # usa 1 se não houver fator (sem normalização)
        for linha in info["linhas"]:
            num = int(linha[0])
            area_net = linha[2]
            elemento = elementos.get(num)

            # Aplica normalização na área antes do cálculo
            area_net_normalizada = area_net * fator

            if elemento in c_padrao and elemento in area_padrao:
                conc = (area_net_normalizada * c_padrao[elemento]) / area_padrao[elemento]
                concentracoes[f"concentracao{i}"][nome_amostra][elemento] = conc

for chave, dados in concentracoes.items():
    print(f"--- {chave} ---")
    for amostra, valores in dados.items():
        print(f"{amostra}: {valores}")
habilitar_exportar()

