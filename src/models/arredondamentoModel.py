import math
import numpy as np


class ArredondamentoModel:
    """
    Centraliza todo o arredondamento usado na exportação.
    A lógica aqui é uma cópia fiel do que existia dentro de exportarModel.py,
    apenas reorganizada em um único lugar.
    """

    def formatar_valor_erro(self, valor, erro):
        if erro is None or erro == 0:
            return valor, erro

        ordem = math.floor(math.log10(abs(erro)))
        sig = 2
        if ordem < 0:
            casas = -(ordem - (sig - 1))
            erro_arred = np.round(erro, casas)
            valor_arred = np.round(valor, casas)
        elif ordem >= 0:
            erro_arred = np.round(erro)
            valor_arred = np.round(valor)

        return valor_arred, erro_arred

    def formatar_ld(self, ld):
        if ld is None or ld == "":
            return ld

        try:
            ld = float(ld)
        except:
            return ld

        if ld == 0:
            return 0

        ordem = math.floor(math.log10(abs(ld)))
        primeira = ld / (10 ** ordem)

        # mesma lógica do erro
        if primeira < 3:
            sig = 2
        else:
            sig = 1

        casas = -(ordem - (sig - 1))

        return round(ld, casas)

    def formatar_par(self, valor, erro):
        """
        Recebe o par (valor, erro) de um elemento na aba "Resultados" e devolve
        (valor_final, erro_final) já prontos para ir na célula do Excel.

        IMPORTANTE: assume que `valor` já foi checado como não vazio pelo
        chamador (mesmo comportamento do código original: se valor == "",
        a célula simplesmente não é preenchida).

        Reproduz exatamente o procedimento que estava dentro do loop de
        `exportar_para_excel` no exportarModel.py original.
        """
        try:
            valor_num = float(valor)
            erro_existe = erro not in ["", None]

            if erro_existe:
                erro_num = float(erro)
            else:
                erro_num = None

            # Se não tem erro ou erro = 0 → NÃO arredonda
            if erro_existe:
                valor_fmt, erro_fmt = self.formatar_valor_erro(valor_num, erro_num)

                if isinstance(valor_fmt, (int, float)) and isinstance(erro_fmt, (int, float)):

                    if erro_fmt != 0:
                        ordem = math.floor(math.log10(abs(erro_fmt)))
                        primeira = erro_fmt / (10 ** ordem)
                        sig = 2 if primeira < 3 else 1
                        casas = max(0, -(ordem - (sig - 1)))
                    else:
                        casas = 0

                    valor_str = f"{valor_fmt:.{casas}f}"
                    erro_str = f"{erro_fmt:.{casas}f}"

                    return valor_str, erro_str

                return valor_fmt, erro_fmt

            valor_fmt = round(valor_num)  # arredondamento simples
            return valor_fmt, ""

        except Exception:
            return valor, erro
