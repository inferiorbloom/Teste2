import customtkinter as ctk
from PIL import Image

# Configurações iniciais do customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class LimiteDeteccaoView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        icone_lista = ctk.CTkImage(light_image=Image.open("imagens/icones/lista.png"), size=(20, 20))

        self.botao_limite = ctk.CTkButton(
            self, state="disabled", image=icone_lista, text="FullReport", font=("Arial", 12), command=""
        )
        self.botao_limite.pack(pady=10, fill="x", padx=20)
