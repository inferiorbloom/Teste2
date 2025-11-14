from models.PadraoModel import PadraoModel
from views.PadraoView import PadraoView
from service.variaveis import Variaveis
from viewmodels.gerenciarPadraoVM import Gerenciar_PadraoVM
import customtkinter as ctk
class PadraoVM:
    def __init__(self, master, dynamic_frame, sidebar_frame):
        self.frame = ctk.CTkFrame(master)
        self.frame.pack(pady=10)

        self.padrao_view = PadraoView(master, self.frame)
        self.padrao_model = PadraoModel()

        self.variaveis = Variaveis(master)
        self.variaveis.padroes
        
        self.gerenciar_padraovm = Gerenciar_PadraoVM(dynamic_frame, sidebar_frame, self.frame)
                
    def volta_padrao(self):
        self.lista_padrao = self.variaveis.padroes
        #print("Padroes carregados:", self.lista_padrao)
        return self.padrao_view.lista_box(self.lista_padrao, self.gerenciar_padraovm)
    
    def c_padrao_lista_selecionado(self):
        escolha_atual = self.padrao_view.combobox.get()
        self.selecionado = next((item for item in self.padrao_view.lista_dados if item["nome"] == escolha_atual), None)
        return self.selecionado
       