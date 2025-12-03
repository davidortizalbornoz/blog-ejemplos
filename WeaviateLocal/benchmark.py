#!/usr/bin/env python3
"""
Benchmark de Weaviate - Pruebas de rendimiento
"""

import weaviate
import time
import random
import string
from datetime import datetime


WEAVIATE_URL = "http://localhost:8080"


def generate_random_text(words=50):
    """Generar texto aleatorio"""
    word_list = ["machine", "learning", "neural", "network", "data", "science",
                 "algorithm", "model", "training", "prediction", "feature",
                 "dataset", "accuracy", "optimization", "gradient", "layer"]
    return " ".join(random.choices(word_list, k=words))


def benchmark_insert(client, num_objects=1000):
    """Benchmark de inserción"""
    print(f"\n📝 Benchmark: Inserción de {num_objects} objetos")
    print("=" * 60)
    
    # Limpiar datos anteriores
    try:
        client.schema.delete_class("BenchmarkDoc")
    except:
        pass
    
    # Crear schema simple
    schema = {
        "class": "BenchmarkDoc",
        "vectorizer": "text2vec-transformers",
        "properties": [
            {"name": "title", "dataType": ["text"]},
            {"name": "content", "dataType": ["text"]},
            {"name": "index", "dataType": ["int"]}
        ]
    }
    client.schema.create(schema)
    
    # Inserción con batch
    start_time = time.time()
    
    with client.batch as batch:
        batch.batch_size = 100
        
        for i in range(num_objects):
            obj = {
                "title": f"Document {i}",
                "content": generate_random_text(),
                "index": i
            }
            batch.add_data_object(obj, "BenchmarkDoc")
            
            if (i + 1) % 100 == 0:
                print(f"   Insertados: {i + 1}/{num_objects}")
    
    elapsed = time.time() - start_time
    
    print(f"\n✅ Resultados de Inserción:")
    print(f"   Total de objetos: {num_objects}")
    print(f"   Tiempo total: {elapsed:.2f} segundos")
    print(f"   Objetos/segundo: {num_objects/elapsed:.2f}")
    print(f"   Tiempo promedio: {(elapsed/num_objects)*1000:.2f} ms/objeto")


def benchmark_search(client, num_queries=100):
    """Benchmark de búsqueda"""
    print(f"\n🔍 Benchmark: {num_queries} búsquedas semánticas")
    print("=" * 60)
    
    queries = [
        "machine learning algorithms",
        "neural network training",
        "data science optimization",
        "deep learning models",
        "predictive analytics"
    ]
    
    latencies = []
    
    for i in range(num_queries):
        query = random.choice(queries)
        
        start_time = time.time()
        
        result = (
            client.query
            .get("BenchmarkDoc", ["title"])
            .with_near_text({"concepts": [query]})
            .with_limit(10)
            .do()
        )
        
        latency = (time.time() - start_time) * 1000  # en ms
        latencies.append(latency)
        
        if (i + 1) % 20 == 0:
            print(f"   Completadas: {i + 1}/{num_queries}")
    
    # Estadísticas
    latencies.sort()
    avg_latency = sum(latencies) / len(latencies)
    p50 = latencies[len(latencies)//2]
    p95 = latencies[int(len(latencies)*0.95)]
    p99 = latencies[int(len(latencies)*0.99)]
    
    print(f"\n✅ Resultados de Búsqueda:")
    print(f"   Total de queries: {num_queries}")
    print(f"   Latencia promedio: {avg_latency:.2f} ms")
    print(f"   Latencia mínima: {min(latencies):.2f} ms")
    print(f"   Latencia máxima: {max(latencies):.2f} ms")
    print(f"   P50 (mediana): {p50:.2f} ms")
    print(f"   P95: {p95:.2f} ms")
    print(f"   P99: {p99:.2f} ms")
    print(f"   QPS (queries/seg): {1000/avg_latency:.2f}")


def benchmark_filtered_search(client, num_queries=50):
    """Benchmark de búsqueda con filtros"""
    print(f"\n🎯 Benchmark: {num_queries} búsquedas con filtros")
    print("=" * 60)
    
    latencies = []
    
    for i in range(num_queries):
        start_time = time.time()
        
        result = (
            client.query
            .get("BenchmarkDoc", ["title", "index"])
            .with_near_text({"concepts": ["machine learning"]})
            .with_where({
                "path": ["index"],
                "operator": "GreaterThan",
                "valueInt": random.randint(0, 500)
            })
            .with_limit(10)
            .do()
        )
        
        latency = (time.time() - start_time) * 1000
        latencies.append(latency)
        
        if (i + 1) % 10 == 0:
            print(f"   Completadas: {i + 1}/{num_queries}")
    
    avg_latency = sum(latencies) / len(latencies)
    
    print(f"\n✅ Resultados de Búsqueda Filtrada:")
    print(f"   Latencia promedio: {avg_latency:.2f} ms")
    print(f"   Latencia mínima: {min(latencies):.2f} ms")
    print(f"   Latencia máxima: {max(latencies):.2f} ms")


def get_storage_info(client):
    """Obtener información de almacenamiento"""
    print(f"\n💾 Información de Almacenamiento")
    print("=" * 60)
    
    # Contar objetos
    result = client.query.aggregate("BenchmarkDoc").with_meta_count().do()
    count = result["data"]["Aggregate"]["BenchmarkDoc"][0]["meta"]["count"]
    
    print(f"   Total de objetos: {count}")
    print(f"   Vectorizador: text2vec-transformers")
    print(f"   Dimensiones: 384 (MiniLM-L6-v2)")
    print(f"   Espacio estimado: ~{count * 384 * 4 / 1024 / 1024:.2f} MB (vectores)")


def main():
    """Función principal de benchmark"""
    print("=" * 60)
    print("🏁 BENCHMARK: Weaviate Performance")
    print("=" * 60)
    
    # Conectar
    client = weaviate.Client(WEAVIATE_URL)
    if not client.is_ready():
        print("❌ Weaviate no está disponible")
        return
    
    print("✅ Conectado a Weaviate")
    
    # Ejecutar benchmarks
    benchmark_insert(client, num_objects=1000)
    benchmark_search(client, num_queries=100)
    benchmark_filtered_search(client, num_queries=50)
    get_storage_info(client)
    
    print("\n" + "=" * 60)
    print("✅ Benchmark completado!")
    print("=" * 60)
    
    print("\n💡 Notas:")
    print("   - Los resultados dependen del hardware y configuración")
    print("   - Primera búsqueda puede ser más lenta (warm-up)")
    print("   - GPU mejora significativamente el rendimiento")
    print("   - Modelo más grande = mejor calidad pero más lento")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Benchmark interrumpido")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
