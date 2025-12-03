.PHONY: help start stop restart logs clean install test health benchmark example advanced

help: ## Mostrar esta ayuda
	@echo "📚 Comandos disponibles para Weaviate:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

start: ## Iniciar Weaviate
	@echo "🚀 Iniciando Weaviate..."
	docker-compose up -d
	@echo "⏳ Esperando que los servicios estén listos..."
	@sleep 10
	@echo "✅ Weaviate iniciado en http://localhost:8080"

start-multilingual: ## Iniciar con modelo multiidioma
	@echo "🚀 Iniciando Weaviate con modelo multiidioma..."
	docker-compose -f docker-compose-multilingual.yml up -d
	@sleep 10
	@echo "✅ Weaviate iniciado con soporte multiidioma"

stop: ## Detener Weaviate
	@echo "🛑 Deteniendo Weaviate..."
	docker-compose down

restart: ## Reiniciar Weaviate
	@echo "🔄 Reiniciando Weaviate..."
	docker-compose restart

logs: ## Ver logs en tiempo real
	docker-compose logs -f

logs-weaviate: ## Ver solo logs de Weaviate
	docker-compose logs -f weaviate

logs-transformers: ## Ver solo logs del transformers
	docker-compose logs -f t2v-transformers

clean: ## Limpiar datos y contenedores
	@echo "🧹 Limpiando todo..."
	docker-compose down -v
	@echo "✅ Datos eliminados"

install: ## Instalar dependencias Python
	@echo "📦 Instalando dependencias..."
	pip install -r requirements.txt
	@echo "✅ Dependencias instaladas"

health: ## Verificar estado del sistema
	@./scripts/check_health.sh

example: ## Ejecutar ejemplo básico
	@echo "▶️  Ejecutando ejemplo básico..."
	python3 example.py

advanced: ## Ejecutar ejemplo avanzado
	@echo "▶️  Ejecutando ejemplo avanzado..."
	python3 advanced_example.py

benchmark: ## Ejecutar benchmark de rendimiento
	@echo "▶️  Ejecutando benchmark..."
	python3 benchmark.py

setup: start install ## Setup completo (iniciar + instalar)
	@echo ""
	@echo "✅ Setup completo!"
	@echo "   Ejecuta 'make example' para probar"

reset: ## Reiniciar desde cero
	@./scripts/reset_data.sh
