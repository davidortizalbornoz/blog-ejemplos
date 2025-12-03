#!/usr/bin/env python3
"""
Diagrama Visual del Flujo RAG
"""

def print_rag_flow():
    """Imprimir diagrama visual del flujo RAG"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                    🧠 FLUJO COMPLETO DE RAG                          ║
╚══════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────┐
│  FASE 1: PREPARACIÓN (Se hace UNA sola vez)                        │
└─────────────────────────────────────────────────────────────────────┘

      📁 TUS DOCUMENTOS
      │
      ├─ manual_python.pdf
      ├─ politicas_empresa.docx
      ├─ documentacion_api.md
      └─ base_conocimiento.txt
      │
      │
      ↓
╔═════════════════════════════════════════════════════════════════╗
║  PROCESAMIENTO DE DOCUMENTOS                                    ║
╚═════════════════════════════════════════════════════════════════╝
      │
      ├─→ [CHUNKING] Dividir en trozos manejables
      │   │
      │   ├─ "Python es un lenguaje de programación..."
      │   ├─ "La política de vacaciones establece..."
      │   └─ "El endpoint /api/users requiere..."
      │
      ↓
╔═════════════════════════════════════════════════════════════════╗
║  🔢 CONVERSIÓN A VECTORES (Embeddings)                         ║
║                                                                  ║
║  Modelo: text2vec-transformers (MiniLM)                        ║
╚═════════════════════════════════════════════════════════════════╝
      │
      ├─→ Texto → [0.12, -0.34, 0.56, 0.23, ..., -0.11]  (384 dims)
      │            └─ Vector captura el SIGNIFICADO
      │
      ↓
╔═════════════════════════════════════════════════════════════════╗
║  💾 WEAVIATE (Base de Datos Vectorial)                         ║
║                                                                  ║
║  Almacena:                                                      ║
║  • Texto original                                               ║
║  • Vector (embedding)                                           ║
║  • Metadata (fecha, autor, categoría, etc.)                    ║
╚═════════════════════════════════════════════════════════════════╝
      │
      └─→ ✅ BASE DE CONOCIMIENTO LISTA




┌─────────────────────────────────────────────────────────────────────┐
│  FASE 2: CONSULTA (Se ejecuta CADA vez que el usuario pregunta)   │
└─────────────────────────────────────────────────────────────────────┘


      👤 USUARIO
      │
      └─→ "¿Cuántos días de vacaciones tengo?"
            │
            ↓
╔═════════════════════════════════════════════════════════════════╗
║  🔢 VECTORIZACIÓN DE LA PREGUNTA                               ║
║                                                                  ║
║  Mismo modelo que para los documentos                          ║
╚═════════════════════════════════════════════════════════════════╝
            │
            └─→ [0.15, -0.28, 0.51, 0.19, ..., -0.09]
                 │
                 │
                 ↓
╔═════════════════════════════════════════════════════════════════╗
║  🔍 BÚSQUEDA KNN (K-Nearest Neighbors)                         ║
║                                                                  ║
║  Weaviate busca vectores similares en la base de datos        ║
║                                                                  ║
║  Espacio Vectorial (simplificado a 2D):                        ║
║                                                                  ║
║      •"política vacaciones"                                     ║
║        ↑                                                        ║
║   0.98 │ ← Alta similitud                                      ║
║        │                                                        ║
║        ⭐ "¿días vacaciones?" ← Pregunta                       ║
║        │                                                        ║
║   0.95 │                                                        ║
║        ↓                                                        ║
║      •"días libres"                                             ║
║                                                                  ║
║      •"salario" ← Baja similitud (0.23)                        ║
╚═════════════════════════════════════════════════════════════════╝
            │
            ↓
╔═════════════════════════════════════════════════════════════════╗
║  📄 DOCUMENTOS RECUPERADOS (Top 3)                             ║
║                                                                  ║
║  1. "La política de vacaciones establece 20 días al año..."   ║
║     Similitud: 0.98                                             ║
║                                                                  ║
║  2. "Los días libres se pueden acumular hasta..."              ║
║     Similitud: 0.95                                             ║
║                                                                  ║
║  3. "Para solicitar ausencias, completa el formulario..."      ║
║     Similitud: 0.92                                             ║
╚═════════════════════════════════════════════════════════════════╝
            │
            │
            ↓
╔═════════════════════════════════════════════════════════════════╗
║  📝 CONSTRUCCIÓN DEL PROMPT                                    ║
║                                                                  ║
║  Eres un asistente experto. Responde basándote en:            ║
║                                                                  ║
║  CONTEXTO:                                                      ║
║  [Documento 1]: La política de vacaciones...                   ║
║  [Documento 2]: Los días libres se pueden...                   ║
║  [Documento 3]: Para solicitar ausencias...                    ║
║                                                                  ║
║  PREGUNTA:                                                      ║
║  ¿Cuántos días de vacaciones tengo?                            ║
║                                                                  ║
║  INSTRUCCIONES:                                                 ║
║  - Usa SOLO información del contexto                           ║
║  - Cita las fuentes                                             ║
║  - Sé específico y claro                                        ║
╚═════════════════════════════════════════════════════════════════╝
            │
            │
            ↓
╔═════════════════════════════════════════════════════════════════╗
║  🤖 LLM (GPT-4, Claude, Llama, etc.)                           ║
║                                                                  ║
║  El LLM:                                                        ║
║  1. Lee el contexto proporcionado                              ║
║  2. Lee la pregunta                                             ║
║  3. Genera respuesta basándose SOLO en el contexto            ║
║  4. Cita las fuentes                                            ║
╚═════════════════════════════════════════════════════════════════╝
            │
            │
            ↓
╔═════════════════════════════════════════════════════════════════╗
║  💬 RESPUESTA GENERADA                                          ║
║                                                                  ║
║  "Según la política de vacaciones de la empresa, tienes       ║
║   derecho a 20 días de vacaciones al año. Estos días se       ║
║   pueden acumular hasta un máximo de 40 días.                 ║
║                                                                  ║
║   Para solicitar tus vacaciones, debes completar el           ║
║   formulario disponible en el portal de empleados.            ║
║                                                                  ║
║   [Fuentes: Política de Vacaciones 2024, Manual del          ║
║   Empleado]"                                                   ║
╚═════════════════════════════════════════════════════════════════╝
            │
            ↓
      👤 USUARIO recibe respuesta
         │
         └─→ ✅ Precisa
             ✅ Verificable
             ✅ Basada en datos reales
             ✅ Con fuentes citadas




┌─────────────────────────────────────────────────────────────────────┐
│  🎯 VENTAJAS DE RAG                                                │
└─────────────────────────────────────────────────────────────────────┘

╔════════════════════════╦════════════════════════════════════════════╗
║   SIN RAG              ║   CON RAG                                  ║
╠════════════════════════╬════════════════════════════════════════════╣
║ ❌ Solo conocimiento   ║ ✅ Acceso a TUS documentos                ║
║    del entrenamiento   ║                                            ║
║                        ║                                            ║
║ ❌ Desactualizado      ║ ✅ Siempre actualizado                    ║
║    (datos antiguos)    ║    (añade docs nuevos)                    ║
║                        ║                                            ║
║ ❌ Alucinaciones       ║ ✅ Respuestas verificables                ║
║    frecuentes          ║    (basadas en docs reales)               ║
║                        ║                                            ║
║ ❌ Sin fuentes         ║ ✅ Con citas y referencias                ║
║                        ║                                            ║
║ ❌ Genérico            ║ ✅ Específico a tu dominio                ║
║                        ║                                            ║
║ ❌ Sin datos privados  ║ ✅ Usa tu info confidencial               ║
╚════════════════════════╩════════════════════════════════════════════╝




┌─────────────────────────────────────────────────────────────────────┐
│  ❓ ¿POR QUÉ VECTORES?                                             │
└─────────────────────────────────────────────────────────────────────┘

🔹 BÚSQUEDA POR PALABRAS (Tradicional):
   
   Usuario busca: "días libres"
   │
   └─→ Base de datos busca: "días libres" (texto exacto)
       │
       └─→ ❌ NO encuentra: "política de vacaciones"
           ❌ NO encuentra: "ausencias laborales"
           ❌ NO encuentra: "tiempo de descanso"
           
           Porque las palabras NO son idénticas!


🔹 BÚSQUEDA POR VECTORES (Semántica):
   
   Usuario busca: "días libres"
   │
   ├─→ Convertir a vector: [0.15, -0.28, 0.51, ...]
   │
   └─→ Buscar vectores CERCANOS en el espacio semántico
       │
       └─→ ✅ Encuentra: "política de vacaciones" (vector similar)
           ✅ Encuentra: "ausencias laborales" (vector similar)
           ✅ Encuentra: "tiempo de descanso" (vector similar)
           
           ¡Busca por SIGNIFICADO, no por palabras!


   ESPACIO VECTORIAL (conceptual):
   
              Trabajo
                │
        ┌───────┼───────┐
        │       │       │
   "vacaciones" │   "días libres"
        │       │       │
        └───────┼───────┘
                │
          "ausencias"
                │
         (todos cercanos porque
          tienen significado similar)




┌─────────────────────────────────────────────────────────────────────┐
│  📊 EJEMPLO DE SIMILITUD VECTORIAL                                 │
└─────────────────────────────────────────────────────────────────────┘

Vector de pregunta:     [0.2,  0.5, -0.1,  0.8, ...]
                          ↕     ↕     ↕     ↕
Documento "vacaciones": [0.21, 0.48, -0.09, 0.79, ...] → Distancia: 0.02
                                                           ✅ MUY SIMILAR!

Documento "salario":    [0.8, -0.3,  0.6, -0.2, ...] → Distancia: 1.45
                                                           ❌ MUY DIFERENTE

Por eso RAG encuentra el documento correcto!




┌─────────────────────────────────────────────────────────────────────┐
│  🎓 ANALOGÍA FINAL                                                 │
└─────────────────────────────────────────────────────────────────────┘

RAG es como un ESTUDIANTE en un EXAMEN:

❌ SIN RAG:
   Estudiante sin apuntes
   │
   └─→ Solo confía en su memoria
       └─→ Puede olvidar cosas
           └─→ Puede inventar respuestas (alucinar)

✅ CON RAG:
   Estudiante CON apuntes organizados
   │
   ├─→ Busca en sus apuntes (Weaviate)
   │   └─→ Encuentra la página correcta (búsqueda vectorial)
   │
   ├─→ Lee la información exacta
   │
   └─→ Formula respuesta basada en los apuntes (LLM)
       └─→ ✅ Respuesta correcta
           ✅ Con referencia a la página
           ✅ Sin inventar nada




┌─────────────────────────────────────────────────────────────────────┐
│  ✅ CONCLUSIÓN                                                     │
└─────────────────────────────────────────────────────────────────────┘

RAG = BÚSQUEDA INTELIGENTE + LLM

1. Los VECTORES permiten buscar por SIGNIFICADO
   (no necesitas usar las palabras exactas)

2. WEAVIATE almacena tus documentos como vectores
   (listos para búsqueda semántica)

3. Cuando preguntas, Weaviate encuentra lo RELEVANTE
   (los 3-5 documentos más cercanos)

4. El LLM lee esos documentos y GENERA la respuesta
   (precisa, verificable, sin alucinar)

RESULTADO:
🎯 Respuestas basadas en TU información
🎯 Siempre actualizadas
🎯 Sin necesidad de re-entrenar el modelo
🎯 Con fuentes verificables

¡RAG es darle "superpoderes" a un LLM con TUS datos!
    """)


if __name__ == "__main__":
    print_rag_flow()
