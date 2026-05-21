#!/bin/bash

# Script para iniciar o Frontend localmente

echo "🚀 Iniciando Frontend da Plataforma de Risco Climático"
echo "═════════════════════════════════════════════════════"

cd /Users/marcusvgo/Downloads/Capacitação/clima-risk-platform/frontend

# Instalar dependências se não existir
if [ ! -d "node_modules" ]; then
    echo "📦 Instalando dependências Node.js..."
    npm install
fi

echo ""
echo "✅ Frontend pronto para iniciar!"
echo "🌐 Acesse: http://localhost:3000"
echo ""
echo "Iniciando Next.js..."
echo ""

npm run dev
