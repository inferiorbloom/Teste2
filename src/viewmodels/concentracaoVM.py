import os
from views.concentracaoView import ConcentracaoView, ConcentracaoResultadoView, AttArquivoSelecionado
from models.concentracaoModel import ConcentracaoModel
from service.fileService import Service
from store.variaveis import Variaveis
from viewmodels.exportarVM import ExportarVM
from viewmodels.padraoVM import PadraoVM
from viewmodels.graficosVM import GraficosVM
from viewmodels.limiteDeteccaoVM import LimiteDeteccaoVM


class ConcentracaoVM:
    def __init__(self,
                sidebar_frame,
                result_frame,
                arquivo_frame,
                amostras_frame,
                dynamic_frame,
                mostrar_tela_inicial):

        self.sidebar_frame = sidebar_frame
        self.result_frame = result_frame
        self.arquivos_frame = arquivo_frame
        self.amostras_frame = amostras_frame
        self.dynamic_frame = dynamic_frame
        self.mostrar_tela_inicial = mostrar_tela_inicial
        self.botoes_criados = False

        # Variáveis para armazenar arquivos selecionados
        self.variaveis = Variaveis(sidebar_frame)
        self.arquivo_padrao = self.variaveis.lista_arquivo_padrao
        self.arquivos_amostras = self.variaveis.lista_arquivos
        self.resultado_limite = self.variaveis.resultado_limite

        # Chama os arquivos de service
        self.service = Service(sidebar_frame)

        # Chama o PadraoVM
        self.padrao_vm = PadraoVM(sidebar_frame, dynamic_frame, sidebar_frame)
        self.padrao_vm.padrao_view
        self.lista_padrao = self.padrao_vm.volta_padrao()

        # Chama os calculos de concentracao
        self.model = ConcentracaoModel()

        # Chama a view dos botoes de calcular
        self.view = ConcentracaoView(sidebar_frame)
        self.view.pack(fill="x", padx=10, pady=10)

        # Chama o resultado
        self.resultados_view = ConcentracaoResultadoView(self.result_frame)
        self.resultados_view.pack(padx=20, pady=20, fill="both", expand=True)

        # Chama o texto dos arquivos
        self.texto_arquivo_pd = AttArquivoSelecionado(self.arquivos_frame)
        self.texto_arquivo_pd.pack(fill="x", padx=10, pady=10)

        self.texto_arquivos_am = AttArquivoSelecionado(self.amostras_frame)
        self.texto_arquivos_am.pack(fill="x", padx=10, pady=10)

        # Chama a Exportacao
        self.export = ExportarVM(sidebar_frame, self.variaveis)
        #self.export.export

        # Chama os Graficos
        self.graficos = GraficosVM(sidebar_frame, self.variaveis)

        # Chama os Limite
        self.limite_deteccao = LimiteDeteccaoVM(sidebar_frame, self.service, self.variaveis)

    def botoes(self):
        if not self.botoes_criados:
        # impede recriação de botoes
        # Conectar os botões da View aos métodos da VM
            self.view.selecionar_arquivo_padrao.configure(command=self.padrao)
            self.view.selecionar_amostras.configure(command=self.amostras)
            self.view.calcular.configure(command=self.calcular)
            self.botoes_criados = True

    def padrao(self):
        arquivo = self.service.selecionar_arquivo_padrao()
        if arquivo:
            self.arquivo_padrao = arquivo
            self._verificar_pronto()
            # print("Arquivo de padrão selecionado:", self.arquivo_padrao)
            self.texto_arquivo_pd.atualizar(os.path.basename(self.arquivo_padrao))
        return self.arquivo_padrao

    def amostras(self):
        arquivos = list(self.service.selecionar_arquivos_amostras())
        if arquivos:
            self.arquivos_amostras = arquivos
            self._verificar_pronto()
            # print("Arquivos de amostras selecionadas:", self.arquivos_amostras)
            nomes_amostras = [os.path.basename(a) + "," for a in arquivos]
            self.texto_arquivos_am.atualizar(nomes_amostras)
        return self.arquivos_amostras

    def _verificar_pronto(self):
        """Habilita o botão Calcular quando tudo estiver selecionado."""
        if self.arquivos_amostras and self.arquivo_padrao:
            self.view.calcular.configure(state="normal")

    def calcular(self):
        self.c_padrao = self.padrao_vm.c_padrao_lista_selecionado()
        self.resultado = self.model.calcular_concentracoes(self.arquivos_amostras,
                                                           self.arquivo_padrao,
                                                           self.c_padrao)

        # Atualiza Variaveis global
        self.variaveis.resultados = self.resultado
        self.variaveis.lista_arquivos = self.arquivos_amostras
        self.variaveis.lista_arquivo_padrao = self.arquivo_padrao
        self.variaveis.c_padrao = self.c_padrao

        # Atualiza a instância dentro de ExportarVM
        self.export.arquivos_amostras = self.variaveis.lista_arquivos
        self.export.resultados = self.variaveis.resultados
        if self.resultado:
            self.export.habilita_exporta_excel()
            self.graficos.habilita_graficos()
            self.limite_deteccao.habilita_limite(self.arquivo_padrao, self.c_padrao)
        return self.resultados_view.mostrar_resultados(self.resultado[0])
