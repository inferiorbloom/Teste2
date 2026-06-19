import os
import sys
from pathlib import Path


def resource_path(*relative_parts: str) -> str:
    """Resolve caminhos de recursos tanto no desenvolvimento quanto no executável PyInstaller."""
    base = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parents[1]))
    return str(base.joinpath(*relative_parts))


def user_data_path(*relative_parts: str) -> str:
    """Retorna um local gravável pelo usuário para arquivos persistentes."""
    if os.name == 'nt':
        base = os.environ.get('APPDATA', os.path.expanduser('~'))
    else:
        base = os.path.expanduser('~/.local/share')

    app_dir = os.path.join(base, 'CXCalculator')
    os.makedirs(app_dir, exist_ok=True)

    if relative_parts:
        return os.path.join(app_dir, *relative_parts)
    return app_dir


def ensure_directory(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    return path
