from views.graficosView import GraficosView
from models.graficosModel import GraficosModel

class GraficosVM:
    def __init__(self, master, variaveis):

        self.variaveis = variaveis
                
        self.graficos_view = GraficosView(master)
        self.graficos_view.pack(fill="x", padx=10, pady=10)
        self.graficos_view.botao_grafico.configure(command=self.faz_graficos)

        self.graficos_model = GraficosModel()
        
    def habilita_graficos(self):
        """Habilita o botão Graficos"""
        self.graficos_view.botao_grafico.configure(state="normal")

    def faz_graficos(self):
        #self.variaveis.verificar_estado()
        self.resultados = self.variaveis.resultados        
        self.graficos_var = self.graficos_model.graficos(self.resultados)
        return self.graficos_var
