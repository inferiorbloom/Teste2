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
