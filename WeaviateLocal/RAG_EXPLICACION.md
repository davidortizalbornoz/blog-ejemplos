# 🧠 RAG (Retrieval-Augmented Generation) - Explicación Completa

## 📌 ¿Qué es RAG?

**RAG = Retrieval-Augmented Generation**
- **Retrieval** (Recuperación): Buscar información relevante
- **Augmented** (Aumentado): Enriquecer el contexto
- **Generation** (Generación): Generar respuesta con LLM

---

## 🤔 El Problema que RAG Resuelve

### ❌ **Problema: LLM sin RAG**

Los LLMs (ChatGPT, Claude, etc.) tienen **limitaciones críticas**:

```
┌─────────────────────────────────────────────────────────┐
│  LLM (GPT-4, Claude, etc.)                              │
│                                                         │
│  Entrenado hasta: Octubre 2023                         │
│  Conocimiento: Solo lo que vio en entrenamiento       │
│                                                         │
│  ❌ NO sabe de eventos después de Oct 2023            │
│  ❌ NO sabe de documentos privados de tu empresa      │
│  ❌ NO sabe de tu base de datos interna               │
│  ❌ NO sabe de documentación técnica específica       │
│  ❌ Puede "alucinar" información que no sabe          │
└─────────────────────────────────────────────────────────┘
```

### ✅ **Solución: LLM con RAG**

```
┌─────────────────────────────────────────────────────────┐
│  LLM + RAG                                               │
│                                                         │
│  ✅ Acceso a información actualizada                   │
│  ✅ Acceso a documentos privados                       │
│  ✅ Respuestas basadas en TUS datos                    │
│  ✅ Reducción de alucinaciones                         │
│  ✅ Citas y referencias verificables                   │
└─────────────────────────────────────────────────────────┘
```

---

## 🔄 ¿Cómo Funciona RAG? (Flujo Completo)

### **Fase 1: Preparación (Se hace UNA vez)**

```
1. Tus Documentos
   ↓
   📄 "Manual de Python"
   📄 "Políticas de la empresa"
   📄 "Documentación técnica"
   📄 "Base de conocimiento"
   ↓
2. Dividir en Chunks (Trozos)
   ↓
   📝 "Python es un lenguaje de programación..."
   📝 "La política de vacaciones es..."
   📝 "El API REST usa autenticación OAuth..."
   ↓
3. Convertir a Vectores (Embeddings)
   ↓
   🔢 [0.2, 0.5, -0.1, 0.8, ...] ← 384 dimensiones
   🔢 [0.1, -0.3, 0.6, 0.2, ...]
   🔢 [-0.4, 0.7, 0.1, -0.2, ...]
   ↓
4. Almacenar en Base de Datos Vectorial (Weaviate)
   ↓
   💾 Vector DB lista para búsquedas
```

### **Fase 2: Consulta del Usuario (Cada pregunta)**

```
Usuario pregunta: "¿Cuál es la política de vacaciones?"
         ↓
1. Convertir pregunta a vector
         ↓
   🔢 [0.15, -0.25, 0.55, 0.25, ...]
         ↓
2. Buscar vectores similares (KNN)
         ↓
   💾 Weaviate encuentra los 3 documentos más relevantes:
      📄 "La política de vacaciones es 20 días al año..."
      📄 "Los días de vacaciones se pueden acumular..."
      📄 "Para solicitar vacaciones, usa el portal..."
         ↓
3. Construir Prompt para el LLM
         ↓
   📝 "Contexto: [documentos encontrados]
       Pregunta: ¿Cuál es la política de vacaciones?
       Responde basándote SOLO en el contexto."
         ↓
4. Enviar al LLM (GPT-4, Claude, etc.)
         ↓
   🤖 LLM genera respuesta basada en TUS documentos
         ↓
5. Respuesta al usuario
         ↓
   ✅ "Según la política de la empresa, tienes 20 días
       de vacaciones al año, los cuales se pueden
       acumular hasta 40 días máximo..."
```

---

## 🎯 ¿Por Qué Usar Vectores?

### **Pregunta: ¿Por qué no simplemente buscar con palabras clave?**

### ❌ **Búsqueda Tradicional (Keyword Search)**

```python
Usuario: "¿Cómo puedo descansar del trabajo?"

# Búsqueda por palabras clave
keywords = ["descansar", "trabajo"]

# ❌ NO encuentra: "política de vacaciones"
# ❌ NO encuentra: "días libres"
# ❌ NO encuentra: "ausencias laborales"

# Porque las palabras literales no coinciden!
```

### ✅ **Búsqueda Vectorial (Semantic Search)**

```python
Usuario: "¿Cómo puedo descansar del trabajo?"

# Convertir a vector
vector_pregunta = [0.15, -0.25, 0.55, ...]

# Buscar vectores similares por SIGNIFICADO
# ✅ Encuentra: "política de vacaciones" (similar semánticamente)
# ✅ Encuentra: "días libres" (similar semánticamente)
# ✅ Encuentra: "ausencias laborales" (similar semánticamente)

# ¡Entiende el SIGNIFICADO, no solo palabras!
```

### **Ejemplo Visual:**

```
Espacio Vectorial (simplificado a 2D):

                    ↑
         "vacaciones"  •
                      |
    "días libres"  •  |  • "descanso"
                  |   |
                  | • "descansar del trabajo" ← Pregunta
                  |   |
  "ausencias"  •  |   |
                      |
                      |
    ────────────────────────────→

Todos los puntos cercanos tienen SIGNIFICADOS similares
aunque usen palabras diferentes!
```

---

## 📊 Comparación: Con vs Sin RAG

### **Ejemplo Real: Chatbot de Empresa**

#### **Pregunta:** "¿Cuándo fue la última reunión del equipo de ingeniería?"

### SIN RAG (LLM solo):
```
🤖 LLM: "No tengo información sobre reuniones específicas
         de tu empresa. Mi conocimiento se limita a 
         octubre 2023. Te sugiero revisar tu calendario
         o correo electrónico."
         
❌ Respuesta genérica e inútil
❌ No accede a datos de la empresa
```

### CON RAG:
```
1. Vector DB busca en documentos de la empresa
   📄 Encuentra: "Minuta reunión ingeniería - 15 Nov 2024"
   📄 Encuentra: "Resumen semanal equipo - 18 Nov 2024"

2. LLM recibe estos documentos como contexto

3. 🤖 LLM: "La última reunión del equipo de ingeniería fue
            el 18 de noviembre de 2024. En ella se discutió:
            - Migración a microservicios
            - Nueva arquitectura de base de datos
            - Sprint planning para diciembre
            
            [Fuente: Resumen semanal equipo - 18 Nov 2024]"

✅ Respuesta específica y precisa
✅ Basada en datos reales de la empresa
✅ Con fuente verificable
```

---

## 🔬 Ejemplo Técnico Paso a Paso

### **Escenario: Sistema de Soporte Técnico**

#### **Paso 1: Indexar Documentación**

```python
# Documentos de soporte técnico
docs = [
    {
        "title": "Error de conexión a base de datos",
        "content": "Si recibes el error 'Connection timeout', verifica:\n"
                   "1. Firewall permite puerto 5432\n"
                   "2. PostgreSQL está corriendo\n"
                   "3. Credenciales son correctas"
    },
    {
        "title": "Configurar variables de entorno",
        "content": "Para configurar variables de entorno en producción:\n"
                   "export DB_HOST=localhost\n"
                   "export DB_PORT=5432\n"
                   "export DB_NAME=myapp"
    },
    {
        "title": "Optimización de queries",
        "content": "Para mejorar rendimiento de consultas SQL:\n"
                   "1. Añade índices a columnas frecuentes\n"
                   "2. Usa EXPLAIN para analizar queries\n"
                   "3. Evita SELECT * en tablas grandes"
    }
]

# Weaviate automáticamente convierte a vectores
for doc in docs:
    weaviate_client.data_object.create(
        data_object=doc,
        class_name="TechDoc"
    )
# ✅ Vectores almacenados en Weaviate
```

#### **Paso 2: Usuario hace pregunta**

```python
user_question = "Mi aplicación no puede conectarse a PostgreSQL, ¿qué hago?"
```

#### **Paso 3: Buscar documentos relevantes (RAG - Retrieval)**

```python
# Búsqueda semántica
relevant_docs = weaviate_client.query \
    .get("TechDoc", ["title", "content"]) \
    .with_near_text({"concepts": [user_question]}) \
    .with_limit(2) \
    .do()

# Resultado:
# ✅ Documento 1: "Error de conexión a base de datos" (muy relevante!)
# ✅ Documento 2: "Configurar variables de entorno" (relevante)
```

#### **Paso 4: Construir contexto para LLM (RAG - Augmented)**

```python
context = ""
for doc in relevant_docs["data"]["Get"]["TechDoc"]:
    context += f"Título: {doc['title']}\n"
    context += f"Contenido: {doc['content']}\n\n"

prompt = f"""
Eres un asistente técnico. Responde basándote SOLO en la siguiente información:

CONTEXTO:
{context}

PREGUNTA DEL USUARIO:
{user_question}

INSTRUCCIONES:
- Usa solo información del contexto
- Sé específico y claro
- Cita las fuentes
"""
```

#### **Paso 5: Enviar a LLM (RAG - Generation)**

```python
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "Eres un asistente técnico experto."},
        {"role": "user", "content": prompt}
    ]
)

print(response.choices[0].message.content)
```

#### **Respuesta del LLM:**

```
Para resolver el problema de conexión a PostgreSQL, sigue estos pasos:

1. **Verifica el firewall**: Asegúrate de que el puerto 5432 está abierto
2. **Confirma que PostgreSQL está corriendo**: Ejecuta `systemctl status postgresql`
3. **Revisa las credenciales**: Verifica las variables de entorno:
   - DB_HOST debe apuntar al servidor correcto
   - DB_PORT debe ser 5432 (por defecto)
   - DB_NAME debe coincidir con tu base de datos

Si el problema persiste, revisa los logs en /var/log/postgresql/

[Fuente: Documentación "Error de conexión a base de datos" y 
 "Configurar variables de entorno"]
```

✅ **Respuesta precisa basada en TU documentación**

---

## 🎭 Analogía del Mundo Real

### **Sin RAG = Estudiante en examen SIN apuntes**
```
Profesor: "¿Cuál es la fórmula para calcular el área de un trapecio?"
Estudiante: "Ehhh... creo que es algo con la base y la altura...
             tal vez... (A = b × h)?"
             
❌ Respuesta incorrecta (alucinación)
❌ Solo confía en su memoria (limitada)
```

### **Con RAG = Estudiante en examen CON apuntes**
```
Profesor: "¿Cuál es la fórmula para calcular el área de un trapecio?"

Estudiante:
1. 🔍 Busca en sus apuntes (Vector DB)
2. 📄 Encuentra la página correcta
3. 📖 Lee: "A = ((b₁ + b₂) × h) / 2"
4. 💬 Responde: "El área de un trapecio es A = ((b₁ + b₂) × h) / 2
                 donde b₁ y b₂ son las bases y h es la altura"
                 
✅ Respuesta correcta
✅ Basada en fuente verificable
✅ Cita exacta de los apuntes
```

**RAG es darle "apuntes" al LLM!**

---

## 💡 Ventajas de RAG

### 1. **Información Actualizada**
```
Sin RAG: "No sé quién ganó las elecciones de 2024"
Con RAG: "Según las noticias indexadas, ganó [candidato]"
```

### 2. **Datos Privados**
```
Sin RAG: "No tengo acceso a información de tu empresa"
Con RAG: "Según el documento interno Q3-2024.pdf..."
```

### 3. **Reducción de Alucinaciones**
```
Sin RAG: Inventa información (alucinación)
Con RAG: Solo usa información de los documentos encontrados
```

### 4. **Trazabilidad**
```
Sin RAG: "Confía en mí"
Con RAG: "Según el documento X, página Y, sección Z..."
```

### 5. **Dominio Específico**
```
Sin RAG: Conocimiento general
Con RAG: Experto en TU dominio (medicina, legal, ingeniería, etc.)
```

---

## 🏗️ Arquitectura Completa de RAG

```
┌─────────────────────────────────────────────────────────────────┐
│                     SISTEMA RAG COMPLETO                        │
└─────────────────────────────────────────────────────────────────┘

1. INDEXACIÓN (Offline - Una vez)
   ┌──────────────┐
   │ Documentos   │  (PDFs, docs, web, DB, etc.)
   └──────┬───────┘
          │
          ↓
   ┌──────────────┐
   │ Chunking     │  (Dividir en trozos)
   └──────┬───────┘
          │
          ↓
   ┌──────────────┐
   │ Embedding    │  (text2vec-transformers)
   │ Model        │  Convierte texto → vectores
   └──────┬───────┘
          │
          ↓
   ┌──────────────┐
   │ Weaviate     │  Almacena vectores + metadata
   │ Vector DB    │
   └──────────────┘


2. CONSULTA (Online - Cada pregunta)
   ┌──────────────┐
   │ User Query   │  "¿Cómo configurar SSL?"
   └──────┬───────┘
          │
          ↓
   ┌──────────────┐
   │ Embedding    │  Pregunta → vector
   └──────┬───────┘
          │
          ↓
   ┌──────────────┐
   │ Weaviate     │  Búsqueda KNN
   │ Search       │  Encuentra top K documentos
   └──────┬───────┘
          │
          ↓
   ┌──────────────┐
   │ Reranking    │  (Opcional) Reordena resultados
   └──────┬───────┘
          │
          ↓
   ┌──────────────┐
   │ Prompt       │  Construye contexto + pregunta
   │ Engineering  │
   └──────┬───────┘
          │
          ↓
   ┌──────────────┐
   │ LLM          │  GPT-4, Claude, etc.
   │ (OpenAI)     │  Genera respuesta
   └──────┬───────┘
          │
          ↓
   ┌──────────────┐
   │ Response     │  Respuesta al usuario
   └──────────────┘
```

---

## 🧪 Código Completo de RAG con Weaviate

```python
import weaviate
import openai

class RAGSystem:
    def __init__(self, weaviate_url, openai_key):
        self.weaviate_client = weaviate.Client(weaviate_url)
        openai.api_key = openai_key
    
    def index_documents(self, documents):
        """Fase 1: Indexar documentos (una vez)"""
        print("📝 Indexando documentos...")
        
        with self.weaviate_client.batch as batch:
            for doc in documents:
                # Weaviate automáticamente convierte a vectores
                batch.add_data_object(
                    data_object={
                        "title": doc["title"],
                        "content": doc["content"]
                    },
                    class_name="Document"
                )
        
        print(f"✅ {len(documents)} documentos indexados")
    
    def retrieve_relevant_docs(self, query, top_k=3):
        """Fase 2: Recuperar documentos relevantes (Retrieval)"""
        print(f"🔍 Buscando documentos para: '{query}'")
        
        result = (
            self.weaviate_client.query
            .get("Document", ["title", "content"])
            .with_near_text({"concepts": [query]})
            .with_limit(top_k)
            .with_additional(["distance"])
            .do()
        )
        
        docs = result["data"]["Get"]["Document"]
        print(f"✅ Encontrados {len(docs)} documentos relevantes")
        
        return docs
    
    def generate_answer(self, query, relevant_docs):
        """Fase 3: Generar respuesta con LLM (Augmented Generation)"""
        # Construir contexto
        context = "\n\n".join([
            f"Documento: {doc['title']}\n{doc['content']}"
            for doc in relevant_docs
        ])
        
        # Prompt engineering
        prompt = f"""
Eres un asistente experto. Responde la pregunta basándote ÚNICAMENTE 
en el contexto proporcionado.

CONTEXTO:
{context}

PREGUNTA:
{query}

INSTRUCCIONES:
- Usa solo información del contexto
- Si el contexto no contiene la respuesta, di "No tengo información suficiente"
- Cita las fuentes
- Sé claro y conciso

RESPUESTA:
"""
        
        # Llamar al LLM
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres un asistente técnico experto."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3  # Más determinista, menos creativo
        )
        
        return response.choices[0].message.content
    
    def ask(self, question):
        """Método principal: RAG completo"""
        print("\n" + "="*60)
        print(f"❓ Pregunta: {question}")
        print("="*60)
        
        # 1. Retrieve
        relevant_docs = self.retrieve_relevant_docs(question)
        
        # 2. Augmented Generation
        answer = self.generate_answer(question, relevant_docs)
        
        print("\n💬 Respuesta:")
        print(answer)
        
        return answer


# USO
rag = RAGSystem(
    weaviate_url="http://localhost:8080",
    openai_key="tu-api-key"
)

# Indexar tus documentos (una vez)
docs = [
    {
        "title": "Guía de instalación",
        "content": "Para instalar la aplicación: 1) Descarga el instalador..."
    },
    {
        "title": "Solución de problemas",
        "content": "Si encuentras el error 'Connection refused', verifica..."
    }
]
rag.index_documents(docs)

# Hacer preguntas (muchas veces)
rag.ask("¿Cómo instalo la aplicación?")
rag.ask("Tengo un error de conexión, ¿qué hago?")
```

---

## 🎯 Casos de Uso Reales de RAG

### 1. **Chatbot de Soporte Técnico**
- Indexa: Documentación técnica, FAQs, tickets resueltos
- Usuario pregunta: "¿Cómo resetear mi contraseña?"
- RAG encuentra la documentación exacta y responde

### 2. **Asistente Legal**
- Indexa: Leyes, jurisprudencia, contratos
- Abogado pregunta: "¿Qué dice la ley sobre X?"
- RAG cita artículos específicos con referencias

### 3. **Búsqueda en Documentación Interna**
- Indexa: Wikis, Confluence, Google Docs
- Empleado pregunta: "¿Cuál es el proceso de aprobación?"
- RAG encuentra el procedimiento exacto

### 4. **Análisis de Investigación**
- Indexa: Papers científicos, estudios
- Investigador pregunta: "¿Qué estudios existen sobre X?"
- RAG resume hallazgos de múltiples papers

### 5. **E-commerce Inteligente**
- Indexa: Catálogo de productos, reviews
- Cliente pregunta: "Laptop buena para gaming y edición"
- RAG encuentra productos que cumplen ambos criterios

---

## 📈 RAG vs Alternativas

### **Fine-tuning**
```
Fine-tuning:
- Entrena el modelo con tus datos
- ❌ Caro (miles de dólares)
- ❌ Lento (horas/días)
- ❌ Difícil de actualizar
- ✅ El modelo "aprende" tus datos

RAG:
- Busca en tus datos en tiempo real
- ✅ Gratis o barato
- ✅ Instantáneo
- ✅ Fácil actualizar (añadir docs)
- ✅ Siempre información fresca
```

### **Prompt Engineering Puro**
```
Prompt con todo el contexto:
- Incluyes todos los docs en el prompt
- ❌ Limitado por context window (128k tokens)
- ❌ Caro (pagas por todos los tokens)
- ❌ Lento (procesar todo el contexto)

RAG:
- Solo incluye docs relevantes
- ✅ Ilimitados documentos en DB
- ✅ Barato (solo pagas por docs relevantes)
- ✅ Rápido (solo procesa lo necesario)
```

---

## 🔑 Conclusión: ¿Por Qué Vectores en RAG?

### **La Respuesta Simple:**

```
Los vectores permiten encontrar información por SIGNIFICADO,
no por palabras exactas.

Sin vectores:
  "política de vacaciones" != "días libres"
  
Con vectores:
  "política de vacaciones" ≈ "días libres" ≈ "ausencias"
  (todos tienen vectores cercanos en el espacio semántico)
```

### **El Flujo Completo:**

```
1. Almacenas TUS documentos como vectores en Weaviate
   → Para poder buscarlos por significado
   
2. Usuario hace una pregunta
   → Conviertes a vector
   
3. Weaviate encuentra los documentos MÁS RELEVANTES
   → Búsqueda KNN por similitud vectorial
   
4. Envías esos documentos al LLM como contexto
   → El LLM genera respuesta basada en TUS datos
   
5. Usuario recibe respuesta precisa y verificable
   → Basada en información real, no alucinada
```

---

## 💡 Metáfora Final

**RAG es como tener un bibliotecario + experto:**

```
🏢 Biblioteca (Weaviate):
   - Almacena millones de libros (documentos)
   - Organizados por tema (vectores similares juntos)

👤 Bibliotecario (Sistema de búsqueda vectorial):
   - Entiende tu pregunta
   - Encuentra los 3-5 libros más relevantes
   - Te los entrega rápidamente

🧠 Experto (LLM):
   - Lee esos libros específicos
   - Sintetiza la información
   - Te da una respuesta clara y citada
```

**Sin RAG:** El experto solo confía en su memoria (limitada)
**Con RAG:** El experto consulta la biblioteca antes de responder

---

## 🚀 Próximos Pasos

1. Entender que RAG = Búsqueda + LLM
2. Los vectores permiten búsqueda semántica
3. Weaviate es el "bibliotecario inteligente"
4. El LLM es el "experto que sintetiza"
5. Juntos crean respuestas precisas y verificables

**Ahora ya sabes por qué almacenamos vectores: ¡para encontrar información relevante por significado y dársela al LLM!**
