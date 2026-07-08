import os
import sys
import unittest

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from models.exportarModel import ExportarModel
from models.limitedeteccaoModel import LimiteDeteccaoModel


class LimiteDeteccaoModelTests(unittest.TestCase):
    def test_calcular_limite_deteccao_works_with_tuple_keys(self):
        model = LimiteDeteccaoModel()

        arquivos_fullReport = {"amostra.pdf": {"Fe": 9.0}}
        areas_normalizadas = {"amostra": {("Fe", 6.4): 20.0}}
        concentracoes = {"bloco1": {"amostra": {("Fe", 6.4): "3.0"}}}

        ld_resultado = model.calcular_limite_deteccao(
            arquivos_fullReport,
            "padrao.txt",
            {},
            areas_normalizadas,
            concentracoes,
        )

        self.assertIn("amostra", ld_resultado)
        self.assertIn("Fe", ld_resultado["amostra"])
        self.assertAlmostEqual(ld_resultado["amostra"]["Fe"], 1.35)


class ExportarModelTests(unittest.TestCase):
    def test_normalizar_valores_para_excel_converte_strings_numericas(self):
        model = ExportarModel()
        df = pd.DataFrame({"valor": ["1.23", "-", "2.50"], "erro": ["0.01", "", "0.02"]})

        df_exportado = model._normalizar_valores_para_excel(df)

        self.assertEqual(df_exportado.loc[0, "valor"], 1.23)
        self.assertIsInstance(df_exportado.loc[0, "valor"], float)
        self.assertEqual(df_exportado.loc[1, "valor"], "-")
        self.assertEqual(df_exportado.loc[2, "erro"], 0.02)

    def test_buscar_ld_para_elemento_usa_nome_padrao_quando_existe(self):
        model = ExportarModel()

        ld_resultado = {"290426ab": {"Fe": 1.23}}

        self.assertEqual(model._buscar_ld_para_elemento(ld_resultado, "290426ab", "Fe"), 1.23)

    def test_buscar_ld_para_elemento_faz_fallback_para_primeiro_ld_disponivel(self):
        model = ExportarModel()

        ld_resultado = {"290426ak": {"Fe": 4.56}}

        self.assertEqual(model._buscar_ld_para_elemento(ld_resultado, "290426ab", "Fe"), 4.56)


if __name__ == "__main__":
    unittest.main()
