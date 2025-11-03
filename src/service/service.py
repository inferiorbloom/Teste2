import os
import customtkinter as ctk
from tkinter.filedialog import askopenfilename, askopenfilenames

class Service:
    def __init__(self, master):
        super().__init__()
        self.master = master

    # Função para selecionar arquivo padrão 
    def selecionar_arquivo_padrao(self):
        arquivo_padrao = askopenfilename(title="Selecione o arquivo.txt que deseja utilizar como PADRÃO!", 
                                         filetypes=[("Arquivos de texto", "*.txt")])
        texto_arquivo_padrao = ctk.CTkLabel(self.master, text="")
        texto_arquivo_padrao.configure(text=os.path.basename(arquivo_padrao))
        #arquivo = os.path.basename(arquivo_padrao)
        return arquivo_padrao

    # Função para selecionar arquivos das amostras
    def selecionar_arquivos_amostras(self):
        arquivos_amostras = askopenfilenames(title="Selecione os arquivos.txt que deseja utilizar como AMOSTRAS!", 
                                    filetypes=[("Arquivos de texto", "*.txt")])
        texto_arquivos_amostras = ctk.CTkLabel(self.master, text="")
        if arquivos_amostras:
            ultimo = os.path.basename(arquivos_amostras[-1])
            primeiro = os.path.basename(arquivos_amostras[0])
            texto_arquivos_amostras.configure(text=f"{primeiro} ... {ultimo}")
        else:
            texto_arquivos_amostras.configure(text="Nenhum arquivo selecionado")
        return arquivos_amostras

'''
    # Função para selecionar arquivos das amostras
    def selecionar_arquivos_amostras(self):
        arquivos_amostras = askopenfilenames(title="Selecione os arquivos.txt que deseja utilizar como AMOSTRAS!", 
                                    filetypes=[("Arquivos de texto", "*.txt")])
        texto_arquivos_amostras = ctk.CTkLabel(self.master, text="")
        if arquivos_amostras:
            #nomes_amostras = [os.path.basename(a) for a in arquivos_amostras]
            texto_arquivos_amostras.configure(text=f"{nomes_amostras[0]} ... {nomes_amostras[-1]}")
        else:
            texto_arquivos_amostras.configure(text="Nenhum arquivo selecionado")
        return nomes_amostras
'''

