"""
Modulos de carregamento de arquivos e bibliotecas
"""
import os
import json
from tkinter.filedialog import askopenfilename, askopenfilenames
import customtkinter as ctk
from ui_config import texto_arquivo_padrao, texto_arquivos_amostras, texto_padraoselecionado, botao_calcular, janela, icone_adicionar, icone_remover
from utils import som_atencao
from calculos import calcular_concentracoes

arquivo_padrao = 0
path = "padroes/padroes.json"
padroes = {}
padrao_escolhido = None
if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        padroes = json.load(f)
arquivos = ()

# Para habilitar o botão de calcular apenas quando os arquivos forem selecionados
selecionado_arquivo_padrao = False
selecionado_amostras = False
selecionado_padrao = False
def habilitar_calcular(selecionado_arquivo_padrao, selecionado_amostras, selecionado_padrao):
    if selecionado_arquivo_padrao and selecionado_amostras and selecionado_padrao:
        botao_calcular.configure(state="normal", command=calcular_concentracoes)

def salvar_padroes():
    with open(path, "w", encoding="utf-8") as f:
        json.dump(padroes, f, ensure_ascii=False, indent=4)
    print(padroes)

def selecionar_arquivo_padrao():
    global selecionado_arquivo_padrao
    global arquivo_padrao
    arquivo_padrao = askopenfilename(title="Selecione o arquivo.txt que deseja utilizar como PADRÃO!", filetypes=[("Arquivos de texto", "*.txt")])
    texto_arquivo_padrao.configure(text=os.path.basename(arquivo_padrao))
    selecionado_arquivo_padrao = True

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

def adicionar_nomes_padrao():
    global padroes
    nome_padrao = caixa_de_texto.get()
    caixa_de_texto.delete(0, ctk.END)

    if nome_padrao:
        padroes[nome_padrao] = {}
    print(padroes)
    salvar_padroes()

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
