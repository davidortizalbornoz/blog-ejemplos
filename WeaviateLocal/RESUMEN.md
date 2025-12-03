# 📦 Weaviate Local - Resumen del Proyecto

## ✅ Lo que has recibido

Un setup completo y funcional de **Weaviate** con vectorización local usando **text2vec-transformers**.

### 📁 Estructura del Proyecto

```
WeaviateLocal/
├── docker-compose.yml                    # Configuración principal
├── docker-compose-multilingual.yml      # Configuración con modelo multiidioma
├── requirements.txt                      # Dependencias Python
├── Makefile                             # Comandos útiles
│
├── README.md                            # Documentación completa
├── QUICKSTART.md                        # Inicio rápido
├── RESUMEN.md                           # Este archivo
│
├── example.py                           # ⭐ Ejemplo básico
├── advanced_example.py                  # ⭐ Ejemplo avanzado
├── benchmark.py                         # ⭐ Pruebas de rendimiento
│
└── scripts/
    ├── check_health.sh                  # Verificar estado
    └── reset_data.sh                    # Reiniciar todo
```

---

## 🚀 Inicio Rápido (3 comandos)

```bash
# 1. Iniciar Weaviate
make start

# 2. Instalar cliente Python
make install

# 3. Ejecutar ejemplo
make example
```

**O manualmente:**
```bash
docker-compose up -d
pip install -r requirements.txt
python3 example.py
```

---

## 🎯 Características Principales

### ✅ **Sin APIs Externas**
- No necesitas API keys (OpenAI, Cohere, etc.)
- Todo corre 100% local
- Sin costos de uso
- Total privacidad de datos

### ✅ **Vectorización Automática**
- Modelo: `sentence-transformers/all-MiniLM-L6-v2`
- 384 dimensiones
- No necesitas calcular embeddings manualmente
- Solo insertas texto y Weaviate hace el resto

### ✅ **Imagen ARM64 Específica**
- `semitechnologies/weaviate:1.35.0-dev-4431468.arm64`
- Optimizada para arquitectura ARM
- Compatible con Mac M1/M2/M3, Raspberry Pi, etc.

### ✅ **Persistencia de Datos**
- Los datos se guardan en volumen Docker
- Sobreviven a reinicios
- Fácil backup

---

## 📚 Ejemplos Incluidos

### 1. **example.py** - Ejemplo Básico
Aprende lo fundamental:
- ✓ Conectar a Weaviate
- ✓ Crear schemas
- ✓ Insertar datos con vectorización automática
- ✓ Búsqueda semántica (KNN)
- ✓ Filtros y agregaciones

**Ejecutar:**
```bash
make example
# o
python3 example.py
```

### 2. **advanced_example.py** - Ejemplo Avanzado
Features complejas:
- ✓ Schemas con referencias cruzadas
- ✓ Búsquedas con filtros múltiples
- ✓ Búsqueda híbrida (vectorial + keyword)
- ✓ Agregaciones y estadísticas
- ✓ Joins entre clases

**Ejecutar:**
```bash
make advanced
# o
python3 advanced_example.py
```

### 3. **benchmark.py** - Pruebas de Rendimiento
Mide el desempeño:
- ✓ Velocidad de inserción (objetos/segundo)
- ✓ Latencia de búsqueda (P50, P95, P99)
- ✓ Búsquedas con filtros
- ✓ Uso de almacenamiento

**Ejecutar:**
```bash
make benchmark
# o
python3 benchmark.py
```

---

## 🎨 Modelos Disponibles

El proyecto viene configurado con **all-MiniLM-L6-v2** (rápido y eficiente).

### Para cambiar el modelo:

Edita `docker-compose.yml`, línea del `t2v-transformers`:

```yaml
t2v-transformers:
  image: semitechnologies/transformers-inference:MODELO_AQUI
```

### Opciones recomendadas:

| Modelo | Velocidad | Calidad | Dimensiones | Uso |
|--------|-----------|---------|-------------|-----|
| `sentence-transformers-all-MiniLM-L6-v2` | ⚡⚡⚡ | ⭐⭐⭐ | 384 | General (actual) |
| `sentence-transformers-all-mpnet-base-v2` | ⚡⚡ | ⭐⭐⭐⭐ | 768 | Mejor calidad |
| `sentence-transformers-paraphrase-multilingual-MiniLM-L12-v2` | ⚡⚡ | ⭐⭐⭐ | 384 | Multiidioma |
| `sentence-transformers-multi-qa-MiniLM-L6-cos-v1` | ⚡⚡⚡ | ⭐⭐⭐ | 384 | Q&A |

**Para multiidioma (incluye español):**
```bash
make start-multilingual
```

---

## 🛠️ Comandos Útiles (Makefile)

```bash
make help           # Ver todos los comandos disponibles
make start          # Iniciar Weaviate
make stop           # Detener Weaviate
make restart        # Reiniciar servicios
make logs           # Ver logs en tiempo real
make health         # Verificar estado del sistema
make clean          # Limpiar datos
make reset          # Reiniciar desde cero
make setup          # Setup completo (start + install)
```

---

## 🔧 Comandos Docker Directos

```bash
# Iniciar
docker-compose up -d

# Detener
docker-compose down

# Ver logs
docker-compose logs -f

# Ver estado
docker-compose ps

# Reiniciar
docker-compose restart

# Limpiar todo
docker-compose down -v
```

---

## 🌐 Endpoints Disponibles

Una vez iniciado:

| Endpoint | URL | Descripción |
|----------|-----|-------------|
| API REST | http://localhost:8080/v1 | API principal |
| GraphQL | http://localhost:8080/v1/graphql | Consultas GraphQL |
| Meta Info | http://localhost:8080/v1/meta | Información del sistema |
| Schema | http://localhost:8080/v1/schema | Ver schemas |
| Health | http://localhost:8080/v1/.well-known/ready | Estado de salud |

---

## 📊 Desempeño Esperado

Con hardware moderno:

- **Inserción**: 50-200 objetos/segundo
- **Búsqueda**: 5-20ms de latencia (P95)
- **QPS**: 50-200 queries/segundo
- **Memoria**: ~4GB RAM recomendado

*Nota: Con GPU, el rendimiento puede ser 5-10x mejor.*

---

## 🔒 Configuración para Producción

El setup actual es ideal para **desarrollo**. Para producción:

### 1. Habilitar Autenticación

Edita `docker-compose.yml`:
```yaml
environment:
  AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: 'false'
  AUTHENTICATION_APIKEY_ENABLED: 'true'
  AUTHENTICATION_APIKEY_ALLOWED_KEYS: 'tu-clave-segura-aqui'
```

### 2. Habilitar HTTPS

Usa un reverse proxy (Nginx, Traefik, Caddy).

### 3. Backups

```bash
# Backup del volumen
docker run --rm -v weaviate_data:/data -v $(pwd):/backup \
  ubuntu tar czf /backup/weaviate-backup.tar.gz /data
```

### 4. Monitoreo

- Prometheus metrics: http://localhost:8080/metrics
- Logs centralizados con ELK/Loki

---

## 💡 Tips y Buenas Prácticas

### ✅ DO:
- Usa batch inserts para grandes volúmenes
- Define schemas explícitos en producción
- Monitorea el uso de memoria
- Usa índices apropiados (HNSW por defecto)
- Prueba diferentes modelos para tu caso de uso

### ❌ DON'T:
- No uses `autoschema` en producción
- No insertes sin batch para grandes volúmenes
- No cambies el modelo sin limpiar datos antiguos
- No expongas el puerto sin autenticación

---

## 🐛 Troubleshooting

### Problema: Puerto 8080 ocupado
**Solución:** Cambia el puerto en `docker-compose.yml`:
```yaml
ports:
  - "8081:8080"
```

### Problema: Contenedor no inicia
**Solución:** Ver logs:
```bash
make logs
# o
docker-compose logs weaviate
```

### Problema: Falta memoria
**Solución:** 
1. Usa un modelo más pequeño (MiniLM-L6)
2. Aumenta RAM disponible para Docker
3. Reduce `batch.batch_size` en el código

### Problema: Búsquedas lentas
**Solución:**
1. Habilita GPU si disponible (`ENABLE_CUDA: '1'`)
2. Usa un modelo más rápido
3. Reduce el número de objetos indexados

---

## 📖 Recursos Adicionales

- **Documentación Weaviate**: https://weaviate.io/developers/weaviate
- **Client Python**: https://weaviate.io/developers/weaviate/client-libraries/python
- **Modelos**: https://www.sbert.net/docs/pretrained_models.html
- **GraphQL**: https://weaviate.io/developers/weaviate/api/graphql

---

## ❓ Preguntas Frecuentes

### ¿Puedo usar GPUs?
Sí, cambia `ENABLE_CUDA: '1'` en `docker-compose.yml` (requiere NVIDIA GPU + nvidia-docker).

### ¿Cuántos vectores puedo almacenar?
Depende de la RAM. Aprox. 1M de vectores (384 dims) = ~1.5GB RAM.

### ¿Puedo usar múltiples modelos?
Sí, puedes especificar diferentes vectorizadores por clase en el schema.

### ¿Los datos persisten?
Sí, se guardan en volumen Docker. Solo se borran con `docker-compose down -v`.

### ¿Funciona en producción?
Sí, pero habilita autenticación y usa HTTPS con reverse proxy.

---

## 🎉 Siguientes Pasos

1. ✅ Ejecuta `make example` para ver Weaviate en acción
2. ✅ Prueba `make advanced` para features complejas
3. ✅ Ejecuta `make benchmark` para medir rendimiento
4. ✅ Lee `README.md` para documentación completa
5. ✅ Adapta el código a tu caso de uso específico

---

## 📞 Soporte

- **GitHub Issues**: Para reportar bugs
- **Weaviate Slack**: Comunidad activa
- **Stack Overflow**: Tag `weaviate`

---

**¡Disfruta tu base de datos vectorial! 🚀**
