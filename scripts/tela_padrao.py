from tkinter import *
from tkinter.filedialog import askopenfilename, askopenfilenames
import os
import json
#________________________________________________________________________________________________________________________________________________________________
# Variável global para armazenar o caminho do arquivo padrão
arquivo_padrao = 0
arquivos = ()
padroes = {}
path = r'padroes/padroes.json'
if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        padroes = json.load(f)
#função para salvar padrões
def salvar_padroes():
    with open(path, "w", encoding="utf-8") as f:
        json.dump(padroes, f, ensure_ascii=False, indent=4)
print(padroes)  # Apenas para verificar se está funcionando
#________________________________________________________________________________________________________________________________________________________________
# Função para selecionar o arquivo padrão
def selecionar_arquivo_padrao():
    # Função para selecionar o arquivo padrão
    arquivo_padrao = askopenfilename(title="Selecione o arquivo.txt que deseja utilizar como PADRÃO!", filetypes=[("Arquivos de texto", "*.txt")])
    #editar texto na janela
    texto_arquivo_padrao["text"] = os.path.basename(arquivo_padrao)
#________________________________________________________________________________________________________________________________________________________________
#função para selecionar os arquivos das amostras
def selecionar_arquivos_amostras():
    arquivos = askopenfilenames(title="Selecione os arquivos.txt que deseja utilizar como AMOSTRAS!", filetypes=[("Arquivos de texto", "*.txt")])
    #editar texto na janela
    ultimo = os.path.basename(arquivos[-1])
    primeiro = os.path.basename(arquivos[0])
    texto_arquivos_amostras["text"] = f"{primeiro} ... {ultimo}"
#________________________________________________________________________________________________________________________________________________________________
# Adicionar padrões certificados e secundários
def adicionar_nomes_padrao():
    # Função para adicionar novas concentrações padrão
    nome_padrao = caixa_de_texto.get()
    if nome_padrao:
        padroes[nome_padrao] = {}
    print(padroes)  # Apenas para verificar se está funcionando

    pass


def adicionar_concentracoes_elementos():
    # Função para adicionar concentrações dos elementos ao padrão selecionado
    lista_elementos = Tk()

    # Aqui você pode adicionar widgets para inserir os elementos e suas concentrações
    # Por exemplo, uma Entry para o elemento e outra para a concentração, e um botão para adicionar
    # Exemplo simples:
    escreva_elemento = Label(lista_elementos, text="Elemento (símbolo):")
    escreva_elemento.grid(column=0, row=0, padx=10, pady=10)
    #validação para aceitar apenas letras
    conferindo_letras = (lista_elementos.register(lambda P: P.isalpha() or P == ""), "%P")
    caixa_elemento = Entry(lista_elementos, width=20, validate="key", validatecommand=conferindo_letras)
    caixa_elemento.grid(column=0, row=1, padx=10, pady=10)
    #escrevendo valor de concentração
    escreva_concentracao = Label(lista_elementos, text="Concentração (mg/kg):")
    escreva_concentracao.grid(column=1, row=0, padx=10, pady=10)
    #validação para aceitar apenas números
    conferindo_numeros = (lista_elementos.register(lambda P: P.replace('.','',1).isdigit() or P == ""), "%P")
    caixa_concentracao = Entry(lista_elementos, width=20, validate="key", validatecommand=conferindo_numeros)  
    caixa_concentracao.grid(column=1, row=1, padx=10, pady=10)

#função adicionar elemento e concentração e salvar
    def adicionar():
        elemento = caixa_elemento.get().strip()
        try:
            concentracao = float(caixa_concentracao.get().strip())
            if elemento and concentracao:
                # Adiciona ao último padrão adicionado
                if padroes:
                    ultimo_padrao = list(padroes.keys())[-1]
                    padroes[ultimo_padrao][elemento] = concentracao
                    print(f"Adicionado {elemento}: {concentracao} mg/kg ao padrão {ultimo_padrao}")
                    salvar_padroes() #salva após adicionar
                else:
                    print("Nenhum padrão adicionado. Adicione um padrão primeiro.")
        except ValueError:
            print("Concentração inválida. Por favor, insira um número.")
        print(padroes)  # Apenas para verificar se está funcionando
    
    botao_adicionar = Button(lista_elementos, text="Adicionar", command=adicionar)
    botao_adicionar.grid(column=0, row=5, columnspan=2, padx=10, pady=10, sticky="ew")
   
    lista_elementos.mainloop()
    pass


def excluir_padrao():
    # Função para excluir um padrão selecionado
    lista_excluir = Tk()
    lista_excluir.title("Excluir Padrão")
    escreva_excluir = Label(lista_excluir, text="Selecione o padrão que deseja excluir:")
    escreva_excluir.grid(column=0, row=0, padx=10, pady=10)
    lista_padroes = Listbox(lista_excluir)
    lista_padroes.grid(column=0, row=1, padx=10, pady=10)
    for padrao in padroes.keys():
        lista_padroes.insert(END, padrao)
    def excluir():
        selecionado = lista_padroes.curselection()
        if selecionado:
            padrao_para_excluir = lista_padroes.get(selecionado)
            del padroes[padrao_para_excluir]
            lista_padroes.delete(selecionado)
            salvar_padroes() #salva após excluir
            print(f"Padrão {padrao_para_excluir} excluído.")
    botao_excluir = Button(lista_excluir, text="Excluir", command=excluir)
    botao_excluir.grid(column=0, row=2, padx=10, pady=10)

    lista_excluir.mainloop()
    pass
#________________________________________________________________________________________________________________________________________________________________
#definir padrão a ser utilizado
def escolher_padrao():
    lista_escolher = Tk()
    lista_escolher.title("Escolher Padrão")
    lista_pd = Listbox(lista_escolher)
    lista_pd.grid(column=0, row=0, padx=10, pady=10)
    for padrao in padroes.keys():
        lista_pd.insert(END, padrao)
    def escolher():
        selecionado = lista_pd.curselection()
        if selecionado:
            padrao_escolhido = lista_pd.get(selecionado)
            print(f"Padrão escolhido: {padrao_escolhido}")
            # Aqui você pode adicionar a lógica para usar o padrão escolhido no cálculo
    botao_escolher = Button(lista_escolher, text="Escolher", command=escolher)
    botao_escolher.grid(column=0, row=1, padx=10, pady=10)
    pass
    lista_escolher.mainloop()
#________________________________________________________________________________________________________________________________________________________________
# Configuração da janela principal
janela = Tk()
janela.title("Cálculo de Concentrações")
#janela.geometry("500x300")
#texto arquivo padrão
texto_orientacao = Label(janela, text="Selecione o arquivo.txt para o padrão")
texto_orientacao.grid(column=0, row=0, padx=10, pady=10)
#botão selecionar arquivo padrão
botao_selecionar_padrao = Button(janela, text="Selecionar Arquivo Padrão", command=selecionar_arquivo_padrao)
botao_selecionar_padrao.grid(column=0, row=1, padx=10, pady=10)
#texto exibindo o arquivo padrão selecionado
texto_arquivo_padrao = Label(janela, text= "")
texto_arquivo_padrao.grid(column=0, row=2, padx=10, pady=10)

#texto arquivos amostras
texto_orientacao2 = Label(janela, text="Selecione os arquivos.txt das amostras")
texto_orientacao2.grid(column=1, row=0, padx=10, pady=10)
#botão selecionar arquivos amostras
botao_selecionar_amostras = Button(janela, text="Selecionar Arquivos Amostras", command=selecionar_arquivos_amostras)
botao_selecionar_amostras.grid(column=1, row=1, padx=10, pady=10)
#texto exibindo os arquivos amostras selecionados
texto_arquivos_amostras = Label(janela, text= "")
texto_arquivos_amostras.grid(column=1, row=2, padx=10, pady=10)

#adicionar concentrações padrão
texto_orientacao3 = Label(janela, text="Adicione os padrões certificados e secundários")
texto_orientacao3.grid(column=0, row=3, padx=10, pady=10)
#botão nome do padrão a ser adicionado
caixa_de_texto = Entry(janela, width=30)
caixa_de_texto.grid(column=0, row=4, padx=10, pady=10)
#botão adicionar padrão
botao_adicionar_nome = Button(janela, text="Adicionar Nome do Padrão", command=adicionar_nomes_padrao)
botao_adicionar_nome.grid(column=0, row=5, padx=10, pady=10)
#botão adicionar concentrações dos elementos
botao_adicionar_concentracoes = Button(janela, text="Adicionar Concentrações dos Elementos", command=adicionar_concentracoes_elementos)
botao_adicionar_concentracoes.grid(column=0, row=6, padx=10, pady=10)
#botão de excluir padrão
botao_excluir_padrao = Button(janela, text="Selecione um Padrão para Exluir", command=excluir_padrao)
botao_excluir_padrao.grid(column=0, row=7, padx=10, pady=10)

#selecionar o padrão que deseja utilizar
texto_orientacao4 = Label(janela, text="Selecione o padrão que deseja utilizar")
texto_orientacao4.grid(column=1, row=3, padx=10, pady=10)
botao_escolher_padrao = Button(janela, text="Escolher Padrão", command=escolher_padrao)
botao_escolher_padrao.grid(column=1, row=4, padx=10, pady=10)


janela.mainloop()

