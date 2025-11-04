import customtkinter as ctk
from PIL import Image

class CalculoView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Carregando ícone
        icone_pasta = ctk.CTkImage(light_image=Image.open("imagens/icones/pasta.png"), size=(20, 20))
        icone_file = ctk.CTkImage(light_image=Image.open("imagens/icones/file.png"), size=(20, 20))
        icone_calcular = ctk.CTkImage(light_image=Image.open("imagens/icones/calcular.png"), size=(20, 20))

        self.selecionar_arquivo_padrao = ctk.CTkButton(self, text="Selecionar Arquivo Padrão",
                        image=icone_file, 
                        compound="left")
        self.selecionar_arquivo_padrao.pack(pady=10, fill="x", padx=20)

        self.selecionar_amostras = ctk.CTkButton(self, text="Selecionar Amostras",
                        image=icone_pasta, compound="left")
        self.selecionar_amostras.pack(pady=10, fill="x", padx=20)
        
        self.calcular = ctk.CTkButton(self, text="Calcular Concentrações", font=("Arial Black", 12),
                       state="disabled",
                       fg_color="#0D740F", text_color="#FFFFFF",
                        command="", image=icone_calcular, compound="left")
        self.calcular.pack(pady=40, fill="x", padx=20)

class CalculoResultadoView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.resultado_textbox = ctk.CTkTextbox(self, height=300, font=("Arial", 16))
        self.resultado_textbox.pack(padx=20, pady=20, fill="both", expand=True)

    def mostrar_resultados(self, concentracoes):
        #print(concentracoes)
        resultado_texto = ""
        for chave, dados in concentracoes.items():
            resultado_texto += f"--- {chave} ---\n"
            for amostra, valores in dados.items():
                resultado_texto += f"{amostra}: {valores}\n"

        print(resultado_texto)

        self.resultado_textbox.delete("1.0", "end")
        self.resultado_textbox.insert("1.0", resultado_texto)
        self.resultado_textbox.configure(state="disabled")

class AttArquivoSelecionado(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

    def texto_pd(self, texto):
        self.texto_arquivo_pd = ctk.CTkLabel(self, text=texto, font=("Arial", 16)).pack(pady=10)

    def texto_am(self, texto):
        self.texto_arquivos_am = ctk.CTkLabel(self, text=texto, font=("Arial", 16)).pack(pady=10)    


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


