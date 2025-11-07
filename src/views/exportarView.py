import customtkinter as ctk
from PIL import Image

# Configurações iniciais do customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class ExportarView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        icone_excel = ctk.CTkImage(light_image=Image.open("imagens/icones/excel.png"), size=(20, 20))
        self.exportar_botao = ctk.CTkButton(self, text="Exportar para Excel",
                       state="disabled",
                        command="",
                        image=icone_excel,
                        compound="left",
                        font=("Arial", 12))
        self.exportar_botao.pack(pady=10, fill="x", padx=20)
