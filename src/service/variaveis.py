import customtkinter as ctk
import json
import os

class Variaveis(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.lista_arquivo_padrao = None
        self.lista_arquivos = []
        self.resultados = [None, None]  #armazena os resultados (concentracoes e areas normalizadas)

        self.padroes = {}
        self.path = r'padroes/padroes.json'
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as f:
                self.padroes = json.load(f)
        
    def verificar_estado(self):
        print("Verificando estado atual das variáveis:")
        print(f"- Arquivo padrão: {self.lista_arquivo_padrao}")
        print(f"- Amostras: {self.lista_arquivos}")
        print(f"- Resultados: {'OK' if self.resultados else 'Nenhum'}")
