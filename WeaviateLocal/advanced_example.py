#!/usr/bin/env python3
"""
Ejemplo avanzado de Weaviate - Casos de uso complejos
"""

import weaviate
import numpy as np
from datetime import datetime, timedelta
import random


WEAVIATE_URL = "http://localhost:8080"


def connect():
    """Conectar a Weaviate"""
    client = weaviate.Client(WEAVIATE_URL)
    if client.is_ready():
        print("✅ Conectado a Weaviate")
        return client
    else:
        raise Exception("No se pudo conectar a Weaviate")


def create_advanced_schema(client):
    """Crear schema más complejo con múltiples clases"""
    print("\n📋 Creando schema avanzado...")
    
    # Limpiar schemas anteriores
    try:
        client.schema.delete_class("Article")
        client.schema.delete_class("Author")
        client.schema.delete_class("Category")
    except:
        pass
    
    # Schema para Categorías
    category_schema = {
        "class": "Category",
        "description": "Categorías de contenido",
        "vectorizer": "text2vec-transformers",
        "properties": [
            {
                "name": "name",
                "dataType": ["text"],
                "description": "Nombre de la categoría"
            },
            {
                "name": "description",
                "dataType": ["text"],
                "description": "Descripción de la categoría"
            }
        ]
    }
    
    # Schema para Autores
    author_schema = {
        "class": "Author",
        "description": "Autores de artículos",
        "vectorizer": "text2vec-transformers",
        "properties": [
            {
                "name": "name",
                "dataType": ["string"],
                "description": "Nombre del autor"
            },
            {
                "name": "bio",
                "dataType": ["text"],
                "description": "Biografía del autor"
            },
            {
                "name": "email",
                "dataType": ["string"],
                "description": "Email del autor"
            }
        ]
    }
    
    # Schema para Artículos con referencias
    article_schema = {
        "class": "Article",
        "description": "Artículos técnicos",
        "vectorizer": "text2vec-transformers",
        "properties": [
            {
                "name": "title",
                "dataType": ["text"],
                "description": "Título del artículo"
            },
            {
                "name": "content",
                "dataType": ["text"],
                "description": "Contenido del artículo"
            },
            {
                "name": "publishDate",
                "dataType": ["date"],
                "description": "Fecha de publicación"
            },
            {
                "name": "views",
                "dataType": ["int"],
                "description": "Número de vistas"
            },
            {
                "name": "rating",
                "dataType": ["number"],
                "description": "Calificación promedio"
            },
            {
                "name": "tags",
                "dataType": ["string[]"],
                "description": "Etiquetas del artículo"
            },
            {
                "name": "author",
                "dataType": ["Author"],
                "description": "Autor del artículo"
            },
            {
                "name": "category",
                "dataType": ["Category"],
                "description": "Categoría del artículo"
            }
        ]
    }
    
    # Crear schemas
    client.schema.create_class(category_schema)
    client.schema.create_class(author_schema)
    client.schema.create_class(article_schema)
    
    print("✅ Schema avanzado creado")


def insert_complex_data(client):
    """Insertar datos con referencias cruzadas"""
    print("\n📝 Insertando datos complejos...")
    
    # Crear categorías
    categories = []
    cat_data = [
        {"name": "Machine Learning", "description": "Artículos sobre aprendizaje automático y modelos predictivos"},
        {"name": "Web Development", "description": "Desarrollo web, frameworks y mejores prácticas"},
        {"name": "DevOps", "description": "Infraestructura, CI/CD y automatización"},
        {"name": "Data Science", "description": "Análisis de datos, visualización y estadística"}
    ]
    
    for cat in cat_data:
        result = client.data_object.create(
            data_object=cat,
            class_name="Category"
        )
        categories.append(result)
        print(f"   ✓ Categoría: {cat['name']}")
    
    # Crear autores
    authors = []
    author_data = [
        {
            "name": "Ana García",
            "bio": "Ingeniera de ML con 10 años de experiencia en deep learning",
            "email": "ana@example.com"
        },
        {
            "name": "Carlos Rodríguez",
            "bio": "Desarrollador full-stack especializado en React y Node.js",
            "email": "carlos@example.com"
        },
        {
            "name": "María López",
            "bio": "DevOps engineer apasionada por Kubernetes y automatización",
            "email": "maria@example.com"
        }
    ]
    
    for author in author_data:
        result = client.data_object.create(
            data_object=author,
            class_name="Author"
        )
        authors.append(result)
        print(f"   ✓ Autor: {author['name']}")
    
    # Crear artículos con referencias
    articles_data = [
        {
            "title": "Introducción a Redes Neuronales Convolucionales",
            "content": "Las CNN son fundamentales en visión computacional. Aprenden características jerárquicas de las imágenes mediante capas de convolución, pooling y fully connected.",
            "tags": ["CNN", "Deep Learning", "Vision"],
            "views": 1500,
            "rating": 4.8,
            "author_idx": 0,
            "category_idx": 0
        },
        {
            "title": "Building Modern React Applications",
            "content": "React Hooks han revolucionado el desarrollo. useState, useEffect y custom hooks permiten crear componentes funcionales poderosos y reutilizables.",
            "tags": ["React", "JavaScript", "Frontend"],
            "views": 2300,
            "rating": 4.6,
            "author_idx": 1,
            "category_idx": 1
        },
        {
            "title": "Kubernetes: Orquestación de Contenedores",
            "content": "Kubernetes automatiza el despliegue, escalado y gestión de aplicaciones containerizadas. Pods, Services y Deployments son conceptos clave.",
            "tags": ["Kubernetes", "Docker", "Cloud"],
            "views": 1800,
            "rating": 4.9,
            "author_idx": 2,
            "category_idx": 2
        },
        {
            "title": "Transfer Learning en NLP",
            "content": "Transformers pre-entrenados como BERT y GPT han transformado el NLP. Fine-tuning permite adaptar modelos a tareas específicas con pocos datos.",
            "tags": ["NLP", "Transformers", "BERT"],
            "views": 2100,
            "rating": 4.7,
            "author_idx": 0,
            "category_idx": 0
        },
        {
            "title": "Data Visualization con Python",
            "content": "Matplotlib, Seaborn y Plotly ofrecen herramientas poderosas para visualización. Los dashboards interactivos mejoran la comunicación de insights.",
            "tags": ["Python", "Visualization", "Analytics"],
            "views": 1200,
            "rating": 4.5,
            "author_idx": 0,
            "category_idx": 3
        }
    ]
    
    for article in articles_data:
        # Calcular fecha aleatoria en los últimos 90 días
        days_ago = random.randint(1, 90)
        publish_date = (datetime.now() - timedelta(days=days_ago)).isoformat() + "Z"
        
        # Preparar objeto con referencias
        article_obj = {
            "title": article["title"],
            "content": article["content"],
            "publishDate": publish_date,
            "views": article["views"],
            "rating": article["rating"],
            "tags": article["tags"]
        }
        
        # Añadir referencias a autor y categoría
        client.data_object.create(
            data_object=article_obj,
            class_name="Article",
            uuid=None
        )
        
        # Obtener UUID del último artículo creado
        result = client.query.get("Article", ["title"]) \
            .with_limit(1) \
            .with_sort([{"path": ["publishDate"], "order": "desc"}]) \
            .with_additional(["id"]) \
            .do()
        
        if result["data"]["Get"]["Article"]:
            article_uuid = result["data"]["Get"]["Article"][0]["_additional"]["id"]
            
            # Añadir referencia al autor
            client.data_object.reference.add(
                from_class_name="Article",
                from_uuid=article_uuid,
                from_property_name="author",
                to_class_name="Author",
                to_uuid=authors[article["author_idx"]]
            )
            
            # Añadir referencia a la categoría
            client.data_object.reference.add(
                from_class_name="Article",
                from_uuid=article_uuid,
                from_property_name="category",
                to_class_name="Category",
                to_uuid=categories[article["category_idx"]]
            )
            
            print(f"   ✓ Artículo: {article['title']}")
    
    print(f"✅ {len(articles_data)} artículos insertados con referencias")


def search_with_filters(client):
    """Búsquedas avanzadas con filtros múltiples"""
    print("\n🔍 Búsquedas con filtros avanzados")
    print("=" * 60)
    
    # Filtro 1: Artículos con alta calificación
    print("\n1️⃣  Artículos con rating > 4.7:")
    result = (
        client.query
        .get("Article", ["title", "rating", "views"])
        .with_where({
            "path": ["rating"],
            "operator": "GreaterThan",
            "valueNumber": 4.7
        })
        .with_sort([{"path": ["rating"], "order": "desc"}])
        .do()
    )
    
    for article in result["data"]["Get"]["Article"]:
        print(f"   • {article['title']} (⭐ {article['rating']})")
    
    # Filtro 2: Artículos recientes
    print("\n2️⃣  Artículos de los últimos 30 días:")
    thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat() + "Z"
    
    result = (
        client.query
        .get("Article", ["title", "publishDate", "views"])
        .with_where({
            "path": ["publishDate"],
            "operator": "GreaterThan",
            "valueDate": thirty_days_ago
        })
        .with_sort([{"path": ["publishDate"], "order": "desc"}])
        .do()
    )
    
    for article in result["data"]["Get"]["Article"]:
        print(f"   • {article['title']} ({article['publishDate'][:10]})")
    
    # Filtro 3: Búsqueda semántica con filtro de popularidad
    print("\n3️⃣  Artículos sobre 'machine learning' con más de 1500 vistas:")
    result = (
        client.query
        .get("Article", ["title", "views"])
        .with_near_text({"concepts": ["machine learning deep learning"]})
        .with_where({
            "path": ["views"],
            "operator": "GreaterThan",
            "valueInt": 1500
        })
        .with_limit(3)
        .with_additional(["certainty"])
        .do()
    )
    
    for article in result["data"]["Get"]["Article"]:
        print(f"   • {article['title']}")
        print(f"     Vistas: {article['views']} | Similitud: {article['_additional']['certainty']:.4f}")


def search_with_references(client):
    """Búsquedas incluyendo referencias cruzadas"""
    print("\n🔗 Búsquedas con referencias")
    print("=" * 60)
    
    # Obtener artículos con información del autor
    print("\n1️⃣  Artículos con información del autor:")
    result = (
        client.query
        .get("Article", [
            "title",
            "rating",
            "author { ... on Author { name email } }",
            "category { ... on Category { name } }"
        ])
        .with_limit(3)
        .do()
    )
    
    for article in result["data"]["Get"]["Article"]:
        author = article.get("author", [{}])[0] if article.get("author") else {}
        category = article.get("category", [{}])[0] if article.get("category") else {}
        
        print(f"\n   📄 {article['title']}")
        print(f"      Autor: {author.get('name', 'N/A')}")
        print(f"      Categoría: {category.get('name', 'N/A')}")
        print(f"      Rating: ⭐ {article['rating']}")


def aggregate_statistics(client):
    """Agregaciones y estadísticas"""
    print("\n📊 Estadísticas agregadas")
    print("=" * 60)
    
    # Estadísticas generales
    print("\n1️⃣  Estadísticas de artículos:")
    result = (
        client.query
        .aggregate("Article")
        .with_fields("meta { count } rating { mean maximum minimum } views { sum mean }")
        .do()
    )
    
    stats = result["data"]["Aggregate"]["Article"][0]
    print(f"   Total de artículos: {stats['meta']['count']}")
    print(f"   Rating promedio: {stats['rating']['mean']:.2f}")
    print(f"   Rating máximo: {stats['rating']['maximum']:.2f}")
    print(f"   Total de vistas: {stats['views']['sum']}")
    print(f"   Vistas promedio: {stats['views']['mean']:.0f}")
    
    # Agrupar por categoría
    print("\n2️⃣  Artículos por categoría:")
    result = (
        client.query
        .aggregate("Article")
        .with_fields("meta { count } rating { mean }")
        .with_group_by_filter(["category"])
        .do()
    )
    
    for group in result["data"]["Aggregate"]["Article"]:
        print(f"   • Categoría: {group['groupedBy']['value']}")
        print(f"     Artículos: {group['meta']['count']} | Rating promedio: {group['rating']['mean']:.2f}")


def hybrid_search(client):
    """Búsqueda híbrida (vectorial + keyword)"""
    print("\n🎯 Búsqueda híbrida (vectorial + BM25)")
    print("=" * 60)
    
    query = "neural networks deep learning"
    
    # Búsqueda híbrida
    result = (
        client.query
        .get("Article", ["title", "content"])
        .with_hybrid(
            query=query,
            alpha=0.5  # 0.5 = 50% vectorial, 50% keyword
        )
        .with_limit(3)
        .with_additional(["score"])
        .do()
    )
    
    print(f"\n   Query: '{query}'")
    print(f"   Alpha: 0.5 (balance entre vectorial y keyword)\n")
    
    if result["data"]["Get"]["Article"]:
        for i, article in enumerate(result["data"]["Get"]["Article"], 1):
            print(f"   {i}. {article['title']}")
            print(f"      Score: {article['_additional']['score']:.4f}")
            print(f"      Preview: {article['content'][:80]}...\n")


def main():
    """Función principal"""
    print("=" * 60)
    print("🚀 DEMO AVANZADA: Weaviate Features Completas")
    print("=" * 60)
    
    client = connect()
    
    # Setup
    create_advanced_schema(client)
    insert_complex_data(client)
    
    # Búsquedas y análisis
    search_with_filters(client)
    search_with_references(client)
    aggregate_statistics(client)
    hybrid_search(client)
    
    print("\n" + "=" * 60)
    print("✅ Demo avanzada completada!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
