import os
from views.concentracaoView import ConcentracaoView, ConcentracaoResultadoView, AttArquivoSelecionado
from models.concentracaoModel import ConcentracaoModel
from models.propagacaoErrosModel import PropagacaoErrosModel
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
        self.erro_model = PropagacaoErrosModel()

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
            self.view.botao_limite.configure(command=self.limite_deteccao.calcula_resultado_limite, state="disabled")
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
        if not self.resultado:
            return
        self.concentracoes = self.resultado[0]
        self.areas_normalizadas = self.resultado[1]
        self.fatores_normalizacao = self.resultado[2]
        self.erros_normalizados = self.resultado[3]
        self.area_padrao = self.resultado[4]
        self.erro_padrao = self.resultado[5]



        # calcula propagação de erro
        self.erros_concentracao, self.unidade_padrao = self.erro_model.calcular(
            self.concentracoes,
            self.areas_normalizadas,
            self.erros_normalizados,
            self.c_padrao,
            self.area_padrao,
            self.erro_padrao
        )



        # Atualiza Variaveis global
        self.variaveis.lista_arquivos = self.arquivos_amostras
        self.variaveis.lista_arquivo_padrao = self.arquivo_padrao
        self.variaveis.c_padrao = self.c_padrao

        from models.arredondamentoModel import ArredondamentoModel
        self.arredondamento = ArredondamentoModel()
        self.arredondamento.atualizar_casas_padrao(self.c_padrao)
        self.export.exportar_model.arredondamento = self.arredondamento
        self.export.exportar_model.aba_resultados.arredondamento = self.arredondamento
        self.variaveis.resultados = self.resultado
        self.variaveis.erros_concentracao = self.erros_concentracao
        self.variaveis.unidade_padrao = self.unidade_padrao

        # Atualiza a instância dentro de ExportarVM
        self.export.arquivos_amostras = self.variaveis.lista_arquivos
        self.export.resultados = self.variaveis.resultados
        if self.resultado:
            self.export.habilita_exporta_excel()
            self.graficos.habilita_graficos()
            self.limite_deteccao.habilita_limite(self.arquivo_padrao, self.c_padrao)
            self.view.botao_limite.configure(state="normal")
        return self.resultados_view.mostrar_resultados(self.resultado[0])
