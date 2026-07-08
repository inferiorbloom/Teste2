import json
import os

CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".cx_calculator_config.json")
CHAVE_ULTIMO_DIRETORIO = "ultimo_diretorio"


def carregar_ultimo_diretorio():
    """Carrega o último diretório utilizado a partir do arquivo de configuração."""
    if not os.path.exists(CONFIG_FILE):
        return None

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except (OSError, json.JSONDecodeError):
        return None

    return dados.get(CHAVE_ULTIMO_DIRETORIO)


def salvar_ultimo_diretorio(caminho):
    """Salva o último diretório utilizado no arquivo de configuração."""
    if not caminho:
        return

    if os.path.isfile(caminho):
        diretorio = os.path.dirname(caminho)
    else:
        diretorio = caminho

    diretorio = os.path.abspath(os.path.expanduser(diretorio))

    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)

    with open(CONFIG_FILE, "w", encoding="utf-8") as arquivo:
        json.dump({CHAVE_ULTIMO_DIRETORIO: diretorio}, arquivo, ensure_ascii=False, indent=2)
