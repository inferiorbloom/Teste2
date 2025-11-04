import customtkinter as ctk

# Configurações iniciais do customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class PadraoView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.frame = ctk.CTkFrame(master)
        self.frame.pack(pady=10)

        self.label_opcoes = ctk.CTkLabel(self.frame, text="Escolha um Padrão:", font=("Arial", 12, "bold"))
        self.label_opcoes.pack(padx=66, pady=10)

        self.lista_dados = {}
        self.selecionado = None

    def lista_box(self, lista):
        self.lista_dados = lista

        if not isinstance(lista, list) or not all(isinstance(item, dict) for item in lista):
            print("Lista precisa ser uma lista de dicionários com chave 'nome'")
            return
    
        nomes = [item["nome"] for item in lista]
        self.combobox = ctk.CTkComboBox(self.frame,
                                        state="readonly",
                                        values=list(nomes),
                                        command=self.ao_selecionar
                                       )
        self.combobox.pack(pady=10)
        
        # Define o valor inicial apenas visualmente
        self.combobox.set(nomes[0])
        self.selecionado = self.lista_dados[0]
        return self.selecionado
    
    def ao_selecionar(self, escolha):
        self.selecionado = next((item for item in self.lista_dados if item["nome"] == escolha), None)
        if self.selecionado:
            print(f"Padrão selecionado em Pd_VIEW (def selecionar): {escolha}")
            print("Elementos em Pd_VIEW (def selecionar):", self.selecionado["elementos"])
            return self.selecionado
        else:
            print("Nenhum padrão encontrado.")
