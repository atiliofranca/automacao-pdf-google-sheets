@echo off
REM Script de inicialização para Windows

echo Iniciando Extrator de Orçamentos PDF...
echo.

REM Ativar ambiente virtual se existir
if exist "venv\Scripts\activate.bat" (
    echo Ativando ambiente virtual...
    call venv\Scripts\activate.bat
    echo.
)

REM Executar o extrator
python extrator_simples.py

REM Pausar para ver mensagens de erro se houver
if errorlevel 1 (
    echo.
    echo Erro ao executar o extrator!
    pause
)
