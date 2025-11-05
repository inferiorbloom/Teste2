import customtkinter as ctk
from viewmodels.calculoVM import CalculoVM
#from viewmodels.gerenciarPadraoVM import Gerenciar_PadraoVM
#from viewmodels.graficosVM import GraficosView
#from viewmodels.graficosVM import GraficosVM
#from viewmodels.exportarVM import ExportarVM

# Configurações iniciais do customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class MainView(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🧪 Calculadora de Concentrações")
        self.geometry("1200x800")
        self.resizable(True, True)

        # --- VARIÁVEIS ---
        self.data_file = None
        self.standard_file = None
        self.standards = []

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=220)
        self.sidebar.pack(side="left", fill="y")
    
        # --- MAIN AREA ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # 🔹 Frame dinâmico — é o único que será limpo ao trocar telas
        self.dynamic_frame = ctk.CTkFrame(self.main_frame)
        self.dynamic_frame.pack(fill="both", expand=True, pady=10)

        titulo = ctk.CTkLabel(self.sidebar, text="≡ Menu", font=("Arial", 18, "bold"))
        titulo.pack(pady=20)

        self.mostrar_tela_inicial()

        #Chama os Botoes Gerais e os Resultados
        self.calculo_vm = CalculoVM(self.main_frame, self.sidebar, self.result_frame, self.arquivos_frame, self.dynamic_frame, self.mostrar_tela_inicial)
        self.calculo_vm.botoes()

        #Botao dos Graficos
        #self.grafico_view = GraficosView(self.sidebar)
        #self.grafico_view.pack(fill="x", padx=10, pady=10)

        #Botao Sair
        ctk.CTkButton(self.sidebar, text="Sair", fg_color="red", font=("Arial Black", 12), command=self.quit).pack(side="bottom", pady=20, fill="x", padx=20)
        
    def mostrar_tela_inicial(self):
        """Recria apenas o conteúdo dinâmico da tela principal."""
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()

        title = ctk.CTkLabel(self.dynamic_frame, text="Calcular Concentrações", font=("Arial", 24, "bold"))
        title.pack(pady=20)

        # Área dos arquivos
        self.arquivos_frame = ctk.CTkFrame(self.dynamic_frame)
        self.arquivos_frame.pack(pady=10, fill="x", padx=40)

        # --- ARQUIVO PADRÃO ---
        ctk.CTkLabel(self.arquivos_frame, text="Arquivo Padrão:", font=("Arial", 16))
        self.label_padrao = ctk.CTkLabel(self.arquivos_frame, text="Nenhuma selecionada", font=("Arial", 14))
        #self.label_padrao.grid(row=0, column=1, sticky="w", padx=10)

        # --- ARQUIVOS AMOSTRAS ---
        ctk.CTkLabel(self.arquivos_frame, text="Arquivos Amostras:", font=("Arial", 16))
        self.label_amostras = ctk.CTkLabel(self.arquivos_frame, text="Nenhuma selecionada", font=("Arial", 14))

        result_label = ctk.CTkLabel(self.dynamic_frame, text="Resultados:", font=("Arial Black", 20))
        result_label.pack(pady=10)

        # Área dos resultados
        self.result_frame = ctk.CTkFrame(self.dynamic_frame)
        self.result_frame.pack(fill="both", expand=True, pady=10)
        







