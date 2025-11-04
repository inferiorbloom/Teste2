from models.PadraoModel import PadraoModel
from views.PadraoView import PadraoView
from service.variaveis import Variaveis

class PadraoVM:
    def __init__(self, master):

        self.padrao_view = PadraoView(master)
        self.padrao_model = PadraoModel()

        self.variaveis = Variaveis(master)
        self.variaveis.padroes
        
    def volta_padrao(self):
        self.lista_padrao = self.variaveis.padroes
        #print("Padroes carregados:", self.lista_padrao)
        return self.padrao_view.lista_box(self.lista_padrao)
    
    def teste(self):
        escolha_atual = self.padrao_view.combobox.get()
        self.selecionado = next((item for item in self.padrao_view.lista_dados if item["nome"] == escolha_atual), None)
        return self.selecionado
       