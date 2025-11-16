import customtkinter as ctk

# Configurações iniciais do customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class PadraoView(ctk.CTkFrame):
    def __init__(self, master, frame):
        super().__init__(master)

        self.frame = frame

        self.label_opcoes = ctk.CTkLabel(self.frame, text="Escolha um Padrão:", font=("Arial", 14, "bold"))
        self.label_opcoes.pack(padx=54, pady=10)

        self.lista_dados = {}
        self.selecionado = None

    def lista_box(self, lista, gerenciar_padraovm):
        self.lista_dados = lista
        self.gerenciar_padraovm = gerenciar_padraovm
                        
        if not isinstance(lista, list) or not all(isinstance(item, dict) for item in lista):
            print("Lista precisa ser uma lista de dicionários com chave 'nome'")
            return
    
        nomes = [item["nome"] for item in lista]
        self.combobox = ctk.CTkComboBox(self.frame,
                                        button_color="#213A57",
                                        border_color="#213A57",
                                        fg_color="#375270",
                                        state="readonly",
                                        values=list(nomes),
                                        font=("Arial", 12),
                                        command=self.ao_selecionar
                                       )
        self.combobox.pack(side="right", padx=(0, 20))
        self.botao_gerenciar = self.gerenciar_padraovm.botao_gerenciar()
        
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

    def atualizar_lista(self, nova_lista):
        """ Atualiza a ComboBox após salvar novos padrões no JSON """
        self.lista_dados = nova_lista
        nomes = [item["nome"] for item in nova_lista]

        # Atualizar valores
        if self.combobox:
            self.combobox.configure(values=nomes)

        # Selecionar o primeiro automaticamente
        if nomes:
            self.combobox.set(nomes[0])
            self.selecionado = nova_lista[0]

        #print("ComboBox atualizada com:", nomes)
