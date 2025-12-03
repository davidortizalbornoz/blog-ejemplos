#!/bin/bash
# Script de inicio rápido para Weaviate

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║       🚀 Weaviate Local - Inicio Automático               ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Función para verificar si Docker está corriendo
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        echo "❌ Error: Docker no está corriendo"
        echo "   Por favor inicia Docker Desktop primero"
        exit 1
    fi
}

# Función para verificar si Weaviate está respondiendo
wait_for_weaviate() {
    echo "⏳ Esperando que Weaviate esté listo..."
    local max_attempts=30
    local attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        if curl -s http://localhost:8080/v1/meta > /dev/null 2>&1; then
            echo "✅ Weaviate está listo!"
            return 0
        fi
        
        attempt=$((attempt + 1))
        echo "   Intento $attempt/$max_attempts..."
        sleep 2
    done
    
    echo "❌ Timeout: Weaviate no responde"
    echo "   Verifica los logs: docker-compose logs weaviate"
    return 1
}

# Verificar Docker
check_docker

# Detener contenedores existentes
echo "🛑 Deteniendo contenedores existentes..."
docker-compose down > /dev/null 2>&1 || true

# Iniciar servicios
echo "🚀 Iniciando Weaviate y text2vec-transformers..."
docker-compose up -d

# Esperar a que esté listo
if wait_for_weaviate; then
    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║                    ✅ ¡Listo para usar!                    ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
    echo "🌐 Endpoints disponibles:"
    echo "   • API REST:    http://localhost:8080/v1"
    echo "   • GraphQL:     http://localhost:8080/v1/graphql"
    echo "   • Health:      http://localhost:8080/v1/.well-known/ready"
    echo ""
    echo "📚 Próximos pasos:"
    echo "   1. Instalar cliente:  pip install -r requirements.txt"
    echo "   2. Ejecutar ejemplo:  python3 example.py"
    echo "   3. Ejemplo avanzado:  python3 advanced_example.py"
    echo "   4. Benchmark:         python3 benchmark.py"
    echo ""
    echo "🔧 Comandos útiles:"
    echo "   • Ver logs:           docker-compose logs -f"
    echo "   • Detener:            docker-compose down"
    echo "   • Ver ayuda:          make help"
    echo ""
    echo "📖 Documentación completa en README.md"
    echo ""
else
    echo ""
    echo "⚠️  Weaviate no pudo iniciarse correctamente"
    echo ""
    echo "🔍 Para diagnosticar:"
    echo "   docker-compose logs weaviate"
    echo "   docker-compose logs t2v-transformers"
    exit 1
fi
