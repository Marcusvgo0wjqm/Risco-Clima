#!/bin/bash

# Script para iniciar tudo com Docker

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║   🚀 Iniciando Plataforma de Risco Climático com Docker       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Verificar se Docker está rodando
if ! docker ps &> /dev/null; then
    echo "❌ Docker Desktop não está rodando!"
    echo ""
    echo "📍 Abra o Docker Desktop:"
    echo "   1. Finder → Aplicativos → Docker.app"
    echo "   2. Aguarde o Docker iniciar (ícone no menu de cima)"
    echo "   3. Tente novamente"
    echo ""
    exit 1
fi

echo "✅ Docker está rodando!"
echo ""

# Ir para a pasta do projeto
cd /Users/marcusvgo/Downloads/Capacitação/clima-risk-platform

echo "📁 Pasta do projeto: $(pwd)"
echo ""

# Iniciar Docker Compose
echo "🐳 Iniciando Docker Compose..."
echo ""
echo "Aguarde 2-3 minutos para os serviços iniciarem..."
echo ""
echo "Quando ver estas mensagens, está pronto:"
echo "  ✅ postgres | database system is ready to accept connections"
echo "  ✅ redis    | Ready to accept connections"
echo "  ✅ backend  | Uvicorn running on http://0.0.0.0:8000"
echo "  ✅ frontend | ready - started server on 0.0.0.0:3000"
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo ""

docker-compose up

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "🎉 Plataforma iniciada!"
echo ""
echo "Acesse no Safari:"
echo "  🌐 Frontend:  http://localhost:3000"
echo "  🔧 Backend:   http://localhost:8000"
echo "  📚 Docs:      http://localhost:8000/docs"
echo ""
