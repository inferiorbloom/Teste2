from views.exportarView import ExportarView
from models.exportarModel import ExportarModel

class ExportarVM:
    def __init__(self, master, variaveis):

        self.variaveis = variaveis
        self.arquivos_amostras = self.variaveis.lista_arquivos
        self.resultados = self.variaveis.resultados

        self.exportar_model = ExportarModel()

        self.export = ExportarView(master)
        self.export.pack(fill="x", padx=10, pady=10)
        self.export.exportar_botao.configure(command=self.exporta_excel)

    def habilita_exporta_excel(self):
        """Habilita o botão Exportar"""
        self.export.exportar_botao.configure(state="normal")
             
    def exporta_excel(self):
        #print('Exportando...')
        #self.variaveis.verificar_estado()        
        self.exporta_excel_var = self.exportar_model.exportar_para_excel(self.arquivos_amostras, self.resultados[0])
        return self.exporta_excel_var
    