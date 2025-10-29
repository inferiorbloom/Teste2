import customtkinter as ctk
from tkinter.filedialog import askopenfilename, askopenfilenames
import os
import json
import pandas as pd
from PIL import Image
import winsound
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
#importações necessárias
#_____________________________________________________________________________________________________________________________________________________________________________________
# Configurações iniciais do customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
#_____________________________________________________________________________________________________________________________________________________________________________________
# Carregando ícone
icone_pasta = ctk.CTkImage(light_image=Image.open("imagens/icones/pasta.png"), size=(20, 20))
icone_file = ctk.CTkImage(light_image=Image.open("imagens/icones/file.png"), size=(20, 20))
icone_excel = ctk.CTkImage(light_image=Image.open("imagens/icones/excel.png"), size=(20, 20))
icone_remover = ctk.CTkImage(light_image=Image.open("imagens/icones/remover.png"), size=(20, 20))
icone_padrao = ctk.CTkImage(light_image=Image.open("imagens/icones/padrao.png"), size=(20, 20))
icone_calcular = ctk.CTkImage(light_image=Image.open("imagens/icones/calcular.png"), size=(20, 20))
icone_adicionar = ctk.CTkImage(light_image=Image.open("imagens/icones/adicionar.png"), size=(20, 20))
#_____________________________________________________________________________________________________________________________________________________________________________________
# Variáveis globais
arquivo_padrao = 0
arquivos = ()
padroes = {}
padrao_escolhido = None
path = r'padroes/padroes.json'
if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        padroes = json.load(f)
#_____________________________________________________________________________________________________________________________________________________________________________________
# Para habilitar o botão de calcular apenas quando os arquivos forem selecionados
selecionado_arquivo_padrao = False
selecionado_amostras = False
selecionado_padrao = False
def habilitar_calcular(selecionado_arquivo_padrao, selecionado_amostras, selecionado_padrao):
    if selecionado_arquivo_padrao and selecionado_amostras and selecionado_padrao:
        botao_calcular.configure(state="normal", command=calcular_concentracoes)


#_____________________________________________________________________________________________________________________________________________________________________________________
# Sons de notificação
def som_concluido():
    winsound.MessageBeep(winsound.MB_ICONASTERISK)  # som de "sucesso"

def som_atencao():
    winsound.MessageBeep(winsound.MB_ICONHAND)  # som de "erro/alerta"

#_____________________________________________________________________________________________________________________________________________________________________________________
# Função para salvar padrões no arquivo JSON
def salvar_padroes():
    with open(path, "w", encoding="utf-8") as f:
        json.dump(padroes, f, ensure_ascii=False, indent=4)
    print(padroes)
#_____________________________________________________________________________________________________________________________________________________________________________________
# Função para selecionar arquivo padrão 
def selecionar_arquivo_padrao():
    global selecionado_arquivo_padrao
    global arquivo_padrao
    arquivo_padrao = askopenfilename(title="Selecione o arquivo.txt que deseja utilizar como PADRÃO!", filetypes=[("Arquivos de texto", "*.txt")])
    texto_arquivo_padrao.configure(text=os.path.basename(arquivo_padrao))
    selecionado_arquivo_padrao = True
#_____________________________________________________________________________________________________________________________________________________________________________________
# Função para selecionar arquivos das amostras
def selecionar_arquivos_amostras():
    global arquivos
    global selecionado_amostras
    arquivos = askopenfilenames(title="Selecione os arquivos.txt que deseja utilizar como AMOSTRAS!", filetypes=[("Arquivos de texto", "*.txt")])
    if arquivos:
        ultimo = os.path.basename(arquivos[-1])
        primeiro = os.path.basename(arquivos[0])
        texto_arquivos_amostras.configure(text=f"{primeiro} ... {ultimo}")
    else:
        texto_arquivos_amostras.configure(text="Nenhum arquivo selecionado")
    selecionado_amostras = True
#_____________________________________________________________________________________________________________________________________________________________________________________
# Função para adicionar nomes dos padrões
def adicionar_nomes_padrao():
    global padroes
    nome_padrao = caixa_de_texto.get()
    caixa_de_texto.delete(0, ctk.END)

    if nome_padrao:
        padroes[nome_padrao] = {}
    print(padroes)
    salvar_padroes()
#_____________________________________________________________________________________________________________________________________________________________________________________
# Função para adicionar concentrações dos elementos
def adicionar_concentracoes_elementos():
    lista_elementos = ctk.CTkToplevel(gerenciador)
    lista_elementos.title("Adicionar Concentrações dos Elementos")
    lista_elementos.transient(gerenciador)  # Torna a janela filha da janela principal
    lista_elementos.grab_set()  # Impede interação com a janela principal enquanto esta está aberta

    # Centraliza na tela
    lista_elementos.update_idletasks()
    largura = lista_elementos.winfo_width()
    altura = lista_elementos.winfo_height()
    x = (lista_elementos.winfo_screenwidth() // 2) - (largura // 2)
    y = (lista_elementos.winfo_screenheight() // 2) - (altura // 2)
    lista_elementos.geometry(f"+{x}+{y}")

    # Mantém em primeiro plano
    escreva_elemento = ctk.CTkLabel(lista_elementos, text="Elemento (símbolo):")
    escreva_elemento.grid(column=0, row=0, padx=10, pady=10)
    caixa_elemento = ctk.CTkEntry(lista_elementos, width=120)
    caixa_elemento.grid(column=0, row=1, padx=10, pady=10)
    # Concentração
    escreva_concentracao = ctk.CTkLabel(lista_elementos, text="Concentração (mg/kg):")
    escreva_concentracao.grid(column=1, row=0, padx=10, pady=10)
    caixa_concentracao = ctk.CTkEntry(lista_elementos, width=120)
    caixa_concentracao.grid(column=1, row=1, padx=10, pady=10)

    # Validação das caixas
    def validar_letras(event):
        valor = caixa_elemento.get()
        if not valor.isalpha():
            caixa_elemento.delete(0, "end")
            caixa_elemento.insert(0, ''.join(filter(str.isalpha, valor)))
    # Validação para números e ponto decimal
    def validar_numeros(event):
        valor = caixa_concentracao.get()
        novo_valor = ''.join([c for c in valor if c.isdigit() or c == '.'])
        if valor != novo_valor:
            caixa_concentracao.delete(0, "end")
            caixa_concentracao.insert(0, novo_valor)
    # Liga as validações aos eventos de digitação
    caixa_elemento.bind("<KeyRelease>", validar_letras)
    caixa_concentracao.bind("<KeyRelease>", validar_numeros)
    # Botão para adicionar o elemento e a concentração ao padrão
    def adicionar():
        global padroes
        elemento = caixa_elemento.get().strip()
        caixa_elemento.delete(0, ctk.END)
        try:
            concentracao = float(caixa_concentracao.get().strip())
            caixa_concentracao.delete(0, ctk.END)
            if elemento and concentracao:
                if padroes:
                    ultimo_padrao = list(padroes.keys())[-1]
                    padroes[ultimo_padrao][elemento] = concentracao
                    print(f"Adicionado {elemento}: {concentracao} mg/kg ao padrão {ultimo_padrao}")
                    salvar_padroes()
                else:
                    print("Nenhum padrão adicionado. Adicione um padrão primeiro.")
        except ValueError:
            print("Concentração inválida. Por favor, insira um número.")
        print(padroes)
    # Botão para adicionar
    botao_adicionar = ctk.CTkButton(lista_elementos, text="Adicionar", command=adicionar)
    botao_adicionar.grid(column=0, row=5, columnspan=2, padx=10, pady=10, sticky="ew")
#_____________________________________________________________________________________________________________________________________________________________________________________
# Função para excluir padrão
def excluir_padrao():
    lista_excluir = ctk.CTkToplevel(janela)
    lista_excluir.title("Excluir Padrão")
    escreva_excluir = ctk.CTkLabel(lista_excluir, text="Selecione o padrão que deseja excluir:")
    escreva_excluir.grid(column=0, row=0, padx=10, pady=10)
    lista_padroes = ctk.CTkComboBox(lista_excluir, values=list(padroes.keys()))
    lista_padroes.grid(column=0, row=1, padx=10, pady=10)
    lista_excluir.transient(janela)  # Torna a janela filha da janela principal
    lista_excluir.grab_set()  # Impede interação com a janela principal enquanto esta está aberta

   # Centraliza na tela
    lista_excluir.update_idletasks()
    largura = lista_excluir.winfo_width()
    altura = lista_excluir.winfo_height()
    x = (lista_excluir.winfo_screenwidth() // 2) - (largura // 2)
    y = (lista_excluir.winfo_screenheight() // 2) - (altura // 2)
    lista_excluir.geometry(f"+{x}+{y}")
    lista_excluir.attributes("-topmost", False)

    def confirmar_exclusao():
        padrao_para_excluir = lista_padroes.get()
        
        if padrao_para_excluir in padroes:
            confirm = ctk.CTkToplevel(lista_excluir)
            confirm.transient(lista_excluir)  # Torna a janela filha da janela principal
            som_atencao()
            confirm.grab_set()  # Impede interação com a janela principal enquanto esta está aberta
            confirm.title("Confirmação")
            texto_confirma = ctk.CTkLabel(confirm, text=f'Tem certeza que deseja excluir o padrão "{padrao_para_excluir}"?')
            texto_confirma.grid(column=0, row=0, columnspan=2, padx=20, pady=20)

            def sim():
                global padroes
                del padroes[padrao_para_excluir]
                salvar_padroes()
                print(f"Padrão {padrao_para_excluir} excluído.")
                confirm.destroy()
                lista_excluir.destroy()

            def nao():
                confirm.destroy()

            botao_sim = ctk.CTkButton(confirm, text="Sim", command=sim)
            botao_sim.grid(column=0, row=1, padx=10, pady=10)
            botao_nao = ctk.CTkButton(confirm, text="Não", command=nao)
            botao_nao.grid(column=1, row=1, padx=10, pady=10)

    botao_excluir = ctk.CTkButton(lista_excluir, text="Excluir", command=confirmar_exclusao)
    botao_excluir.grid(column=0, row=2, padx=10, pady=10)
#_____________________________________________________________________________________________________________________________________________________________________________________
# Função para escolher padrão
def escolher_padrao():
    global padrao_escolhido
    lista_escolher = ctk.CTkToplevel(janela)
    lista_escolher.title("Escolher Padrão")
    lista_escolher.transient(janela)  # Torna a janela filha da janela principal
    lista_escolher.grab_set()  # Impede interação com a janela principal enquanto esta está aberta

    # Centraliza na tela
    lista_escolher.update_idletasks()
    largura = lista_escolher.winfo_width()
    altura = lista_escolher.winfo_height()
    x = (lista_escolher.winfo_screenwidth() // 2) - (largura // 2)
    y = (lista_escolher.winfo_screenheight() // 2) - (altura // 2)
    lista_escolher.geometry(f"+{x}+{y}")

    # Mantém em primeiro plano
    lista_escolher.lift()
    lista_escolher.attributes('-topmost', True)

    lista_pd = ctk.CTkComboBox(lista_escolher, values=list(padroes.keys()))
    lista_pd.grid(column=0, row=0, padx=10, pady=10)

    def escolher():
        global padrao_escolhido
        global selecionado_padrao
        padrao_escolhido = lista_pd.get()
        print(f"Padrão escolhido: {padrao_escolhido}")
        selecionado_padrao = True
        habilitar_calcular(selecionado_arquivo_padrao, selecionado_amostras, selecionado_padrao)
        texto_padraoselecionado.configure(text=f"Padrão escolhido: {padrao_escolhido}")
        lista_escolher.destroy()

    botao_escolher = ctk.CTkButton(lista_escolher, text="Escolher", command=escolher)
    botao_escolher.grid(column=0, row=1, padx=10, pady=10)
#_____________________________________________________________________________________________________________________________________________________________________________________
# Janela principal
janela = ctk.CTk(fg_color="#1E1E1E")
janela.title("Cálculo de Concentrações")
janela.attributes("-topmost", False)
largura = 647
altura = 750
x = (janela.winfo_screenwidth() // 2) - (largura // 2)
y = (janela.winfo_screenheight() // 2) - (altura // 2)
janela.geometry(f"{largura}x{altura}+{x}+{y}")

#_____________________________________________________________________________________________________________________________________________________________________________________
# Frame central com margem
frame = ctk.CTkFrame(janela, corner_radius=20)
frame.pack(expand=True, fill="both", padx=40, pady=40)
frame.grid_columnconfigure(0, weight=1, uniform="colunas")
frame.grid_columnconfigure(1, weight=1, uniform="colunas")
frame.grid_rowconfigure(3, weight=1)
#_____________________________________________________________________________________________________________________________________________________________________________________
# Frame de cima dentro do frame central
frame_cima = ctk.CTkFrame(frame, fg_color="transparent", border_color="#56A4D8", border_width=2, corner_radius=20)
frame_cima.grid(row=0, column=0, columnspan=2, stick="ew", padx=10, pady=10)
#_____________________________________________________________________________________________________________________________________________________________________________________
# Título
titulo = ctk.CTkLabel(frame_cima, text="Seleção de Dados", font=("Arial Black", 24))
titulo.grid(row=0, column=0, padx=10, pady=10, sticky="ew", columnspan=2)
# Faz as colunas ocuparem espaço proporcional
frame_cima.grid_columnconfigure(0, weight=1)
frame_cima.grid_columnconfigure(1, weight=1)
#_____________________________________________________________________________________________________________________________________________________________________________________
# Textos à esquerda dentro do frame cima ----------  Seleção de padrão
texto_orientacao = ctk.CTkLabel(frame_cima, text="Selecione Amostra Padrão", font=("Arial Black", 18), wraplength=200)
texto_orientacao.grid(column=0, row=1, padx=10, pady=10, sticky="n")
botao_selecionar_padrao = ctk.CTkButton(frame_cima, text="Selecionar Arquivo", command=selecionar_arquivo_padrao, image=icone_file, compound="left")
botao_selecionar_padrao.grid(column=0, row=2, padx=10, pady=10, sticky="n")
texto_arquivo_padrao = ctk.CTkLabel(frame_cima, text="")
texto_arquivo_padrao.grid(column=0, row=3, padx=10, pady=10)
#_____________________________________________________________________________________________________________________________________________________________________________________
# Textos à direita dentro do frame cima ----------  Seleção de amostras
texto_orientacao2 = ctk.CTkLabel(frame_cima, text="Selecione Dados para Calcular", font=("Arial Black", 18), wraplength=200)
texto_orientacao2.grid(column=1, row=1, padx=10, pady=10, sticky="n")
botao_selecionar_amostras = ctk.CTkButton(frame_cima, text="Selecionar Arquivos", command=selecionar_arquivos_amostras, image=icone_pasta, compound="left")
botao_selecionar_amostras.grid(column=1, row=2, padx=10, pady=10, sticky="n")
texto_arquivos_amostras = ctk.CTkLabel(frame_cima, text="")
texto_arquivos_amostras.grid(column=1, row=3, padx=10, pady=10, sticky="n")

#_____________________________________________________________________________________________________________________________________________________________________________________
# Função para gerenciar padrões
def gerenciar_padroes():
    global caixa_de_texto, gerenciador

    gerenciador = ctk.CTkToplevel(janela)
    gerenciador.title("Gerenciar Padrões")
    gerenciador.transient(janela)  # Torna a janela filha da janela principal
    gerenciador.grab_set()  # Impede interação com a janela principal enquanto esta está aberta
    l = 300
    a = 400
    
   # Centraliza na tela
    gerenciador.update_idletasks()
    largura = gerenciador.winfo_width()
    altura = gerenciador.winfo_height()
    x = (gerenciador.winfo_screenwidth() // 2) - (l // 2)
    y = (gerenciador.winfo_screenheight() // 2) - (a // 2)
    gerenciador.geometry(f"+{x}+{y}")

    # Tela de gerenciar padrões
    texto_orientacao3 = ctk.CTkLabel(gerenciador, text="Adicione Padrões Certificados", font=("Arial Black", 18), wraplength=200)#texto_orientacao3.grid(column=0, row=3, padx=(30,10), pady=10)
    texto_orientacao3.grid(column=0, row=1, padx=10, pady=10)
    caixa_de_texto = ctk.CTkEntry(gerenciador, width=250)
    caixa_de_texto.grid(column=0, row=2, padx=10, pady=10)
    botao_adicionar_nome = ctk.CTkButton(gerenciador, text="Adicionar", command=adicionar_nomes_padrao, image=icone_adicionar, compound="left")
    botao_adicionar_nome.grid(column=0, row=3, padx=10, pady=10)
    espaco = ctk.CTkLabel(gerenciador, text="")
    espaco.grid(column=0, row=4, padx=10, pady=10)
    texto_orientacao6 = ctk.CTkLabel(gerenciador, text="Escreva as Concentrações", font=("Arial Black", 18), wraplength=200)
    texto_orientacao6.grid(column=0, row=5, padx=10, pady=10)
    botao_adicionar_concentracoes = ctk.CTkButton(gerenciador, text="Escrever", command=adicionar_concentracoes_elementos, image=icone_adicionar, compound="left")
    botao_adicionar_concentracoes.grid(column=0, row=6, padx=10, pady=10)
    botao_excluir_padrao = ctk.CTkButton(gerenciador, text="Excluir Padrão", command=excluir_padrao, image=icone_remover, compound="left")
    botao_excluir_padrao.grid(column=0, row=9, padx=7, pady=10)

# Frame de cima dentro do frame central
frame_meio = ctk.CTkFrame(frame, fg_color="transparent", border_color="#D87878", border_width=2, corner_radius=20)
frame_meio.grid(row=2, column=0, columnspan=2, stick="ew", padx=10, pady=10)
#_____________________________________________________________________________________________________________________________________________________________________________________
# Título
titulo = ctk.CTkLabel(frame_meio, text="Controle dos Padrões", font=("Arial Black", 24))
titulo.grid(row=0, column=0, padx=10, pady=10, sticky="ew", columnspan=2)
# Faz as colunas ocuparem espaço proporcional
frame_meio.grid_columnconfigure(0, weight=1)
frame_meio.grid_columnconfigure(1, weight=1)
#_____________________________________________________________________________________________________________________________________________________________________________________
# Textos à esquerda dentro do frame meio ----------  Gerenciar padrões
texto_orientacao7 = ctk.CTkLabel(frame_meio, text="Adicione e Remova Padrões", font=("Arial Black", 18), wraplength=200)
texto_orientacao7.grid(column=0, row=1, padx=40, pady=10, columnspan=1, sticky="n")
botao_gerenciar_padrao = ctk.CTkButton(frame_meio, text="Gerenciar Padrões", command=gerenciar_padroes)
botao_gerenciar_padrao.grid(column=0, row=2, padx=40, pady=10, sticky="n")
#_____________________________________________________________________________________________________________________________________________________________________________________
# Textos à direita dentro do frame meio ----------  Escolha de padrão
texto_orientacao4 = ctk.CTkLabel(frame_meio, text="Utilizar o Padrão de:", font=("Arial Black", 18), wraplength=200)
texto_orientacao4.grid(column=1, row=1, padx=40, pady=10, sticky="n")
botao_escolher_padrao = ctk.CTkButton(frame_meio, text="Escolher Padrão", command=escolher_padrao, image=icone_padrao, compound="left")
botao_escolher_padrao.grid(column=1, row=2, padx=40, pady=10, sticky="n")
texto_padraoselecionado = ctk.CTkLabel(frame_meio, text="Padrão escolhido: Nenhum")
texto_padraoselecionado.grid(column=1, row=3, padx=40, pady=10, sticky="n")
#_____________________________________________________________________________________________________________________________________________________________________________________
# Dicionário dos elementos químicos
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
#_____________________________________________________________________________________________________________________________________________________________________________________
# Função para habilitar o botão de exportar
def habilitar_exportar():
    botao_exportar.configure(state="normal", command=exportar_para_excel)

#_____________________________________________________________________________________________________________________________________________________________________________________
# Função para calcular as concentrações
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


#_____________________________________________________________________________________________________________________________________________________________________________________
# Normalização
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


#_____________________________________________________________________________________________________________________________________________________________________________________
    # Cálculo das concentrações
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

#_____________________________________________________________________________________________________________________________________________________________________________________
# Funções para os botões do frame inferior esquerdo
# Mostrar previwew dos gráficos de pizza



from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def config_graficos():
    config_graficos = ctk.CTkToplevel(janela)
    config_graficos.title("Configurar Gráficos")
    config_graficos.transient(janela)
    config_graficos.grab_set()

    # Centraliza na tela
    largura, altura = 1000, 800
    x = (config_graficos.winfo_screenwidth() // 2) - (largura // 2)
    y = (config_graficos.winfo_screenheight() // 2) - (altura // 2)
    config_graficos.geometry(f"{largura}x{altura}+{x}+{y}")

    # --- seleção da amostra ---
    selecione_amostra = ctk.CTkComboBox(
        config_graficos,
        values=[os.path.basename(arquivo).replace(".txt", "") for arquivo in arquivos]
    )
    selecione_amostra.grid(column=0, row=0, padx=10, pady=10)

    # --- slider ---
    slider_valor = ctk.CTkSlider(config_graficos, from_=1, to=20, number_of_steps=19)
    slider_valor.set(5)  # valor inicial
    slider_valor.grid(column=1, row=0, padx=10, pady=10, sticky="ew")

    label_slider = ctk.CTkLabel(config_graficos, text="Traço: 5%")
    label_slider.grid(column=2, row=0, padx=10, pady=10)

    # --- frame para os gráficos ---
    frame_graficos = ctk.CTkFrame(config_graficos)
    frame_graficos.grid(column=0, row=1, columnspan=3, padx=10, pady=10, sticky="nsew")
    frame_graficos.grid_rowconfigure(0, weight=1)
    frame_graficos.grid_columnconfigure((0,1), weight=1)

    canvas_maioritario = None
    canvas_traco = None

    def atualizar_graficos(*args):
        nonlocal canvas_maioritario, canvas_traco
        amostra_selecionada = selecione_amostra.get()
        if not amostra_selecionada:
            return

        # --- busca a concentração ---
        concs = None
        for dados in concentracoes.values():
            if amostra_selecionada in dados:
                concs = dados[amostra_selecionada]
                break
        if concs is None:
            return

        elementos = list(concs.keys())
        valores = list(concs.values())

        # --- define limite do traço ---
        percentual = slider_valor.get()
        label_slider.configure(text=f"Traço: {percentual:.0f}%")
        soma_total = sum(valores)
        limite_traco = soma_total * (percentual / 100)

        # separa elementos maiores e traços
        elementos_traco = []
        valores_traco = []
        elementos_majoritarios = []
        valores_majoritarios = []

        soma_traco = 0
        for e, v in sorted(zip(elementos, valores), key=lambda x: x[1]):
            if soma_traco + v <= limite_traco:
                elementos_traco.append(e)
                valores_traco.append(v)
                soma_traco += v
            else:
                elementos_majoritarios.append(e)
                valores_majoritarios.append(v)

        # --- gráfico majoritário ---
        if canvas_maioritario:
            canvas_maioritario.get_tk_widget().destroy()
        fig1, ax1 = plt.subplots(figsize=(4, 4))

        ax1.pie(valores_majoritarios + [soma_traco],
                labels=elementos_majoritarios + ["Traço"],
                autopct='%1.1f%%', startangle=140)
        ax1.set_title(f"Gráfico Majoritário - {amostra_selecionada}")
        canvas_maioritario = FigureCanvasTkAgg(fig1, master=frame_graficos)
        canvas_maioritario.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        # --- gráfico traço ---
        if canvas_traco:
            canvas_traco.get_tk_widget().destroy()
        fig2, ax2 = plt.subplots(figsize=(4, 4))
        if valores_traco:
            ax2.pie(valores_traco, labels=elementos_traco, autopct='%1.1f%%', startangle=140)
        ax2.set_title(f"Gráfico Traço - até {percentual:.0f}%")
        canvas_traco = FigureCanvasTkAgg(fig2, master=frame_graficos)
        canvas_traco.get_tk_widget().grid(row=0, column=1, sticky="nsew")

    # botao para mostrar
    botao_mostrar_grafico = ctk.CTkButton(config_graficos, text="Mostrar Gráficos", command=atualizar_graficos)
    botao_mostrar_grafico.grid(column=0, row=2, padx=10, pady=10)

    # vincula slider
    slider_valor.configure(command=lambda val: atualizar_graficos())

 



#_____________________________________________________________________________________________________________________________________________________________________________________
#frame inferior esquerdo dentro do frame central
frame_inferior_esquerda = ctk.CTkScrollableFrame(frame, fg_color="transparent", border_color="#DFD36B", border_width=2, corner_radius=20)
frame_inferior_esquerda.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
# Título
#titulo = ctk.CTkLabel(frame_inferior_esquerda, text="Opções Extras", font=("Arial Black", 18))
#titulo.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
# Faz as colunas ocuparem espaço proporcional
frame_inferior_esquerda.grid_columnconfigure(0, weight=1)

#Coisas dentro do frame inferior esquerdo
botao_config_graficos = ctk.CTkButton(frame_inferior_esquerda, text="Configurar Gráficos", command=config_graficos)
botao_config_graficos.grid(column=0, row=1, padx=10, pady=10)


#_____________________________________________________________________________________________________________________________________________________________________________________
# Frame inferior dentro do frame central
frame_inferior_direita = ctk.CTkFrame(frame, fg_color="transparent", border_color="#78D890", border_width=2, corner_radius=20)
frame_inferior_direita.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")
# Título
titulo = ctk.CTkLabel(frame_inferior_direita, text="Calcular e Exportar", font=("Arial Black", 18))
titulo.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
# Faz as colunas ocuparem espaço proporcional
frame_inferior_direita.grid_columnconfigure(0, weight=1)
#botão dentro do frame inferior direito
botao_calcular = ctk.CTkButton(frame_inferior_direita, text="Calcular Concentrações", state="disabled", command=calcular_concentracoes, image=icone_calcular, compound="left")
botao_calcular.grid(column=0, row=1, padx=10, pady=10)

#_____________________________________________________________________________________________________________________________________________________________________________________
# Função para exportar para Excel
def exportar_para_excel():
    global arquivos, concentracoes

    # --- Exportação dos dados originais (sem mudar nada) ---
    todos_dados = []
    for arquivo in arquivos:
        nome_amostra = os.path.basename(arquivo).replace(".txt", "")
        todos_dados.append([nome_amostra, "", "", "", ""])
        todos_dados.append(["Elemento", "Z", "Energia", "Área", "Erro"])
        with open(arquivo, "r", encoding="utf-8") as f:
            linhas = f.readlines()[5:]
            for linha in linhas:
                valores = [v.strip() for v in linha.split(",")]
                if len(valores) > 1:
                    try:
                        z = valores[0]
                        nome_elemento = elementos.get(int(z), "")
                    except:
                        nome_elemento = ""
                    dados_sem_ultima = valores[:-1]
                    linha_export = [nome_elemento] + dados_sem_ultima
                    todos_dados.append(linha_export)
        todos_dados.append(["", "", "", "", ""])

    df_dados = pd.DataFrame(todos_dados, columns=["Elemento", "Z", "Energia", "Área", "Erro"])

    # --- Exportação da análise (concentrações já calculadas) ---
    # Agora só usa o dicionário `concentracoes` que já foi gerado antes
    analise = {}
    for chave, dados in concentracoes.items():
        for amostra, valores in dados.items():
            analise[amostra] = valores

    elementos_encontrados = sorted({el for amostra in analise.values() for el in amostra.keys()})
    df_analise = pd.DataFrame([
        [analise[amostra].get(el, "") for el in elementos_encontrados]
        for amostra in analise.keys()
    ], index=list(analise.keys()), columns=elementos_encontrados)

    # Exporta para Excel com duas abas
    with pd.ExcelWriter("amostras.xlsx") as writer:
        df_dados.to_excel(writer, sheet_name="Dados", index=False)
        df_analise.to_excel(writer, sheet_name="Análise", index=True)

    # Pop-up de confirmação
    exportado = ctk.CTkToplevel()
    exportado.title("Exportação Concluída")
    texto_exportado = ctk.CTkLabel(
        exportado,
        text="Arquivo exportado com sucesso como 'amostras.xlsx'! 50 Reais por exportação.",
        font=("Arial Black", 16), wraplength=400
    )
    exportado.transient(janela)  # Torna a janela filha da janela principal
    exportado.grab_set()  # Impede interação com a janela principal enquanto esta está aberta
    texto_exportado.pack(padx=20, pady=20)
    exportado.update_idletasks()
    largura = exportado.winfo_width()
    altura = exportado.winfo_height()
    x = (exportado.winfo_screenwidth() // 2) - (largura // 2)
    y = (exportado.winfo_screenheight() // 2) - (altura // 2)
    exportado.geometry(f"+{x}+{y}")
    som_concluido()

    print("Exportação concluída!")

#_____________________________________________________________________________________________________________________________________________________________________________________
# Botão de exportar dentro do frame inferior direito
botao_exportar = ctk.CTkButton(frame_inferior_direita, text="Exportar para Excel", state="disabled", command=exportar_para_excel, image=icone_excel, compound="left")
botao_exportar.grid(column=0, row=2, padx=10, pady=10)

janela.mainloop()
