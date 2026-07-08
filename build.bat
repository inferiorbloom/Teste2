@echo off
setlocal

set ROOT=%~dp0
set PYTHON=%ROOT%.venv\Scripts\python.exe

if not exist "%PYTHON%" (
    echo Python virtual environment not found.
    exit /b 1
)

"%PYTHON%" -m PyInstaller --noconfirm --clean calculadora.spec

echo.
echo Build concluido.
echo Executavel gerado em: %ROOT%dist\CalculadoraConcentracoes\CalculadoraConcentracoes.exe
endlocal
