#!/usr/bin/env bash
set -e

# Garante que os caminhos de binários locais do usuário estejam no PATH
export PATH="$HOME/.local/bin:$PATH"

echo "============================================================"
echo "  Gerador de Executável Standalone - API de Produtos"
echo "============================================================"
echo ""

# Identifica o executável do Python
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Erro: Python não foi encontrado no sistema."
    exit 1
fi

# Define o executor do pip
if [ -f "$HOME/.local/bin/pip" ]; then
    PIP_CMD="$HOME/.local/bin/pip"
elif command -v pip3 &>/dev/null; then
    PIP_CMD="pip3"
elif command -v pip &>/dev/null; then
    PIP_CMD="pip"
else
    PIP_CMD="$PYTHON_CMD -m pip"
fi

echo "1. Instalando dependências e PyInstaller..."
$PIP_CMD install --user --break-system-packages -r requirements.txt 2>/dev/null || $PIP_CMD install -r requirements.txt

echo ""
echo "2. Limpando pastas temporárias antigas..."
rm -rf build *.spec

echo ""
echo "3. Compilando o executável standalone..."
$PYTHON_CMD -m PyInstaller --onefile --name servidor_produtos \
    --collect-all uvicorn \
    --collect-all fastapi \
    --collect-all starlette \
    --collect-all pydantic \
    main.py

echo ""
echo "============================================================"
echo " ✅ SUCESSO! O executável está disponível em:"
echo "    dist/servidor_produtos"
echo "============================================================"
