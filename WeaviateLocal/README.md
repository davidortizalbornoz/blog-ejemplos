# Weaviate Local - Vector Database

Configuración completa de Weaviate con vectorización local usando `text2vec-transformers`.

## 🚀 Características

- **Base de datos vectorial**: Weaviate 1.35.0
- **Vectorizador local**: sentence-transformers (sin APIs externas)
- **Modelo**: all-MiniLM-L6-v2 (384 dimensiones)
- **Persistencia**: Los datos se guardan en volumen Docker
- **Sin costos**: Todo corre localmente

## 📋 Requisitos

- Docker & Docker Compose
- 4GB+ RAM disponible
- Python 3.8+ (para cliente de ejemplo)

## 🔧 Instalación

### 1. Iniciar Weaviate

```bash
docker-compose up -d
```

### 2. Verificar que los servicios están corriendo

```bash
docker-compose ps
```

Deberías ver:
- `weaviate` corriendo en puerto 8080
- `weaviate-transformers` corriendo

### 3. Verificar logs

```bash
# Ver logs de Weaviate
docker-compose logs -f weaviate

# Ver logs del transformers
docker-compose logs -f t2v-transformers
```

### 4. Probar la conexión

```bash
curl http://localhost:8080/v1/meta
```

## 📦 Instalar Cliente Python

```bash
pip install weaviate-client
```

## 🎯 Uso Básico

Ver archivo `example.py` para ejemplos completos.

### Conectar al servidor

```python
import weaviate

client = weaviate.Client("http://localhost:8080")
print(client.is_ready())  # True si está funcionando
```

### Crear un schema

```python
schema = {
    "classes": [{
        "class": "Document",
        "description": "Documentos con vectorización automática",
        "vectorizer": "text2vec-transformers",
        "moduleConfig": {
            "text2vec-transformers": {
                "vectorizeClassName": False
            }
        },
        "properties": [
            {
                "name": "title",
                "dataType": ["text"],
                "description": "Título del documento"
            },
            {
                "name": "content",
                "dataType": ["text"],
                "description": "Contenido del documento"
            }
        ]
    }]
}

client.schema.create(schema)
```

### Insertar datos

```python
# Los vectores se generan automáticamente
client.data_object.create(
    {
        "title": "Introducción a Python",
        "content": "Python es un lenguaje de programación interpretado..."
    },
    "Document"
)
```

### Búsqueda semántica (KNN)

```python
result = client.query.get("Document", ["title", "content"]) \
    .with_near_text({"concepts": ["lenguaje de programación"]}) \
    .with_limit(5) \
    .do()

print(result)
```

## 🔄 Comandos Útiles

### Detener servicios
```bash
docker-compose down
```

### Detener y eliminar datos
```bash
docker-compose down -v
```

### Ver logs en tiempo real
```bash
docker-compose logs -f
```

### Reiniciar servicios
```bash
docker-compose restart
```

## 🎨 Modelos Disponibles

Para cambiar el modelo, edita en `docker-compose.yml`:

```yaml
t2v-transformers:
  image: semitechnologies/transformers-inference:MODELO
```

### Modelos recomendados:

| Modelo | Dimensiones | Uso | Velocidad |
|--------|-------------|-----|-----------|
| `sentence-transformers-all-MiniLM-L6-v2` | 384 | General, rápido | ⚡⚡⚡ |
| `sentence-transformers-all-mpnet-base-v2` | 768 | Mayor calidad | ⚡⚡ |
| `sentence-transformers-paraphrase-multilingual-MiniLM-L12-v2` | 384 | Multiidioma | ⚡⚡ |
| `sentence-transformers-multi-qa-MiniLM-L6-cos-v1` | 384 | Q&A | ⚡⚡⚡ |

## 🌐 Interfaces Web

- **API REST**: http://localhost:8080/v1
- **GraphQL**: http://localhost:8080/v1/graphql
- **Meta info**: http://localhost:8080/v1/meta

## 🐛 Troubleshooting

### El servicio no inicia
```bash
# Ver logs detallados
docker-compose logs weaviate
docker-compose logs t2v-transformers
```

### Puerto 8080 ocupado
Cambia el puerto en `docker-compose.yml`:
```yaml
ports:
  - "8081:8080"  # Usar puerto 8081
```

### Falta memoria
Reduce recursos o usa un modelo más pequeño (MiniLM-L6-v2).

## 📊 Monitoreo

### Ver estadísticas
```bash
curl http://localhost:8080/v1/nodes
```

### Ver schemas
```bash
curl http://localhost:8080/v1/schema
```

## 🔒 Seguridad (Producción)

Para producción, habilita autenticación:

```yaml
environment:
  AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: 'false'
  AUTHENTICATION_APIKEY_ENABLED: 'true'
  AUTHENTICATION_APIKEY_ALLOWED_KEYS: 'tu-api-key-segura'
```

## 📚 Recursos

- [Documentación Weaviate](https://weaviate.io/developers/weaviate)
- [Modelos Sentence Transformers](https://www.sbert.net/docs/pretrained_models.html)
- [API Reference](https://weaviate.io/developers/weaviate/api/rest)
