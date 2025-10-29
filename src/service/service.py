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
        #texto_arquivo_padrao.grid(column=0, row=3, padx=10, pady=10)
        texto_arquivo_padrao.configure(text=os.path.basename(arquivo_padrao))
        return arquivo_padrao

    # Função para selecionar arquivos das amostras
    def selecionar_arquivos_amostras(self):
        arquivos = askopenfilenames(title="Selecione os arquivos.txt que deseja utilizar como AMOSTRAS!", 
                                    filetypes=[("Arquivos de texto", "*.txt")])
        texto_arquivos_amostras = ctk.CTkLabel(self.master, text="")
        #texto_arquivos_amostras.grid(column=1, row=3, padx=10, pady=10, sticky="n")
        if arquivos:
            ultimo = os.path.basename(arquivos[-1])
            primeiro = os.path.basename(arquivos[0])
            texto_arquivos_amostras.configure(text=f"{primeiro} ... {ultimo}")
        else:
            texto_arquivos_amostras.configure(text="Nenhum arquivo selecionado")
        return arquivos
