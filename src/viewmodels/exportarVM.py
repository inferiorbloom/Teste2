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
        # Obtem as variáveis atualizadas no fluxo principal
        arquivo_padrao = self.variaveis.lista_arquivo_padrao

        


        arquivos_amostras = self.variaveis.lista_arquivos
        resultados = self.variaveis.resultados or []
        concentracoes = resultados[0] if len(resultados) > 0 else {}
        areas_normalizadas = resultados[1] if len(resultados) > 1 else {}
        fatores_normalizacao = resultados[2] if len(resultados) > 2 else {}
        erros_normalizados = resultados[3] if len(resultados) > 3 else {}

        erros_propagados = getattr(self.variaveis, "erros_concentracao", {}) or {}
        unidade_padrao = getattr(self.variaveis, "unidade_padrao", {}) or {}
        ld_resultado = getattr(self.variaveis, "resultado_limite", {}) or {}

        self.exporta_excel_var = self.exportar_model.exportar_para_excel(
            arquivos_amostras,
            concentracoes,
            areas_normalizadas,
            fatores_normalizacao,
            erros_normalizados,
            erros_propagados,
            ld_resultado,
            unidade_padrao,
            arquivo_padrao,
        )
        return self.exporta_excel_var
