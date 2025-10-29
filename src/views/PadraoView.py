import customtkinter as ctk
from PIL import Image

# Configurações iniciais do customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class PadraoView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        icone_padrao = ctk.CTkImage(light_image=Image.open("imagens/icones/padrao.png"), size=(20, 20))
        ctk.CTkButton(self, text="⚙️ Gerenciar Padrões",
                       command="").pack(pady=10, fill="x", padx=20)
        ctk.CTkButton(self, text="Escolher Padrão",
                       command="", image=icone_padrao, compound="left").pack(pady=10, fill="x", padx=20)
        
class Teste(ctk.CTkToplevel):
    def __init__(self, sidebar):
        super().__init__()
        self.sidebar = sidebar

    def gerenciarPadroes(self):
        self.title("Gerenciar Padrões")
        self.geometry("640X320")
        self.resizable(True, True)

        icone_remover = ctk.CTkImage(light_image=Image.open("imagens/icones/remover.png"), size=(20, 20))
        icone_adicionar = ctk.CTkImage(light_image=Image.open("imagens/icones/adicionar.png"), size=(20, 20))

        #Botoes
        ctk.CTkButton(self.sidebar, text="Adicionar", command="", image=icone_adicionar, compound="left").grid(column=0, row=3, padx=10, pady=10)
        ctk.CTkButton(self.sidebar, text="Escrever", command="", image=icone_adicionar, compound="left").grid(column=0, row=6, padx=10, pady=10)
        ctk.CTkButton(self.sidebar, text="Excluir Padrão", command="", image=icone_remover, compound="left").grid(column=0, row=9, padx=7, pady=10)

        gerenciador = ctk.CTkToplevel(self.sidebar)
        gerenciador.transient(self.sidebar)  # Torna a janela filha da janela principal
        gerenciador.grab_set()  # Impede interação com a janela principal enquanto esta está aberta
        
    # Centraliza na tela
        gerenciador.update_idletasks()

        # Tela de gerenciar padrões
        texto_orientacao3 = ctk.CTkLabel(self.sidebar, 
                                         text="Adicione Padrões Certificados", 
                                         font=("Arial Black", 18), 
                                         wraplength=200)
        texto_orientacao3.grid(column=0, row=1, padx=10, pady=10)

        caixa_de_texto = ctk.CTkEntry(self.sidebar, width=250)
        caixa_de_texto.grid(column=0, row=2, padx=10, pady=10)

        espaco = ctk.CTkLabel(self.sidebar, text="")
        espaco.grid(column=0, row=4, padx=10, pady=10)

        texto_orientacao6 = ctk.CTkLabel(self.sidebar, 
                                         text="Escreva as Concentrações", 
                                         font=("Arial Black", 18), 
                                         wraplength=200)
        texto_orientacao6.grid(column=0, row=5, padx=10, pady=10)
