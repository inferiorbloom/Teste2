import importlib
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from models import configModel


class ConfigModelTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        configModel.CONFIG_FILE = os.path.join(self.temp_dir.name, "config.json")
        if os.path.exists(configModel.CONFIG_FILE):
            os.remove(configModel.CONFIG_FILE)

    def test_carregar_ultimo_diretorio_retorna_none_quando_nao_existe(self):
        self.assertIsNone(configModel.carregar_ultimo_diretorio())

    def test_salvar_e_carregar_ultimo_diretorio(self):
        configModel.salvar_ultimo_diretorio("C:/Dados/FRX/Padrões")

        self.assertEqual(
            configModel.carregar_ultimo_diretorio(),
            os.path.normpath("C:/Dados/FRX/Padrões"),
        )


if __name__ == "__main__":
    unittest.main()
