#!/usr/bin/env python3
"""
Aplicación principal para análisis de imágenes con YOLO.
Integra el streaming de imágenes aleatorias con detección en tiempo real.
"""

from yolo_analyzer import YoloAnalyzer
import sys

def main():
    """Función principal de la aplicación."""
    print("=== SISTEMA DE ANÁLISIS DE ANIMALES CON YOLO ===")
    print("Este sistema selecciona imágenes aleatorias de animales")
    print("y las analiza con YOLOv8 para detectar qué animal contienen.")
    print()
    
    # Configuración por defecto
    config = {
        "model_path": "yolov8n.pt",  # Modelo nano (más rápido)
        "images_dir": "imgs",
        "max_images": 15,
        "interval_seconds": 1.0,
        "confidence_threshold": 0.3
    }
    
    print("Configuración:")
    print(f"- Modelo YOLO: {config['model_path']}")
    print(f"- Directorio de imágenes: {config['images_dir']}")
    print(f"- Número de imágenes: {config['max_images']}")
    print(f"- Intervalo: {config['interval_seconds']} segundos")
    print(f"- Umbral de confianza: {config['confidence_threshold']}")
    print()
    
    try:
        # Crear el analizador
        print("Inicializando analizador YOLO...")
        analyzer = YoloAnalyzer(**config)
        
        print("¡Sistema listo!")
        print("- Se abrirá una ventana con la visualización")
        print("- Presiona 'q' para salir en cualquier momento")
        print("- Las detecciones se mostrarán con bounding boxes")
        print("- Verde = detección correcta, Rojo = detección incorrecta")
        print()
        
        input("Presiona Enter para comenzar...")
        
        # Iniciar el análisis
        analyzer.start_analysis()
        
        # Mostrar estadísticas finales
        stats = analyzer.get_statistics()
        if stats:
            print("\n" + "="*50)
            print("ESTADÍSTICAS FINALES")
            print("="*50)
            print(f"Imágenes procesadas: {stats['total_images_processed']}")
            print(f"Detecciones correctas: {stats['images_with_correct_detection']}")
            print(f"Precisión: {stats['accuracy']:.1f}%")
            print(f"Total detecciones: {stats['total_detections']}")
            print(f"Promedio detecciones/imagen: {stats['average_detections_per_image']:.1f}")
            print("="*50)
        
        print("¡Análisis completado exitosamente!")
        
    except KeyboardInterrupt:
        print("\n\nInterrumpido por el usuario...")
        if 'analyzer' in locals():
            analyzer.stop_analysis()
    except FileNotFoundError as e:
        print(f"\nError: No se encontró el directorio o archivo: {e}")
        print("Asegurate de que la carpeta 'imgs' existe y contiene imágenes.")
    except Exception as e:
        print(f"\nError inesperado: {e}")
        print("Verifica que todas las dependencias estén instaladas:")
        print("pip install -r requirements.txt")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
