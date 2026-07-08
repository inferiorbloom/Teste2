import pandas as pd


class AbaConcentracoesModel:
    """Monta o DataFrame usado na aba 'Concentrações' (só a coluna 'C' de cada elemento)."""

    def montar(self, df_analise):
        """
        Recebe o df_analise (já montado pelo AbaResultadosModel) e extrai só
        os valores de concentração.
        """
        if df_analise is None or df_analise.empty:
            return pd.DataFrame()

        df_concentracoes = df_analise.xs("C", axis=1, level=1)
        df_concentracoes.columns.name = None

        return df_concentracoes
