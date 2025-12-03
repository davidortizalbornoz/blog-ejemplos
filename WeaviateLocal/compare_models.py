#!/usr/bin/env python3
"""
Script para comparar visualmente los dos modelos de transformers
Demuestra las diferencias en rendimiento y capacidad
"""

import time

def print_header(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def compare_specifications():
    """Comparar especificaciones técnicas"""
    print_header("📊 ESPECIFICACIONES TÉCNICAS")
    
    specs = {
        "Nombre": [
            "all-MiniLM-L6-v2",
            "paraphrase-multilingual-MiniLM-L12-v2"
        ],
        "Capas del Transformer": ["6 capas (L6)", "12 capas (L12)"],
        "Parámetros": ["~22 millones", "~118 millones"],
        "Dimensiones del Vector": ["384", "384"],
        "Tamaño del Modelo": ["~80 MB", "~470 MB"],
        "RAM Requerida": ["~500 MB", "~1.5 GB"],
        "Idiomas Soportados": ["Solo inglés (1)", "50+ idiomas"],
        "Entrenamiento": ["General purpose", "Paraphrase detection"],
    }
    
    # Calcular ancho de columnas
    max_label = max(len(k) for k in specs.keys())
    
    # Imprimir tabla
    print(f"{'Característica':<{max_label}}  |  Modelo 1 (L6)           |  Modelo 2 (L12-Multi)")
    print("-" * 70)
    
    for key, values in specs.items():
        print(f"{key:<{max_label}}  |  {values[0]:<23}  |  {values[1]}")


def compare_performance():
    """Comparar rendimiento estimado"""
    print_header("⚡ RENDIMIENTO ESTIMADO (CPU)")
    
    perf = [
        ("Vectorización por texto", "~15 ms", "~40 ms", "2.6x más lento"),
        ("Búsqueda KNN (P95)", "~18 ms", "~22 ms", "1.2x más lento"),
        ("Inserción 1,000 docs", "~25 seg", "~65 seg", "2.6x más lento"),
        ("Queries por segundo", "~180 QPS", "~140 QPS", "22% menos"),
        ("Throughput inserción", "~40 docs/s", "~15 docs/s", "2.6x menos"),
    ]
    
    print(f"{'Métrica':<25}  |  L6-English  |  L12-Multi  |  Diferencia")
    print("-" * 75)
    
    for metric, l6, l12, diff in perf:
        print(f"{metric:<25}  |  {l6:<11}  |  {l12:<10}  |  {diff}")


def compare_languages():
    """Comparar soporte de idiomas"""
    print_header("🌍 SOPORTE DE IDIOMAS")
    
    print("📌 all-MiniLM-L6-v2:")
    print("   • Inglés: ✅ ⭐⭐⭐⭐⭐ (Excelente)")
    print("   • Español: ❌ (No funciona bien)")
    print("   • Otros idiomas: ❌ (No funciona)")
    print("   • Cross-language: ❌ (No soportado)")
    
    print("\n📌 paraphrase-multilingual-MiniLM-L12-v2:")
    print("   • Inglés: ✅ ⭐⭐⭐⭐ (Muy bueno)")
    print("   • Español: ✅ ⭐⭐⭐⭐ (Muy bueno)")
    print("   • Portugués: ✅ ⭐⭐⭐⭐")
    print("   • Francés: ✅ ⭐⭐⭐⭐")
    print("   • Alemán: ✅ ⭐⭐⭐⭐")
    print("   • Italiano: ✅ ⭐⭐⭐⭐")
    print("   • Chino: ✅ ⭐⭐⭐⭐")
    print("   • Japonés: ✅ ⭐⭐⭐")
    print("   • Árabe: ✅ ⭐⭐⭐⭐")
    print("   • Ruso: ✅ ⭐⭐⭐⭐")
    print("   • + 40 idiomas más...")
    print("   • Cross-language: ✅ ⭐⭐⭐⭐⭐ (¡Busca en español, encuentra en inglés!)")


def demonstrate_use_cases():
    """Demostrar casos de uso"""
    print_header("🎯 CASOS DE USO RECOMENDADOS")
    
    print("✅ USA all-MiniLM-L6-v2 PARA:")
    cases_l6 = [
        "Aplicación 100% en inglés",
        "Documentación técnica en inglés",
        "Chatbot corporativo (inglés)",
        "Sistema de búsqueda de código (comentarios en inglés)",
        "FAQ en inglés",
        "Búsqueda de productos (descripciones en inglés)",
        "Cuando la velocidad es CRÍTICA",
        "Servidores con RAM limitada",
        "Alto volumen de consultas concurrentes"
    ]
    
    for i, case in enumerate(cases_l6, 1):
        print(f"   {i}. {case}")
    
    print("\n✅ USA paraphrase-multilingual-MiniLM-L12-v2 PARA:")
    cases_multi = [
        "Aplicaciones en español (Latinoamérica/España)",
        "Contenido multiidioma (español + inglés)",
        "Búsqueda cross-language (buscar en un idioma, encontrar en otro)",
        "Detección de paráfrasis y duplicados",
        "Contenido internacional (múltiples mercados)",
        "Documentación traducida a varios idiomas",
        "Soporte multiidioma (helpdesk, FAQ)",
        "Análisis de redes sociales globales",
        "E-commerce internacional"
    ]
    
    for i, case in enumerate(cases_multi, 1):
        print(f"   {i}. {case}")


def show_example_scenarios():
    """Mostrar escenarios de ejemplo"""
    print_header("📝 EJEMPLOS PRÁCTICOS")
    
    print("🔹 ESCENARIO 1: Búsqueda en Blog Técnico (Inglés)")
    print("   Contenido: 'Introduction to neural networks and deep learning'")
    print("   Query: 'AI and machine learning'")
    print("   ")
    print("   Con L6-English:  ✅ ⭐⭐⭐⭐⭐ EXCELENTE")
    print("   Con L12-Multi:   ✅ ⭐⭐⭐⭐ MUY BUENO (pero más lento)")
    print("   Recomendación:   → Usa L6-English (mejor rendimiento)")
    
    print("\n🔹 ESCENARIO 2: E-commerce en Español")
    print("   Contenido: 'Zapatillas deportivas para correr, cómodas y ligeras'")
    print("   Query: 'zapatos para running'")
    print("   ")
    print("   Con L6-English:  ❌ ⭐⭐ MALO (no entiende español)")
    print("   Con L12-Multi:   ✅ ⭐⭐⭐⭐⭐ EXCELENTE")
    print("   Recomendación:   → Usa L12-Multi (imprescindible)")
    
    print("\n🔹 ESCENARIO 3: Documentación Bilingüe (ES + EN)")
    print("   Contenido mixto:")
    print("     - 'Instalación de Docker en Ubuntu' (español)")
    print("     - 'Docker installation on Ubuntu' (inglés)")
    print("   Query: 'cómo instalar docker'")
    print("   ")
    print("   Con L6-English:  ❌ Solo encuentra docs en inglés")
    print("   Con L12-Multi:   ✅ Encuentra ambos (cross-language!)")
    print("   Recomendación:   → Usa L12-Multi (búsqueda unificada)")
    
    print("\n🔹 ESCENARIO 4: Sistema de Alta Concurrencia")
    print("   Tráfico: 10,000 queries/minuto (167 QPS)")
    print("   Idioma: Solo inglés")
    print("   Hardware: CPU estándar (sin GPU)")
    print("   ")
    print("   Con L6-English:  ✅ 180 QPS → Soporta la carga")
    print("   Con L12-Multi:   ⚠️  140 QPS → Necesitarías más servidores")
    print("   Recomendación:   → Usa L6-English (mejor throughput)")


def show_architecture_difference():
    """Mostrar diferencia arquitectural"""
    print_header("🏗️  ARQUITECTURA DEL TRANSFORMER")
    
    print("📊 all-MiniLM-L6-v2 (6 capas):")
    print("""
    Input: "machine learning"
         ↓
    [Embedding Layer]
         ↓
    [Transformer Layer 1]  ← Atención superficial
    [Transformer Layer 2]
    [Transformer Layer 3]
    [Transformer Layer 4]
    [Transformer Layer 5]
    [Transformer Layer 6]  ← Atención final
         ↓
    [Pooling]
         ↓
    Output: [384 dimensiones]
    
    ⚡ Más rápido pero menos contexto
    """)
    
    print("\n" + "-" * 70 + "\n")
    
    print("📊 paraphrase-multilingual-MiniLM-L12-v2 (12 capas):")
    print("""
    Input: "aprendizaje automático"
         ↓
    [Embedding Layer] ← Embedding multilingüe
         ↓
    [Transformer Layer 1]  ← Atención superficial
    [Transformer Layer 2]
    [Transformer Layer 3]
    [Transformer Layer 4]
    [Transformer Layer 5]
    [Transformer Layer 6]
    [Transformer Layer 7]  ← Contexto intermedio
    [Transformer Layer 8]
    [Transformer Layer 9]
    [Transformer Layer 10]
    [Transformer Layer 11]
    [Transformer Layer 12] ← Contexto profundo
         ↓
    [Pooling]
         ↓
    Output: [384 dimensiones]
    
    🎯 Más lento pero mejor comprensión
    """)


def show_docker_compose_difference():
    """Mostrar diferencia en docker-compose"""
    print_header("🐳 DIFERENCIA EN DOCKER-COMPOSE")
    
    print("📄 docker-compose.yml (Principal):")
    print("""
services:
  t2v-transformers:
    image: semitechnologies/transformers-inference:sentence-transformers-all-MiniLM-L6-v2
    #                                                                            ^^^^
    #                                                                            L6 = 6 capas
    environment:
      ENABLE_CUDA: '0'
    """)
    
    print("   Características:")
    print("   • Modelo ligero y rápido")
    print("   • Solo inglés")
    print("   • ~80 MB de imagen Docker")
    print("   • ~500 MB RAM en runtime")
    print()
    
    print("📄 docker-compose-multilingual.yml:")
    print("""
services:
  t2v-transformers:
    image: semitechnologies/transformers-inference:sentence-transformers-paraphrase-multilingual-MiniLM-L12-v2
    #                                                                            ^^^^^^^^^^^^  ^^^^
    #                                                                            Multilingual  L12 = 12 capas
    environment:
      ENABLE_CUDA: '0'
    """)
    
    print("   Características:")
    print("   • Modelo más pesado pero multilingüe")
    print("   • 50+ idiomas incluido español")
    print("   • ~470 MB de imagen Docker")
    print("   • ~1.5 GB RAM en runtime")


def show_decision_tree():
    """Árbol de decisión visual"""
    print_header("🌳 ÁRBOL DE DECISIÓN")
    
    print("""
                    ¿Qué modelo usar?
                           |
                           |
        ¿Tu contenido incluye idiomas además de inglés?
                           |
                 ┌─────────┴─────────┐
                 |                   |
               NO (solo inglés)    SÍ (multiidioma)
                 |                   |
                 |                   └──→ paraphrase-multilingual-MiniLM-L12-v2
                 |                         (docker-compose-multilingual.yml)
                 |
     ¿Necesitas máxima velocidad?
                 |
         ┌───────┴───────┐
         |               |
       SÍ              NO
         |               |
         |               └──→ ¿Qué es más importante?
         |                              |
         |                      ┌───────┴───────┐
         |                      |               |
         |                 Velocidad        Calidad
         |                      |               |
         └──────────────────────┘               |
                 |                               |
    all-MiniLM-L6-v2                ¿Tienes GPU disponible?
    (docker-compose.yml)                        |
                                        ┌───────┴───────┐
                                        |               |
                                      SÍ              NO
                                        |               |
                                    Cualquiera      L6 (más rápido)
                                   con GPU          
    """)


def show_migration_guide():
    """Guía de migración entre modelos"""
    print_header("🔄 CÓMO CAMBIAR DE MODELO")
    
    print("⚠️  IMPORTANTE: Los vectores de diferentes modelos NO son compatibles")
    print("    Si cambias de modelo, debes re-indexar todos tus datos.\n")
    
    print("📋 PASOS PARA CAMBIAR DE L6 a L12-Multilingual:")
    print("""
    1. Detener Weaviate:
       $ docker-compose down
    
    2. Limpiar datos existentes (vectores incompatibles):
       $ docker-compose down -v
       
       ⚠️  Esto borrará TODOS los datos!
       
    3. Iniciar con modelo multilingüe:
       $ docker-compose -f docker-compose-multilingual.yml up -d
    
    4. Esperar que esté listo (~30 segundos):
       $ curl http://localhost:8080/v1/.well-known/ready
    
    5. Re-insertar todos tus datos:
       $ python3 tu_script_de_insercion.py
    """)
    
    print("\n📋 PASOS PARA CAMBIAR DE L12-Multilingual a L6:")
    print("""
    1. Detener Weaviate:
       $ docker-compose -f docker-compose-multilingual.yml down
    
    2. Limpiar datos:
       $ docker-compose -f docker-compose-multilingual.yml down -v
    
    3. Iniciar con modelo inglés:
       $ docker-compose up -d
    
    4. Re-insertar datos
    """)


def show_cost_analysis():
    """Análisis de costos"""
    print_header("💰 ANÁLISIS DE COSTOS")
    
    print("📊 Costo de Infraestructura (servidor dedicado):\n")
    
    print("Escenario: 1 millón de documentos, 100K queries/día\n")
    
    print("Con all-MiniLM-L6-v2:")
    print("   • RAM necesaria: ~8 GB")
    print("   • CPU: 4 cores suficiente")
    print("   • Servidor AWS: t3.large (~$60/mes)")
    print("   • Latencia: ~15-20ms")
    print("   • Total: ~$60/mes")
    
    print("\nCon paraphrase-multilingual-MiniLM-L12-v2:")
    print("   • RAM necesaria: ~16 GB")
    print("   • CPU: 8 cores recomendado")
    print("   • Servidor AWS: t3.xlarge (~$120/mes)")
    print("   • Latencia: ~35-45ms")
    print("   • Total: ~$120/mes")
    
    print("\n💡 Diferencia: ~$60/mes (2x costo)")
    print("   Pero obtienes: Soporte multiidioma + búsqueda cross-language")


def main():
    """Función principal"""
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "    🔬 COMPARACIÓN DETALLADA DE MODELOS TRANSFORMER".ljust(69) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    
    compare_specifications()
    compare_performance()
    compare_languages()
    demonstrate_use_cases()
    show_example_scenarios()
    show_architecture_difference()
    show_docker_compose_difference()
    show_decision_tree()
    show_migration_guide()
    show_cost_analysis()
    
    print_header("✅ RESUMEN EJECUTIVO")
    
    print("""
📌 CONCLUSIÓN:

1. all-MiniLM-L6-v2 (docker-compose.yml):
   ✅ Usa si tu contenido es 100% inglés
   ✅ Prioridad: Velocidad y eficiencia
   ✅ Menor costo de infraestructura
   
2. paraphrase-multilingual-MiniLM-L12-v2 (docker-compose-multilingual.yml):
   ✅ Usa si tienes contenido en español o multiidioma
   ✅ Prioridad: Calidad y cobertura de idiomas
   ✅ Búsqueda cross-language

🎯 Para Latinoamérica: SIEMPRE usa el modelo multilingual
   La diferencia en calidad supera ampliamente el costo de rendimiento.

📞 ¿Dudas sobre cuál usar? Pregunta considerando:
   • Idioma(s) de tu contenido
   • Volumen de consultas esperado
   • Hardware disponible
   • Presupuesto de infraestructura
    """)
    
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    main()
