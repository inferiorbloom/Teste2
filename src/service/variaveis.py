import customtkinter as ctk
import json
import os

class Variaveis(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        #Variaveis de inicializacao
        self.arquivo_padrao = None
        self.arquivos_amostras = None

        # Variáveis para armazenar arquivos selecionados
        self.lista_arquivo_padrao = self.arquivo_padrao
        self.lista_arquivos = self.arquivos_amostras
        #self.resultado_var = ctk.StringVar()

        #self.padrao_escolhido = None

        self.padroes = {}
        path = r'padroes/padroes.json'
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                self.padroes = json.load(f)
       

 