#!/bin/bash
# Script para reiniciar Weaviate y limpiar todos los datos

echo "⚠️  ADVERTENCIA: Esto eliminará todos los datos de Weaviate"
read -p "¿Estás seguro? (yes/no): " confirm

if [ "$confirm" = "yes" ]; then
    echo "🗑️  Deteniendo servicios..."
    docker-compose down -v
    
    echo "🧹 Limpiando volúmenes..."
    docker volume prune -f
    
    echo "🚀 Iniciando servicios frescos..."
    docker-compose up -d
    
    echo "⏳ Esperando que Weaviate esté listo..."
    sleep 10
    
    echo "✅ Weaviate reiniciado y limpio"
    echo "   Puedes ejecutar: python3 example.py"
else
    echo "❌ Operación cancelada"
fi
