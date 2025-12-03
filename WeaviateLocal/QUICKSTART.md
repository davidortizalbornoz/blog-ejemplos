# 🚀 Inicio Rápido - Weaviate Local

## Setup en 3 Pasos

### 1️⃣ Iniciar Weaviate

```bash
cd /workspace/WeaviateLocal
docker-compose up -d
```

Espera ~30 segundos para que los servicios estén listos.

### 2️⃣ Instalar Cliente Python

```bash
pip install -r requirements.txt
```

### 3️⃣ Ejecutar Ejemplo

```bash
python3 example.py
```

## ✅ Verificar que Todo Funciona

```bash
# Opción 1: Verificar servicios
docker-compose ps

# Opción 2: Verificar API
curl http://localhost:8080/v1/meta

# Opción 3: Usar script de salud
./scripts/check_health.sh
```

## 📚 Ejemplos Disponibles

### Ejemplo Básico
```bash
python3 example.py
```
Demuestra:
- Conexión a Weaviate
- Creación de schema
- Inserción de documentos
- Búsqueda semántica (KNN)
- Filtros y agregaciones

### Ejemplo Avanzado
```bash
python3 advanced_example.py
```
Demuestra:
- Schemas con referencias cruzadas
- Búsquedas con filtros múltiples
- Búsqueda híbrida (vectorial + keyword)
- Agregaciones y estadísticas
- Joins entre clases

## 🎨 Cambiar Modelo de Embeddings

Edita `docker-compose.yml` y cambia:

```yaml
t2v-transformers:
  image: semitechnologies/transformers-inference:MODELO
```

### Modelos disponibles:
- `sentence-transformers-all-MiniLM-L6-v2` ⚡⚡⚡ (actual)
- `sentence-transformers-all-mpnet-base-v2` ⚡⚡ (mejor calidad)
- `sentence-transformers-paraphrase-multilingual-MiniLM-L12-v2` (multiidioma)
- `sentence-transformers-multi-qa-MiniLM-L6-cos-v1` (Q&A)

Luego reinicia:
```bash
docker-compose down
docker-compose up -d
```

## 🧹 Limpiar y Reiniciar

```bash
# Detener servicios
docker-compose down

# Limpiar datos y reiniciar
./scripts/reset_data.sh
```

## 🌐 Interfaces

- **API REST**: http://localhost:8080/v1
- **GraphQL**: http://localhost:8080/v1/graphql
- **Health**: http://localhost:8080/v1/.well-known/ready
- **Meta Info**: http://localhost:8080/v1/meta

## 📖 Consultas Rápidas con curl

### Ver schema
```bash
curl http://localhost:8080/v1/schema | python3 -m json.tool
```

### Contar objetos
```bash
curl http://localhost:8080/v1/objects | python3 -m json.tool
```

### Buscar (GraphQL)
```bash
curl -X POST http://localhost:8080/v1/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{
      Get {
        Document(limit: 3) {
          title
          content
        }
      }
    }"
  }' | python3 -m json.tool
```

## ❓ Troubleshooting

### Puerto ocupado
```bash
# Cambiar puerto en docker-compose.yml
ports:
  - "8081:8080"  # Usar 8081 en lugar de 8080
```

### Contenedor no inicia
```bash
# Ver logs
docker-compose logs -f weaviate
docker-compose logs -f t2v-transformers
```

### Limpiar todo y empezar de nuevo
```bash
docker-compose down -v
docker system prune -f
docker-compose up -d
```

## 💡 Tips

- Los vectores se generan **automáticamente** al insertar datos
- No necesitas calcular embeddings manualmente
- La búsqueda semántica funciona con texto en lenguaje natural
- Los datos persisten en volumen Docker entre reinicios
- Puedes tener múltiples modelos para diferentes clases

## 📚 Más Información

- [README.md](README.md) - Documentación completa
- [Weaviate Docs](https://weaviate.io/developers/weaviate)
- [Python Client](https://weaviate.io/developers/weaviate/client-libraries/python)
