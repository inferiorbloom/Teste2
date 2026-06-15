import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

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


if __name__ == "__main__":
    unittest.main()
