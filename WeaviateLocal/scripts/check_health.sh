#!/bin/bash
# Script para verificar el estado de Weaviate

echo "🔍 Verificando estado de Weaviate..."
echo ""

# Verificar contenedores
echo "📦 Estado de contenedores:"
docker-compose ps
echo ""

# Verificar conectividad
echo "🌐 Verificando conectividad..."
if curl -s http://localhost:8080/v1/meta > /dev/null; then
    echo "✅ Weaviate está respondiendo"
    echo ""
    
    # Mostrar información del cluster
    echo "ℹ️  Información del cluster:"
    curl -s http://localhost:8080/v1/meta | python3 -m json.tool
    echo ""
    
    # Mostrar schema
    echo "📋 Schema actual:"
    curl -s http://localhost:8080/v1/schema | python3 -m json.tool
    
else
    echo "❌ Weaviate no está respondiendo"
    echo "   Verifica los logs con: docker-compose logs weaviate"
fi
