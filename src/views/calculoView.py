import customtkinter as ctk
from PIL import Image

class CalculoView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Carregando ícone
        icone_pasta = ctk.CTkImage(light_image=Image.open("imagens/icones/pasta.png"), size=(20, 20))
        icone_file = ctk.CTkImage(light_image=Image.open("imagens/icones/file.png"), size=(20, 20))
        icone_calcular = ctk.CTkImage(light_image=Image.open("imagens/icones/calcular.png"), size=(20, 20))

        self.label_select = ctk.CTkLabel(self, text="Selecione os arquivos:", font=("Arial", 14, "bold"))
        self.label_select.pack(pady=10, fill="x", padx=20)

        self.selecionar_arquivo_padrao = ctk.CTkButton(self, text="Selecionar Arquivo Padrão",
                        image=icone_file, 
                        compound="left", font=("Arial", 12))
        self.selecionar_arquivo_padrao.pack(pady=10, fill="x", padx=20)

        self.selecionar_amostras = ctk.CTkButton(self, text="Selecionar Amostras",
                        image=icone_pasta, compound="left", font=("Arial", 12))
        self.selecionar_amostras.pack(pady=10, fill="x", padx=20)

        self.label_calc = ctk.CTkLabel(self, text="Calcule:", font=("Arial", 14, "bold"))
        self.label_calc.pack(pady=10, fill="x", padx=20)

        self.calcular = ctk.CTkButton(self, text="Calcular Concentrações", font=("Arial Black", 12),
                       state="disabled",
                       fg_color="#0D740F", text_color="#FFFFFF",
                        command="", image=icone_calcular, compound="left")
        self.calcular.pack(pady=10, fill="x", padx=20)

class CalculoResultadoView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # frame rolável que será a planilha
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="#2b2b2b")
        self.scroll.pack(fill="both", expand=True, padx=20, pady=20)

    # apagar conteúdo antigo
    def limpar(self):
        for w in self.scroll.winfo_children():
            w.destroy()

    # mostrar resultados como planilha
    def mostrar_resultados(self, concentracoes):
        self.limpar()

        # Junta todos os elementos presentes em qualquer amostra
        todos_elementos = set()
        for conc_amostra in concentracoes.values():
            for nome_amostra, elementos in conc_amostra.items():
                todos_elementos.update(elementos.keys())
        todos_elementos = sorted(todos_elementos)

        # cria cabeçalho
        ctk.CTkLabel(self.scroll, text="Amostra", font=("Arial Black", 15)).grid(
            row=0, column=0, padx=10, pady=10
        )

        for col, elemento in enumerate(todos_elementos, start=1):
            ctk.CTkLabel(self.scroll, text=elemento, font=("Arial Black", 14)).grid(
                row=0, column=col, padx=10, pady=10
            )

        # cria linhas da tabela
        row = 1
        for conc_amostra in concentracoes.values():
            for nome_amostra, elementos in conc_amostra.items():
                # nome da amostra
                ctk.CTkLabel(self.scroll, text=nome_amostra, font=("Arial Black", 14)).grid(
                    row=row, column=0, padx=10, pady=5, sticky="w"
                )
                # valores por elemento
                for col, elemento in enumerate(todos_elementos, start=1):
                    valor = elementos.get(elemento, "-")
                    ctk.CTkLabel(self.scroll, text=str(valor), font=("Arial", 14)).grid(
                        row=row, column=col, padx=10, pady=5
                    )
                row += 1

class AttArquivoSelecionado(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Cria os labels vazios apenas UMA VEZ
        self.label = ctk.CTkLabel(self, text="", font=("Arial", 16))
        self.label.pack(pady=10)

    def atualizar(self, texto):
        self.label.configure(text=texto)
