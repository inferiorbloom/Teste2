import customtkinter as ctk

class Variaveis(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Variáveis para armazenar arquivos selecionados
        self.lista_arquivo_padrao = list()
        self.lista_arquivos = list()
        self.resultado_var = ctk.StringVar()


