from models.limiteDeteccaoModel import LimiteDeteccaoModel


class LimiteDeteccaoVM:
    def __init__(self, service, variaveis):

        self.service = service
        self.variaveis = variaveis

        self.limitedeteccao_model = LimiteDeteccaoModel()

    def calcula_resultado_limite(self):
        self.arquivos_fullReport = self.service.selecionar_arquivos_fullReport()
        self.resultado_limite = self.limitedeteccao_model.calcular_limite_deteccao(self.arquivos_fullReport)
        self.variaveis.resultado_limite = self.resultado_limite
        return self.variaveis.resultado_limite
