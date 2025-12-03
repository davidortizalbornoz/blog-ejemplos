#!/usr/bin/env python3
"""
Ejemplo Simple de RAG (Retrieval-Augmented Generation)
SIN usar LLM externo - solo para demostrar el concepto de Retrieval
"""

import weaviate
from datetime import datetime


WEAVIATE_URL = "http://localhost:8080"


def print_section(title):
    """Imprimir sección con formato"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def create_knowledge_base():
    """Crear base de conocimiento con información técnica"""
    print_section("📚 PASO 1: CREAR BASE DE CONOCIMIENTO (INDEXACIÓN)")
    
    # Conectar a Weaviate
    client = weaviate.Client(WEAVIATE_URL)
    
    if not client.is_ready():
        print("❌ Weaviate no está disponible. Ejecuta: docker-compose up -d")
        return None
    
    print("✅ Conectado a Weaviate")
    
    # Limpiar datos anteriores
    try:
        client.schema.delete_class("KnowledgeBase")
        print("🗑️  Limpiando datos anteriores...")
    except:
        pass
    
    # Crear schema
    schema = {
        "class": "KnowledgeBase",
        "description": "Base de conocimiento técnico",
        "vectorizer": "text2vec-transformers",
        "properties": [
            {
                "name": "category",
                "dataType": ["string"],
                "description": "Categoría del documento"
            },
            {
                "name": "question",
                "dataType": ["text"],
                "description": "Pregunta o tema"
            },
            {
                "name": "answer",
                "dataType": ["text"],
                "description": "Respuesta o contenido"
            }
        ]
    }
    
    client.schema.create(schema)
    print("📋 Schema creado")
    
    # Base de conocimiento técnico
    knowledge_items = [
        {
            "category": "Docker",
            "question": "¿Qué es Docker?",
            "answer": "Docker es una plataforma de contenedores que permite empaquetar "
                     "aplicaciones con todas sus dependencias en un contenedor aislado. "
                     "Esto garantiza que la aplicación funcionará igual en cualquier entorno."
        },
        {
            "category": "Docker",
            "question": "¿Cómo instalar Docker?",
            "answer": "Para instalar Docker en Ubuntu: 1) Actualiza paquetes con "
                     "'sudo apt update', 2) Instala Docker con 'sudo apt install docker.io', "
                     "3) Verifica la instalación con 'docker --version'."
        },
        {
            "category": "Docker",
            "question": "¿Cómo crear un contenedor?",
            "answer": "Para crear y ejecutar un contenedor: usa 'docker run -d --name "
                     "mi_contenedor imagen:tag'. La opción -d ejecuta en segundo plano, "
                     "--name asigna un nombre personalizado."
        },
        {
            "category": "Python",
            "question": "¿Qué es Python?",
            "answer": "Python es un lenguaje de programación interpretado, de alto nivel "
                     "y propósito general. Es conocido por su sintaxis clara y legible, "
                     "lo que lo hace ideal para principiantes y expertos."
        },
        {
            "category": "Python",
            "question": "¿Cómo crear un entorno virtual en Python?",
            "answer": "Para crear un entorno virtual: 1) Ejecuta 'python -m venv nombre_env', "
                     "2) Actívalo con 'source nombre_env/bin/activate' en Linux/Mac o "
                     "'nombre_env\\Scripts\\activate' en Windows."
        },
        {
            "category": "Python",
            "question": "¿Cómo instalar paquetes en Python?",
            "answer": "Usa pip para instalar paquetes: 'pip install nombre_paquete'. "
                     "Para instalar múltiples paquetes desde un archivo, usa "
                     "'pip install -r requirements.txt'."
        },
        {
            "category": "Weaviate",
            "question": "¿Qué es Weaviate?",
            "answer": "Weaviate es una base de datos vectorial open-source que permite "
                     "almacenar objetos y vectores, facilitando búsquedas semánticas "
                     "mediante machine learning. Es ideal para aplicaciones de IA y RAG."
        },
        {
            "category": "Weaviate",
            "question": "¿Qué son los vectores en Weaviate?",
            "answer": "Los vectores son representaciones numéricas de datos (embeddings) "
                     "que capturan el significado semántico. Weaviate usa estos vectores "
                     "para encontrar objetos similares mediante búsqueda KNN."
        },
        {
            "category": "Weaviate",
            "question": "¿Cómo funciona la búsqueda semántica?",
            "answer": "La búsqueda semántica convierte tu consulta en un vector y busca "
                     "vectores similares en la base de datos. Esto permite encontrar "
                     "información por significado, no por palabras exactas."
        },
        {
            "category": "RAG",
            "question": "¿Qué es RAG?",
            "answer": "RAG (Retrieval-Augmented Generation) es una técnica que combina "
                     "búsqueda de información (retrieval) con generación de texto (LLM). "
                     "Primero busca documentos relevantes, luego usa un LLM para generar "
                     "una respuesta basada en esos documentos."
        },
        {
            "category": "RAG",
            "question": "¿Por qué usar vectores en RAG?",
            "answer": "Los vectores permiten buscar por significado semántico, no por "
                     "palabras exactas. Esto significa que puedes buscar 'cómo descansar "
                     "del trabajo' y encontrar documentos sobre 'política de vacaciones', "
                     "aunque no compartan las mismas palabras."
        },
        {
            "category": "RAG",
            "question": "¿Cuáles son las ventajas de RAG?",
            "answer": "RAG permite: 1) Acceso a información actualizada, 2) Uso de datos "
                     "privados de tu empresa, 3) Reducción de alucinaciones del LLM, "
                     "4) Respuestas verificables con fuentes, 5) No requiere re-entrenar "
                     "el modelo con cada actualización de datos."
        }
    ]
    
    # Insertar conocimiento
    print("\n📝 Insertando conocimiento en Weaviate...")
    print("   (Weaviate convierte automáticamente el texto a vectores)\n")
    
    with client.batch as batch:
        for i, item in enumerate(knowledge_items, 1):
            batch.add_data_object(
                data_object=item,
                class_name="KnowledgeBase"
            )
            print(f"   ✓ [{i}/{len(knowledge_items)}] {item['category']}: {item['question'][:50]}...")
    
    print(f"\n✅ Base de conocimiento creada con {len(knowledge_items)} documentos")
    print("   Cada documento tiene un vector de 384 dimensiones")
    
    return client


def demonstrate_semantic_search(client, user_query):
    """Demostrar búsqueda semántica (parte Retrieval de RAG)"""
    print_section(f"🔍 PASO 2: BÚSQUEDA SEMÁNTICA (RETRIEVAL)")
    
    print(f"❓ Pregunta del usuario: '{user_query}'")
    print("\n🔄 Proceso:")
    print("   1. Convertir pregunta a vector (384 dimensiones)")
    print("   2. Buscar vectores similares en Weaviate (KNN)")
    print("   3. Retornar los 3 documentos más relevantes\n")
    
    # Búsqueda semántica
    result = (
        client.query
        .get("KnowledgeBase", ["category", "question", "answer"])
        .with_near_text({"concepts": [user_query]})
        .with_limit(3)
        .with_additional(["distance", "certainty"])
        .do()
    )
    
    docs = result["data"]["Get"]["KnowledgeBase"]
    
    print("📄 Documentos encontrados (ordenados por relevancia):\n")
    
    for i, doc in enumerate(docs, 1):
        similarity = doc["_additional"]["certainty"]
        distance = doc["_additional"]["distance"]
        
        print(f"   {i}. Categoría: {doc['category']}")
        print(f"      Pregunta: {doc['question']}")
        print(f"      Similitud: {similarity:.4f} (distancia: {distance:.4f})")
        print(f"      Respuesta: {doc['answer'][:100]}...")
        print()
    
    return docs


def simulate_llm_response(user_query, relevant_docs):
    """Simular respuesta de LLM (parte Generation de RAG)"""
    print_section("🤖 PASO 3: GENERAR RESPUESTA (GENERATION)")
    
    print("💡 En un sistema RAG real, aquí:")
    print("   1. Construirías un prompt con los documentos encontrados")
    print("   2. Enviarías el prompt a un LLM (GPT-4, Claude, etc.)")
    print("   3. El LLM generaría una respuesta basada en los documentos")
    print("\n📝 Prompt que se enviaría al LLM:\n")
    
    # Construir contexto
    context = "\n\n".join([
        f"Documento {i}:\n"
        f"Categoría: {doc['category']}\n"
        f"Pregunta: {doc['question']}\n"
        f"Respuesta: {doc['answer']}"
        for i, doc in enumerate(relevant_docs, 1)
    ])
    
    prompt = f"""
Eres un asistente técnico experto. Responde la pregunta del usuario
basándote ÚNICAMENTE en el contexto proporcionado.

CONTEXTO:
{context}

PREGUNTA DEL USUARIO:
{user_query}

INSTRUCCIONES:
- Usa solo información del contexto
- Sé específico y claro
- Cita las fuentes cuando sea posible
- Si no hay suficiente información, dilo

RESPUESTA:
"""
    
    print("-" * 70)
    print(prompt)
    print("-" * 70)
    
    print("\n💬 Respuesta simulada (lo que el LLM respondería):\n")
    
    # Simular respuesta basada en el documento más relevante
    main_doc = relevant_docs[0]
    
    simulated_response = f"""
Basándome en la documentación disponible:

{main_doc['answer']}

Esta información viene de la sección "{main_doc['category']}" de nuestra 
base de conocimiento, específicamente del tema "{main_doc['question']}".

¿Necesitas más detalles sobre algún aspecto específico?
"""
    
    print(simulated_response)
    
    print("\n✅ Ventajas de esta respuesta:")
    print("   ✓ Basada en información verificable (no alucinada)")
    print("   ✓ Con fuente citada (trazable)")
    print("   ✓ Precisa y específica para la pregunta")
    print("   ✓ Se puede actualizar añadiendo nuevos documentos")


def compare_with_without_rag():
    """Comparar respuestas con y sin RAG"""
    print_section("📊 COMPARACIÓN: CON vs SIN RAG")
    
    scenarios = [
        {
            "query": "¿Cómo puedo empaquetar mi aplicación?",
            "without_rag": "Las aplicaciones se pueden empaquetar de varias formas. "
                          "Depende del lenguaje y plataforma. Podrías usar instaladores, "
                          "archivos comprimidos, o contenedores.",
            "with_rag": "Para empaquetar tu aplicación, te recomiendo usar Docker. "
                       "Docker es una plataforma de contenedores que permite empaquetar "
                       "aplicaciones con todas sus dependencias en un contenedor aislado. "
                       "Esto garantiza que funcionará igual en cualquier entorno. "
                       "[Fuente: Base de conocimiento - Docker]"
        },
        {
            "query": "¿Qué necesito para buscar por significado?",
            "without_rag": "Para buscar por significado necesitas técnicas de NLP y "
                          "posiblemente usar embeddings o vectores semánticos.",
            "with_rag": "Para búsqueda por significado, necesitas usar vectores. "
                       "Los vectores son representaciones numéricas que capturan el "
                       "significado semántico. Una base de datos vectorial como Weaviate "
                       "convierte tu consulta en un vector y busca vectores similares, "
                       "permitiendo encontrar información por significado, no por palabras exactas. "
                       "[Fuente: Base de conocimiento - Weaviate]"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n🔹 ESCENARIO {i}")
        print(f"❓ Pregunta: '{scenario['query']}'")
        
        print("\n❌ SIN RAG (LLM solo):")
        print(f"   {scenario['without_rag']}")
        print("   Limitaciones:")
        print("   • Respuesta genérica")
        print("   • Sin fuente verificable")
        print("   • Puede ser imprecisa")
        
        print("\n✅ CON RAG (LLM + Base de Conocimiento):")
        print(f"   {scenario['with_rag']}")
        print("   Ventajas:")
        print("   • Respuesta específica")
        print("   • Con fuente citada")
        print("   • Basada en TU documentación")
        print()


def main():
    """Demostración completa de RAG"""
    print("\n" + "╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "    🧠 DEMOSTRACIÓN: RAG (Retrieval-Augmented Generation)".ljust(69) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    
    print("""
RAG combina:
  1. RETRIEVAL: Buscar información relevante en base de datos vectorial
  2. AUGMENTED: Enriquecer el contexto con esa información
  3. GENERATION: Generar respuesta con LLM basada en el contexto
    """)
    
    # Paso 1: Crear base de conocimiento
    client = create_knowledge_base()
    if not client:
        return
    
    # Paso 2: Demostrar búsquedas
    queries = [
        "¿Cómo puedo ejecutar aplicaciones en contenedores?",
        "Necesito crear un ambiente aislado para Python",
        "¿Qué técnica permite usar información actual con LLMs?"
    ]
    
    for query in queries:
        # Retrieval
        relevant_docs = demonstrate_semantic_search(client, query)
        
        # Generation (simulado)
        simulate_llm_response(query, relevant_docs)
        
        input("\n⏸️  Presiona ENTER para continuar...")
    
    # Comparación
    compare_with_without_rag()
    
    print_section("✅ CONCLUSIÓN")
    print("""
🎯 RAG en 3 pasos:

1. 📚 INDEXACIÓN (una vez):
   - Almacenas tus documentos en Weaviate
   - Weaviate los convierte automáticamente a vectores
   
2. 🔍 RETRIEVAL (cada pregunta):
   - Usuario hace una pregunta
   - Weaviate busca documentos relevantes por similitud vectorial
   
3. 🤖 GENERATION (cada pregunta):
   - LLM recibe la pregunta + documentos relevantes
   - Genera respuesta basada en TUS datos
   - Cita las fuentes

💡 ¿Por qué vectores?
   Los vectores permiten buscar por SIGNIFICADO, no por palabras exactas.
   "contenedores" y "Docker" tienen vectores similares aunque sean palabras diferentes.

🚀 Resultado:
   Respuestas precisas, verificables y basadas en TU información.
   Sin alucinaciones, siempre actualizado.
    """)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrumpida")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
