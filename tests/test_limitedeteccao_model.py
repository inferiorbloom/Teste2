import os
import sys
import unittest

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from models.exportarModel import ExportarModel
from models.limitedeteccaoModel import LimiteDeteccaoModel
from models.arredondamentoModel import ArredondamentoModel


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

    def test_calcular_limite_deteccao_usa_area_e_concentracao_do_padrao(self):
        model = LimiteDeteccaoModel()

        arquivos_fullReport = {"padrao.pdf": {"Fe": 9.0}}
        areas_normalizadas = {"padrao": {("Fe", 6.4): 20.0}}
        concentracoes = {"bloco1": {"padrao": {("Fe", 6.4): "3.0"}}}
        c_padrao = {"elementos": {"Fe": {"valor": 10.0}}}
        area_padrao = {("Fe", 6.4): 50.0}

        ld_resultado = model.calcular_limite_deteccao(
            arquivos_fullReport,
            "padrao.txt",
            c_padrao,
            areas_normalizadas,
            concentracoes,
            area_padrao=area_padrao,
        )

        self.assertIn("padrao", ld_resultado)
        self.assertIn("Fe", ld_resultado["padrao"])
        self.assertAlmostEqual(ld_resultado["padrao"]["Fe"], 1.8)


class ArredondamentoModelTests(unittest.TestCase):
    def test_formatar_par_usa_casas_do_padrao(self):
        model = ArredondamentoModel()
        model.atualizar_casas_padrao({
            "elementos": {
                "Fe": {"valor": 1984.799, "valor_str": "1984.799"},
            }
        })

        valor, erro = model.formatar_par("1742.536", "48.132", "Fe")

        self.assertEqual(valor, 1743.0)
        self.assertEqual(erro, 48.0)

    def test_formatar_ld_usa_casas_do_padrao(self):
        model = ArredondamentoModel()
        model.atualizar_casas_padrao({
            "elementos": {
                "Fe": {"valor": 1985, "valor_str": "1985"},
            }
        })

        ld = model.formatar_ld(5.362352, "Fe")

        self.assertEqual(ld, 5)

    def test_formatar_par_usa_mesmas_casas_para_valor_e_erro(self):
        model = ArredondamentoModel()
        model.atualizar_casas_padrao({
            "elementos": {
                "Ca": {"valor": 3.128, "valor_str": "3.128"},
            }
        })

        valor, erro = model.formatar_par("2.415", "0.327", "Ca")

        self.assertEqual(valor, 2.42)
        self.assertEqual(erro, 0.33)


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
