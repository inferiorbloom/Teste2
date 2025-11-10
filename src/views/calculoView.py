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
                        compound="left", font=("Arial", 12))
        self.selecionar_arquivo_padrao.pack(pady=10, fill="x", padx=20)

        self.selecionar_amostras = ctk.CTkButton(self, text="Selecionar Amostras",
                        image=icone_pasta, compound="left", font=("Arial", 12))
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
        self.resultado_textbox.configure(state="disabled")

    def mostrar_resultados(self, concentracoes):
        # Monta texto
        resultado_texto = ""
        for chave, dados in concentracoes.items():
            resultado_texto += f"--- {chave} ---\n"
            for amostra, valores in dados.items():
                resultado_texto += f"{amostra}: {valores}\n"

        # Habilita antes de atualizar
        self.resultado_textbox.configure(state="normal")

        # Limpa e escreve
        self.resultado_textbox.delete("1.0", "end")
        self.resultado_textbox.insert("1.0", resultado_texto)

        # Bloqueia edição novamente
        self.resultado_textbox.configure(state="disabled")

class AttArquivoSelecionado(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Cria os labels vazios apenas UMA VEZ
        self.label = ctk.CTkLabel(self, text="", font=("Arial", 16))
        self.label.pack(pady=10)

    def atualizar(self, texto):
        self.label.configure(text=texto)





