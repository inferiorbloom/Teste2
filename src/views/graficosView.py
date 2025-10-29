import customtkinter as ctk
from PIL import Image

# Configurações iniciais do customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class GraficosView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ctk.CTkButton(self, text="Gráficos", command="").pack(pady=10, fill="x", padx=20)
