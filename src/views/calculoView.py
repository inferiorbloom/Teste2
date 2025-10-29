import customtkinter as ctk
from PIL import Image

class CalculoView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Carregando ícone
        icone_pasta = ctk.CTkImage(light_image=Image.open("imagens/icones/pasta.png"), size=(20, 20))
        icone_file = ctk.CTkImage(light_image=Image.open("imagens/icones/file.png"), size=(20, 20))
        icone_calcular = ctk.CTkImage(light_image=Image.open("imagens/icones/calcular.png"), size=(20, 20))
        icone_padrao = ctk.CTkImage(light_image=Image.open("imagens/icones/padrao.png"), size=(20, 20))

        self.selecionar_arquivo_padrao = ctk.CTkButton(self, text="Selecionar Padrão",
                        image=icone_file, 
                        compound="left")
        self.selecionar_arquivo_padrao.pack(pady=10, fill="x", padx=20)

        self.selecionar_amostras = ctk.CTkButton(self, text="Selecionar Amostras",
                        image=icone_pasta, compound="left")
        self.selecionar_amostras.pack(pady=10, fill="x", padx=20)

        self.escolher_padrao = ctk.CTkButton(self, text="Escolher Padrão",
                command="", image=icone_padrao, compound="left")
        self.escolher_padrao.pack(pady=10, fill="x", padx=20)
        
        self.calcular = ctk.CTkButton(self, text="Calcular Concentrações", font=("Arial Black", 12),
                       state="disabled",
                       fg_color="#0D740F", text_color="#FFFFFF",
                        command="", image=icone_calcular, compound="left")
        self.calcular.pack(pady=40, fill="x", padx=20)



     
        # Para habilitar o botão de calcular apenas quando os arquivos forem selecionados
        #selecionado_arquivo_padrao = False
        #selecionado_amostras = False
        #selecionado_padrao = False
        #def habilitar_calcular(selecionado_arquivo_padrao, selecionado_amostras, selecionado_padrao):
        #    if selecionado_arquivo_padrao and selecionado_amostras and selecionado_padrao:
        #        botao_calcular.configure(state="normal", command=calcular_concentracoes)

#_____________________________________________________________________________________________________________________________________________________________________________________

#_____________________________________________________________________________________________________________________________________________________________________________________
# Título
#titulo = ctk.CTkLabel(frame_cima, text="Seleção de Dados", font=("Arial Black", 24))
#titulo.grid(row=0, column=0, padx=10, pady=10, sticky="ew", columnspan=2)
# Faz as colunas ocuparem espaço proporcional
#frame_cima.grid_columnconfigure(0, weight=1)
#frame_cima.grid_columnconfigure(1, weight=1)

# Textos à esquerda dentro do frame cima ----------  Seleção de padrão

#texto_arquivo_padrao = ctk.CTkLabel(frame_cima, text="")
#texto_arquivo_padrao.grid(column=0, row=3, padx=10, pady=10)

# Textos à direita dentro do frame cima ----------  Seleção de amostras

#texto_arquivos_amostras = ctk.CTkLabel(frame_cima, text="")
#texto_arquivos_amostras.grid(column=1, row=3, padx=10, pady=10, sticky="n")


