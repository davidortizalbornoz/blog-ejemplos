#!/usr/bin/env python3
"""
Ejemplo completo de uso de Weaviate con text2vec-transformers
"""

import weaviate
import json
from datetime import datetime

# Configuración
WEAVIATE_URL = "http://localhost:8080"


def connect_to_weaviate():
    """Conectar a Weaviate local"""
    print("🔌 Conectando a Weaviate...")
    client = weaviate.Client(WEAVIATE_URL)
    
    if client.is_ready():
        print("✅ Conexión exitosa!")
        return client
    else:
        print("❌ Error: Weaviate no está disponible")
        print("   Ejecuta: docker-compose up -d")
        return None


def create_schema(client):
    """Crear schema para documentos"""
    print("\n📋 Creando schema...")
    
    # Eliminar schema anterior si existe
    try:
        client.schema.delete_class("Document")
        print("   Schema anterior eliminado")
    except:
        pass
    
    schema = {
        "classes": [
            {
                "class": "Document",
                "description": "Documentos con vectorización automática",
                "vectorizer": "text2vec-transformers",
                "moduleConfig": {
                    "text2vec-transformers": {
                        "vectorizeClassName": False,
                        "poolingStrategy": "masked_mean"
                    }
                },
                "properties": [
                    {
                        "name": "title",
                        "dataType": ["text"],
                        "description": "Título del documento",
                        "moduleConfig": {
                            "text2vec-transformers": {
                                "skip": False,
                                "vectorizePropertyName": False
                            }
                        }
                    },
                    {
                        "name": "content",
                        "dataType": ["text"],
                        "description": "Contenido del documento",
                        "moduleConfig": {
                            "text2vec-transformers": {
                                "skip": False,
                                "vectorizePropertyName": False
                            }
                        }
                    },
                    {
                        "name": "category",
                        "dataType": ["string"],
                        "description": "Categoría del documento"
                    },
                    {
                        "name": "timestamp",
                        "dataType": ["date"],
                        "description": "Fecha de creación"
                    }
                ]
            }
        ]
    }
    
    client.schema.create(schema)
    print("✅ Schema creado exitosamente")


def insert_sample_data(client):
    """Insertar datos de ejemplo"""
    print("\n📝 Insertando datos de ejemplo...")
    
    documents = [
        {
            "title": "Introducción a Python",
            "content": "Python es un lenguaje de programación interpretado, de alto nivel y propósito general. Su filosofía de diseño enfatiza la legibilidad del código.",
            "category": "Programación"
        },
        {
            "title": "Bases de Datos Vectoriales",
            "content": "Las bases de datos vectoriales están diseñadas para almacenar y buscar vectores de alta dimensionalidad. Son ideales para búsqueda semántica y aplicaciones de IA.",
            "category": "Tecnología"
        },
        {
            "title": "Machine Learning Básico",
            "content": "El aprendizaje automático es una rama de la inteligencia artificial que permite a las máquinas aprender de datos sin ser programadas explícitamente.",
            "category": "IA"
        },
        {
            "title": "Redes Neuronales",
            "content": "Las redes neuronales artificiales son modelos computacionales inspirados en el cerebro humano. Consisten en capas de nodos interconectados.",
            "category": "IA"
        },
        {
            "title": "Docker y Contenedores",
            "content": "Docker es una plataforma que permite desarrollar, enviar y ejecutar aplicaciones en contenedores. Los contenedores empaquetan el código y todas sus dependencias.",
            "category": "DevOps"
        },
        {
            "title": "Algoritmos KNN",
            "content": "K-Nearest Neighbors es un algoritmo de clasificación que encuentra los K ejemplos más cercanos en el espacio de características para hacer predicciones.",
            "category": "Algoritmos"
        },
        {
            "title": "Procesamiento de Lenguaje Natural",
            "content": "NLP es un campo de la IA que se enfoca en la interacción entre computadoras y lenguaje humano. Incluye tareas como traducción, análisis de sentimiento y respuesta a preguntas.",
            "category": "IA"
        },
        {
            "title": "GraphQL y APIs",
            "content": "GraphQL es un lenguaje de consulta para APIs que permite a los clientes solicitar exactamente los datos que necesitan. Es una alternativa a REST.",
            "category": "Programación"
        }
    ]
    
    # Insertar documentos con batch
    with client.batch as batch:
        batch.batch_size = 100
        
        for i, doc in enumerate(documents, 1):
            doc["timestamp"] = datetime.now().isoformat() + "Z"
            
            batch.add_data_object(
                data_object=doc,
                class_name="Document"
            )
            
            print(f"   ✓ Documento {i}/{len(documents)}: {doc['title']}")
    
    print(f"✅ {len(documents)} documentos insertados")


def semantic_search(client, query, limit=3):
    """Realizar búsqueda semántica"""
    print(f"\n🔍 Buscando: '{query}'")
    print(f"   Límite: {limit} resultados\n")
    
    result = (
        client.query
        .get("Document", ["title", "content", "category"])
        .with_near_text({"concepts": [query]})
        .with_limit(limit)
        .with_additional(["distance", "certainty"])
        .do()
    )
    
    if "data" in result and "Get" in result["data"]:
        documents = result["data"]["Get"]["Document"]
        
        for i, doc in enumerate(documents, 1):
            print(f"📄 Resultado {i}:")
            print(f"   Título: {doc['title']}")
            print(f"   Categoría: {doc['category']}")
            print(f"   Similitud: {doc['_additional']['certainty']:.4f}")
            print(f"   Distancia: {doc['_additional']['distance']:.4f}")
            print(f"   Contenido: {doc['content'][:100]}...")
            print()
    else:
        print("❌ No se encontraron resultados")


def search_with_filter(client, query, category):
    """Búsqueda con filtros"""
    print(f"\n🔍 Búsqueda filtrada: '{query}' en categoría '{category}'")
    
    where_filter = {
        "path": ["category"],
        "operator": "Equal",
        "valueString": category
    }
    
    result = (
        client.query
        .get("Document", ["title", "content", "category"])
        .with_near_text({"concepts": [query]})
        .with_where(where_filter)
        .with_limit(5)
        .with_additional(["certainty"])
        .do()
    )
    
    if "data" in result and "Get" in result["data"]:
        documents = result["data"]["Get"]["Document"]
        print(f"\n   Encontrados {len(documents)} resultados:\n")
        
        for doc in documents:
            print(f"   • {doc['title']} (similitud: {doc['_additional']['certainty']:.4f})")
    else:
        print("   No se encontraron resultados")


def aggregate_by_category(client):
    """Agregar documentos por categoría"""
    print("\n📊 Agregando por categoría...")
    
    result = (
        client.query
        .aggregate("Document")
        .with_fields("meta { count }")
        .with_group_by_filter(["category"])
        .do()
    )
    
    if "data" in result and "Aggregate" in result["data"]:
        groups = result["data"]["Aggregate"]["Document"]
        print()
        for group in groups:
            category = group["groupedBy"]["value"]
            count = group["meta"]["count"]
            print(f"   • {category}: {count} documento(s)")


def get_schema_info(client):
    """Obtener información del schema"""
    print("\n📋 Información del Schema:")
    
    schema = client.schema.get()
    
    for cls in schema["classes"]:
        print(f"\n   Clase: {cls['class']}")
        print(f"   Vectorizador: {cls.get('vectorizer', 'N/A')}")
        print(f"   Propiedades:")
        for prop in cls["properties"]:
            print(f"      • {prop['name']} ({', '.join(prop['dataType'])})")


def main():
    """Función principal"""
    print("=" * 60)
    print("🚀 DEMO: Weaviate con text2vec-transformers")
    print("=" * 60)
    
    # Conectar
    client = connect_to_weaviate()
    if not client:
        return
    
    # Crear schema
    create_schema(client)
    
    # Obtener info del schema
    get_schema_info(client)
    
    # Insertar datos
    insert_sample_data(client)
    
    # Agregar por categoría
    aggregate_by_category(client)
    
    # Ejemplos de búsqueda semántica
    print("\n" + "=" * 60)
    print("🔍 EJEMPLOS DE BÚSQUEDA SEMÁNTICA")
    print("=" * 60)
    
    semantic_search(client, "inteligencia artificial y aprendizaje", limit=3)
    semantic_search(client, "desarrollo de software", limit=3)
    semantic_search(client, "algoritmos de búsqueda", limit=3)
    
    # Búsqueda con filtro
    print("\n" + "=" * 60)
    print("🎯 BÚSQUEDA CON FILTROS")
    print("=" * 60)
    search_with_filter(client, "aprendizaje automático", "IA")
    
    print("\n" + "=" * 60)
    print("✅ Demo completada!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
