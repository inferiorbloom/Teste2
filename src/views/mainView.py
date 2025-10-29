import customtkinter as ctk

from viewmodels.calculoVM import CalculoVM
#from viewmodels.padraoVM import PadraoView
from viewmodels.graficosVM import GraficosView
#from viewmodels.exportarVM import ExportarView
#from views.calculoView import CalculoView
#from viewmodels.padraoVM import PadraoModel
#from viewmodels.graficosVM import GraficosVM
#from viewmodels.exportarVM import ExportarVM

# Configurações iniciais do customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class MainView(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🧪 Calculadora de Concentrações")
        self.geometry("1200x700")
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

        titulo = ctk.CTkLabel(self.sidebar, text="≡ Menu", font=("Arial", 18, "bold"))
        titulo.pack(pady=20)

        #Botoes
        self.calculo_vm = CalculoVM(self.sidebar)
        self.calculo_vm.botoes()

        #self.padrao_view = PadraoView(self.sidebar)
        #self.padrao_view.pack(fill="x", padx=10, pady=10)

        #self.exportar_view = ExportarView(self.sidebar)
        #self.exportar_view.pack(fill="x", padx=10, pady=20)

        self.grafico_view = GraficosView(self.sidebar)
        self.grafico_view.pack(fill="x", padx=10, pady=10)

        #Botao Sair
        ctk.CTkButton(self.sidebar, text="Sair", fg_color="red", font=("Arial Black", 12), command=self.quit).pack(side="bottom", pady=20, fill="x", padx=20)

        self.title_label = ctk.CTkLabel(self.main_frame, text="Calcular Concentrações", font=("Arial", 24, "bold"))
        self.title_label.pack(pady=20)

        # Informações carregadas
        self.info_label = ctk.CTkLabel(self.main_frame, text="Nenhum arquivo carregado ainda.", font=("Arial", 16))
        self.info_label.pack(pady=10)

        # Área dos resultados
        self.result_frame = ctk.CTkFrame(self.main_frame)
        self.result_frame.pack(fill="both", expand=True, pady=10)

        self.result_label = ctk.CTkLabel(self.result_frame, text="Resultados: ", font=("Arial", 18))
        self.result_label.pack(pady=30)
'''
    def abrir_calculo(self):
        # Limpa conteúdo do main_frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Cria a ViewModel e a View de cálculo
        self.calculo_vm = CalculoVM(self.main_frame)
        self.calculo_vm.view.pack(fill="both", expand=True)'''
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


