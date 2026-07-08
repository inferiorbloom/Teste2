import math


class ArredondamentoModel:
    """Centraliza o arredondamento usado na exportação e nos resultados."""

    def __init__(self):
        self.casas_padrao = {}

    def _obter_casas_elemento(self, elemento):
        if not elemento:
            return 0

        casas = self.casas_padrao.get(elemento)
        if casas is None:
            return 0
        return int(casas)

    def atualizar_casas_padrao(self, c_padrao):
        if not isinstance(c_padrao, dict):
            self.casas_padrao = {}
            return

        elementos = c_padrao.get("elementos") or {}
        casas = {}

        for elemento, dados in elementos.items():
            if not isinstance(dados, dict):
                continue

            valor = dados.get("valor")
            if valor in [None, ""]:
                continue

            try:
                valor_num = float(valor)
            except (TypeError, ValueError):
                continue

            texto = str(dados.get("valor_str") or valor).strip()
            if "." in texto:
                casas_elemento = len(texto.split(".")[1].rstrip("0"))
            else:
                casas_elemento = 0

            casas[elemento] = max(0, casas_elemento)

        self.casas_padrao = casas

    def _obter_precisao_maxima(self, elemento=None, precisao_padrao=None):
        if precisao_padrao is not None:
            return int(precisao_padrao)
        if not elemento:
            return 0
        return self._obter_casas_elemento(elemento)

    def _calcular_casas_para_erro(self, erro, precisao_maxima):
        if erro is None or erro == "":
            return 0

        try:
            erro_num = float(erro)
        except (TypeError, ValueError):
            return 0

        if erro_num == 0:
            return 0

        abs_erro = abs(erro_num)
        if abs_erro >= 10:
            casas = 0
        else:
            casas = max(0, int(2 - 1 - math.floor(math.log10(abs_erro))))

        if precisao_maxima is not None:
            casas = min(casas, int(precisao_maxima))

        return casas

    def formatar_resultado(self, valor, erro, elemento=None, precisao_padrao=None):
        if valor is None or valor == "":
            return valor, erro, 0

        try:
            valor_num = float(valor)
            erro_num = float(erro) if erro not in ["", None] else None
        except (TypeError, ValueError):
            return valor, erro, 0

        if erro_num is None:
            return valor, erro, 0

        precisao_maxima = self._obter_precisao_maxima(elemento, precisao_padrao)
        casas_erro = self._calcular_casas_para_erro(erro_num, precisao_maxima)

        valor_fmt = round(valor_num, casas_erro)
        erro_fmt = round(erro_num, casas_erro)

        return valor_fmt, erro_fmt, casas_erro

    def formatar_valor_erro(self, valor, erro, elemento=None):
        valor_fmt, erro_fmt, _ = self.formatar_resultado(valor, erro, elemento)
        return valor_fmt, erro_fmt

    def formatar_ld(self, ld, elemento=None):
        if ld is None or ld == "":
            return ld

        try:
            ld_num = float(ld)
        except (TypeError, ValueError):
            return ld

        precisao_maxima = self._obter_precisao_maxima(elemento)
        if precisao_maxima is None:
            precisao_maxima = 0

        casas = max(0, int(precisao_maxima))
        return round(ld_num, casas)

    def formatar_par(self, valor, erro, elemento=None):
        """Formata valor e erro usando o erro como base para a precisão."""
        valor_fmt, erro_fmt, _ = self.formatar_resultado(valor, erro, elemento)
        return valor_fmt, erro_fmt
