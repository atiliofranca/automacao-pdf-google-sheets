@echo off
echo ========================================
echo   GERADOR DE EXECUTÁVEL PORTÁVEL
echo   Extrator de Orçamentos Makino
echo ========================================
echo.

echo 1. Ativando ambiente virtual...
call venv\Scripts\activate

echo.
echo 2. Instalando PyInstaller...
pip install pyinstaller

echo.
echo 3. Gerando executável portável...
pyinstaller extrator_simples.spec --clean --noconfirm

echo.
echo 4. Copiando arquivos necessários...
if not exist "dist\Extrator_Orcamentos_Makino" mkdir "dist\Extrator_Orcamentos_Makino"
copy "planilha-python-472618-f3c9ba25d174.json" "dist\Extrator_Orcamentos_Makino\"
copy "ícone.png" "dist\Extrator_Orcamentos_Makino\"

echo.
echo ========================================
echo   EXECUTÁVEL CRIADO COM SUCESSO!
echo ========================================
echo.
echo O executável está em: dist\Extrator_Orcamentos_Makino\
echo Arquivo: Extrator_Orcamentos_Makino.exe
echo.
echo Para usar:
echo 1. Copie a pasta 'Extrator_Orcamentos_Makino' para onde quiser
echo 2. Execute o arquivo .exe
echo 3. O arquivo de credenciais deve estar na mesma pasta
echo.
pause
