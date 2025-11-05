import customtkinter as ctk
from PIL import Image

# Configurações iniciais do customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class Gerenciar_PadraoView(ctk.CTkFrame):
    def __init__(self, sidebar, frame, dynamic_frame):
        super().__init__(sidebar)

        self.sidebar = sidebar
        self.frame = frame
        self.dynamic_frame = dynamic_frame

        icone_gear = ctk.CTkImage(light_image=Image.open("imagens/icones/gear.png"), size=(20, 20))

        # Botão Gerenciar
        self.botao_gerenciar = ctk.CTkButton(
            #self.sidebar,
            self.frame,
            text="",
            image=icone_gear,
            width=40,
            height=30,
            corner_radius=8,
            font=("Arial Black", 12),
            fg_color="#213A57",
            #hover_color="#777777",
            command=""
        )
        self.botao_gerenciar.pack(side="right", padx=(0, 20))

        self.texto_gerenciar = ctk.CTkLabel(self.dynamic_frame, text="Gerenciar Padroes", font=("Arial Black", 20))
        
        
