class AbaConcentracoesModel:
    """Monta o DataFrame usado na aba 'Concentrações' (só a coluna 'C' de cada elemento)."""

    def montar(self, df_analise):
        """
        Recebe o df_analise (já montado pelo AbaResultadosModel) e extrai só
        os valores de concentração.

        ATENÇÃO: igual ao código original, isso assume que df_analise tem
        colunas MultiIndex (nome_coluna, "C"/"Erro"). Se df_analise vier vazio
        (nenhuma amostra com concentração), o .xs() abaixo pode estourar erro
        — esse é um comportamento herdado do exportarModel.py original e não
        foi alterado nesta divisão. Vale revisar isso quando formos mexer
        de fato nos bugs da exportação.
        """
        df_concentracoes = df_analise.xs("C", axis=1, level=1)
        df_concentracoes.columns.name = None

        df_concentracoes = df_concentracoes.replace(r'^\s*$', '-', regex=True).fillna('-')

        return df_concentracoes
