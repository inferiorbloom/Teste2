import customtkinter as ctk
import json
import os

class Variaveis(ctk.CTkFrame):
    def __init__(self, master=None):
        self.lista_arquivo_padrao = None
        self.lista_arquivos = []
        self.padroes = []
        self.resultados = {}  #vamos usar isso para armazenar resultados

        self.padroes = {}
        path = r'padroes/padroes.json'
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                self.padroes = json.load(f)
        
    def verificar_estado(self):
        print("Verificando estado atual das variáveis:")
        print(f"- Arquivo padrão: {self.lista_arquivo_padrao}")
        print(f"- Amostras: {self.lista_arquivos}")
        print(f"- Resultados: {'OK' if self.resultados else 'Nenhum'}")

    

'''
        #Variaveis de inicializacao
        self.arquivo_padrao = None
        self.arquivos_amostras = None
        self.resultados = None

        # Variáveis para armazenar arquivos selecionados
        self.lista_arquivo_padrao = self.arquivo_padrao
        self.lista_arquivos = self.arquivos_amostras
        self.resultados_var = self.resultados
'''
