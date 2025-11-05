import os
from views.calculoView import CalculoView, CalculoResultadoView, AttArquivoSelecionado
from models.calculoModel import CalculoModel
from service.service import Service
from service.variaveis import Variaveis
from viewmodels.exportarVM import ExportarVM
from viewmodels.padraoVM import PadraoVM
#from viewmodels.gerenciarPadraoVM import Gerenciar_PadraoVM

class CalculoVM:
    def __init__(self, main_frame, sidebar_frame, result_frame, arquivos_frame, dynamic_frame, mostrar_tela_inicial):
        self.main_frame = main_frame
        self.sidebar_frame = sidebar_frame
        self.result_frame = result_frame
        self.arquivos_frame = arquivos_frame
        self.dynamic_frame = dynamic_frame
        self.mostrar_tela_inicial = mostrar_tela_inicial

        # Variáveis para armazenar arquivos selecionados
        self.variaveis = Variaveis(sidebar_frame)
        self.arquivo_padrao = self.variaveis.lista_arquivo_padrao
        self.arquivos_amostras = self.variaveis.lista_arquivos

        #Chama os arquivos de service
        self.service = Service(sidebar_frame)

        self.padrao_vm = PadraoVM(sidebar_frame, dynamic_frame, sidebar_frame, mostrar_tela_inicial)
        self.padrao_vm.padrao_view
        self.lista_padrao = self.padrao_vm.volta_padrao()

        #Chama os calculos de concentracao
        self.model = CalculoModel()

        #Chama a view dos botoes de calcular
        self.view = CalculoView(sidebar_frame)
        self.view.pack(fill="x", padx=10, pady=10)

        #Chama o resultado
        self.resultados = CalculoResultadoView(result_frame)
        self.resultados.pack(fill="x", padx=10, pady=10)
        self.resultados.resultado_textbox.insert("1.0", "")

        self.texto_arquivo = AttArquivoSelecionado(arquivos_frame)
        self.texto_arquivo.pack(fill="x", padx=10, pady=10)
                
        self.export = ExportarVM(sidebar_frame, self.variaveis)
        self.export.export

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
            #print("Arquivo de padrão selecionado:", self.arquivo_padrao)
            self.texto_arquivo.texto_pd("Arquivo padrão selecionado: " + os.path.basename(self.arquivo_padrao))
        return self.arquivo_padrao

    def amostras(self):
        arquivos = list(self.service.selecionar_arquivos_amostras())
        if arquivos:
            self.arquivos_amostras = arquivos
            self._verificar_pronto()
            #print("Arquivos de amostras selecionadas:", self.arquivos_amostras)
            nomes_amostras = [os.path.basename(a) + "," for a in arquivos]
            self.texto_arquivo.texto_am(nomes_amostras)
        return self.arquivos_amostras

    def _verificar_pronto(self):
        """Habilita o botão Calcular quando tudo estiver selecionado."""
        if self.arquivos_amostras and self.arquivo_padrao:
            self.view.calcular.configure(state="normal")

    def calcular(self):
        self.c_padrao = self.padrao_vm.teste()
        self.resultado = self.model.calcular_concentracoes(self.arquivos_amostras, self.arquivo_padrao, self.c_padrao)
        
        # Atualiza Variaveis global
        self.variaveis.resultados = self.resultado
        self.variaveis.lista_arquivos = self.arquivos_amostras
        self.variaveis.lista_arquivo_padrao = self.arquivo_padrao

        # Atualiza a instância dentro de ExportarVM
        self.export.arquivos_amostras = self.variaveis.lista_arquivos
        self.export.resultados = self.variaveis.resultados
        if self.resultado:
            self.export.habilita_exporta_excel()
        return self.resultados.mostrar_resultados(self.resultado)
    


