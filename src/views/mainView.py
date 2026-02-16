import customtkinter as ctk
from viewmodels.concentracaoVM import ConcentracaoVM
import tkinter as tk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class MainView(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🧪 Calculadora de Concentrações")
        self.geometry("1400x800")
        self.resizable(True, True)

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=220)
        self.sidebar.pack(side="left", fill="y")

        # --- MAIN AREA ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # --- Frame dinâmico (conteúdo que muda) ---
        self.dynamic_frame = ctk.CTkFrame(self.main_frame)
        self.dynamic_frame.pack(fill="both", expand=True, pady=10, padx=40)

        titulo = ctk.CTkLabel(self.sidebar, text="☰ Menu", font=("Arial Black", 18, "bold"))
        titulo.pack(pady=20)

        # Botão Sair
        self.botao_sair = ctk.CTkButton(
            self.sidebar, text="Sair", fg_color="red", text_color="#FFFFFF", font=("Arial Black", 12), command=self.quit
        )
        self.botao_sair.pack(side="bottom", pady=20, fill="x", padx=20)

        # Monta tela principal
        self.mostrar_tela_inicial()

    def mostrar_tela_inicial(self):
        # Limpa conteúdo anterior
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()

        # Título
        title = ctk.CTkLabel(self.dynamic_frame, text="Calcular Concentrações.", font=("Arial Black", 24, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(10, 30))

        self.label_instrucoes = ctk.CTkLabel(
            self.dynamic_frame,
            text="No Menu à esquerda escolha um Padrão, selecione os Arquivos necessários e Calcule. \n"
            "Ao fim, exporte-os para o Excel e crie os Gráficos se quiser.",
            font=("Arial", 15),
            justify="center",
        )
        self.label_instrucoes.grid(row=1, column=0, columnspan=2, pady=(10, 30))

        # Configuração de colunas
        self.dynamic_frame.grid_columnconfigure(0, weight=0)  # coluna dos textos
        self.dynamic_frame.grid_columnconfigure(1, weight=1)  # coluna das áreas
        self.dynamic_frame.grid_rowconfigure(1, weight=0)
        self.dynamic_frame.grid_rowconfigure(2, weight=0)
        self.dynamic_frame.grid_rowconfigure(3, weight=0)
        # self.dynamic_frame.grid_rowconfigure(4, weight=1)
        self.dynamic_frame.grid_rowconfigure(4, weight=2)

        # --- Linha 1: Arquivo Padrão ---
        self.label_padrao = ctk.CTkLabel(self.dynamic_frame, text="> Arquivo Padrão:", font=("Arial Black", 16))
        self.label_padrao.grid(row=2, column=0, sticky="", padx=(10, 10), pady=10)

        self.arquivo_frame = ctk.CTkFrame(self.dynamic_frame, width=40, height=40, fg_color="#2b2b2b")
        self.arquivo_frame.grid(row=2, column=1, sticky="w", padx=(10, 10), pady=10)
        self.arquivo_frame.grid_propagate(False)

        # --- Linha 2: Arquivos Amostras ---
        self.label_amostras = ctk.CTkLabel(self.dynamic_frame, text="> Arquivos Amostras:", font=("Arial Black", 16))
        self.label_amostras.grid(row=3, column=0, sticky="", padx=(10, 10), pady=10)

        # Frame externo
        self.amostras_container = ctk.CTkFrame(self.dynamic_frame, fg_color="#2b2b2b")
        self.amostras_container.grid(row=3, column=1, sticky="we", padx=(10, 40), pady=10)
        self.amostras_container.grid_propagate(False)

        # Canvas dentro do frame
        self.amostras_canvas = tk.Canvas(self.amostras_container, height=67, bg="#2b2b2b", highlightthickness=0)
        self.amostras_canvas.pack(fill="both", expand=True)

        # Scroll horizontal
        self.scroll_x = ctk.CTkScrollbar(
            self.amostras_container, orientation="horizontal", command=self.amostras_canvas.xview
        )
        self.scroll_x.pack(side="bottom", fill="x")

        self.amostras_canvas.configure(xscrollcommand=self.scroll_x.set)

        # Frame real onde os nomes serão colocados
        self.amostras_frame = ctk.CTkFrame(self.amostras_canvas, fg_color="#2b2b2b")
        self.amostras_window = self.amostras_canvas.create_window((0, 0), window=self.amostras_frame, anchor="nw")

        # Atualiza área rolável
        def update_scroll(event=None):
            self.amostras_canvas.configure(scrollregion=self.amostras_canvas.bbox("all"))

        self.amostras_frame.bind("<Configure>", update_scroll)

        # --- Linha 3: Resultados ---
        result_label = ctk.CTkLabel(self.dynamic_frame, text="- Resultados:", font=("Arial Black", 20))
        result_label.grid(row=4, column=0, sticky="", pady=(40, 10))

        self.result_frame = ctk.CTkFrame(self.dynamic_frame, height=500)
        self.result_frame.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=40, pady=(0, 20))
        self.result_frame.grid_propagate(False)

        if not hasattr(self, "calculo_vm"):
            # --- Instância da ViewModel ---
            self.calculo_vm = ConcentracaoVM(
                self.sidebar,
                self.result_frame,
                self.arquivo_frame,
                self.amostras_frame,
                self.dynamic_frame,
                self.mostrar_tela_inicial,
            )
            if not hasattr(self, "botoes_criados"):
                self.calculo_vm.botoes()
                self.botoes_criados = True  # marca que já criou os botoes
