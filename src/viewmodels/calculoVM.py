from models.calculoModel import CalculoModel
from views.calculoView import CalculoView
from service.service import Service
from service.variaveis import Variaveis
from viewmodels.exportarVM import ExportarVM
import customtkinter as ctk

class CalculoVM:
    def __init__(self, master):

        self.view = CalculoView(master)
        self.view.pack(fill="x", padx=10, pady=10)
        
        self.model = CalculoModel()
        self.service = Service(master)
        self.variaveis = Variaveis(master)
        
        self.export = ExportarVM(master)
        self.export.export

        # Inicializar atributos
        self.arquivo_padrao = None
        self.arquivos_amostras = None

        # Variáveis para armazenar arquivos selecionados
        self.lista_arquivo_padrao = self.arquivo_padrao
        self.lista_arquivos = self.arquivos_amostras
        self.resultado_var = ctk.StringVar()

    def botoes(self):
        # Conectar os botões da View aos métodos da VM
        self.view.selecionar_arquivo_padrao.configure(command=self.padrao)
        self.view.selecionar_amostras.configure(command=self.amostras)
        self.view.calcular.configure(command=self.calcular)

    def padrao(self):
        arquivo = self.service.selecionar_arquivo_padrao()
        if arquivo:
            self.arquivo_padrao = arquivo
            self._verificar_pronto()
            print("Arquivo padrão selecionado:", self.arquivo_padrao)
        return self.arquivo_padrao

    def amostras(self):
        arquivos = list(self.service.selecionar_arquivos_amostras())
        if arquivos:
            self.arquivos_amostras = arquivos
            self._verificar_pronto()
            print("Arquivos de amostras selecionadas:", self.arquivos_amostras)
        return self.arquivos_amostras

    def _verificar_pronto(self):
        """Habilita o botão Calcular quando tudo estiver selecionado."""
        if self.arquivos_amostras and self.arquivo_padrao:
            self.view.calcular.configure(state="normal")

    def calcular(self):
        self.resultado = self.model.calcular_concentracoes(self.arquivos_amostras, self.arquivo_padrao)
        if self.resultado:
            self.exportar()
        return self.resultado
    
    def exportar(self):
        """Habilita o botão Exportar"""
        self.export.export.exportar_botao.configure(state="normal")

