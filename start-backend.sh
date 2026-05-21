#!/bin/bash

# Script para iniciar o Backend localmente

echo "🚀 Iniciando Backend da Plataforma de Risco Climático"
echo "═════════════════════════════════════════════════════"

cd /Users/marcusvgo/Downloads/Capacitação/clima-risk-platform/backend

# Criar venv se não existir
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar venv
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências se não existir
if [ ! -f "venv/pyvenv.cfg" ]; then
    echo "📚 Instalando dependências..."
    pip install -r requirements.txt
fi

# Iniciar servidor
echo ""
echo "✅ Backend pronto para iniciar!"
echo "🌐 Acesse: http://localhost:8000"
echo "📚 Docs: http://localhost:8000/docs"
echo ""
echo "Iniciando Uvicorn..."
echo ""

uvicorn app.main:app --reload
