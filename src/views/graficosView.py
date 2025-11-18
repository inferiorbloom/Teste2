import customtkinter as ctk
from PIL import Image

# Configurações iniciais do customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class GraficosView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        icone_graficos = ctk.CTkImage(light_image=Image.open("imagens/icones/graficos.png"), size=(20, 20))

        self.label = ctk.CTkLabel(self, text="Crie Gráficos:", font=("Arial", 14, "bold"))
        self.label.pack(pady=10, fill="x", padx=20)

        self.botao_grafico = ctk.CTkButton(self, state="disabled", image=icone_graficos, text="Gráficos", font=("Arial", 12), command="")
        self.botao_grafico.pack(pady=10, fill="x", padx=20)
