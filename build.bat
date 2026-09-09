@echo off
chcp 65001 > nul
echo ============================================================
echo   Gerador do Executavel (.exe) - API de Produtos
echo ============================================================
echo.
echo 1. Instalando dependencias e PyInstaller...
python -m pip install -r requirements.txt
python -m pip install pyinstaller

echo.
echo 2. Limpando pastas temporarias antigas...
if exist build rd /s /q build
if exist *.spec del /f /q *.spec

echo.
echo 3. Compilando o executavel standalone...
python -m PyInstaller --onefile --name servidor_produtos --collect-all uvicorn --collect-all fastapi --collect-all starlette --collect-all pydantic main.py

echo.
echo ============================================================
echo  ✅ SUCESSO! O executavel esta disponivel em:
echo     dist\servidor_produtos.exe
echo ============================================================
echo.
pause
