import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from models.exportarModel import ExportarModel
from models.arredondamentoModel import ArredondamentoModel


class ExportarModelTests(unittest.TestCase):
    def test_buscar_ld_para_elemento_usa_o_nome_do_arquivo_padrao(self):
        model = ExportarModel()
        ld_resultado = {
            "outro_padrao": {"Fe": 0.111},
            "290426ab": {"Fe": 1.234},
        }

        self.assertEqual(model._buscar_ld_para_elemento(ld_resultado, "290426ab.txt", "Fe"), 1.234)

    def test_formatar_resultado_retorna_float(self):
        model = ArredondamentoModel()
        valor, erro, casas = model.formatar_resultado(20.0, 0.1, "Fe")

        self.assertIsInstance(valor, float)
        self.assertIsInstance(erro, float)
        self.assertEqual(casas, 0)


if __name__ == "__main__":
    unittest.main()
