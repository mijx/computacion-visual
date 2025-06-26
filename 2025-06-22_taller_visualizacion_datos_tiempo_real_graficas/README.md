# 🧪 Taller de Visualización de Datos en Tiempo Real con Gráficas

## 📅 Fecha
`2025-06-22` – Taller de visualización de datos en tiempo real con detección de objetos

---

## 🎯 Objetivo del Taller

Desarrollar un sistema de visualización de datos en tiempo real que integre:
- Streaming de imágenes aleatorias de animales
- Detección de objetos usando YOLOv8
- Visualización dinámica con gráficos de pastel actualizados en tiempo real
- Interface gráfica interactiva con layout de dos columnas

---

## 🧠 Conceptos Aprendidos

Lista los principales conceptos aplicados:

- [x] Detección de objetos en tiempo real con YOLOv8
- [x] Streaming de imágenes con threading
- [x] Visualización de datos dinámicos con matplotlib
- [x] Procesamiento de imágenes con OpenCV
- [x] Interfaz gráfica interactiva
- [x] Arquitectura modular con principios SOLID
- [x] Manejo de callbacks y eventos
- [x] Integración de múltiples librerías de visualización

---

## 🔧 Herramientas y Entornos

Especifica los entornos usados:

- **Python** con las siguientes librerías:
  - `opencv-python>=4.8.0` - Procesamiento de imágenes
  - `ultralytics>=8.0.0` - YOLOv8 para detección de objetos
  - `numpy>=1.24.0` - Operaciones numéricas
  - `matplotlib>=3.7.0` - Gráficos dinámicos
  - `torch>=2.0.0` - Backend de deep learning
  - `pillow>=9.0.0` - Manipulación de imágenes


---

## 🧪 Implementación

### 🔹 Arquitectura del Sistema

El proyecto está dividido en tres componentes principales:

1. **ImageStreamer** (`img_stream.py`):
   - Selección aleatoria de imágenes cada segundo
   - Threading para no bloquear la aplicación
   - Sistema de callbacks para integración

2. **YoloAnalyzer** (`yolo_analyzer.py`):
   - Detección de objetos con YOLOv8
   - Visualización con bounding boxes
   - Gráficos de pastel dinámicos
   - Layout de dos columnas

3. **Aplicación Principal** (`app.py`):
   - Interfaz de usuario
   - Manejo de configuración
   - Estadísticas finales

### 🔹 Etapas realizadas
1. **Preparación del sistema de streaming**: Clase para seleccionar imágenes aleatorias cada segundo
2. **Integración con YOLOv8**: Detección de una sola clase por imagen (mayor confianza)
3. **Visualización dinámica**: Layout de dos columnas con imagen y gráfico de pastel
4. **Sistema de control**: Controles intuitivos con tecla 'q' y manejo de ventanas

### 🔹 Código relevante

**Streaming de imágenes con callback:**
```python
class ImageStreamer:
    def _streaming_loop(self):
        while self.is_streaming and self.current_image_count < self.max_images:
            selected_image_path = self._select_random_image()
            image = self._load_image(selected_image_path)
            
            if self.image_callback:
                self.image_callback(image, animal_name)
```

**Detección con YOLOv8 (una sola detección por imagen):**
```python
def _extract_detections(self, result, true_animal: str):
    best_detection = None
    best_confidence = 0.0
    
    for i in range(len(boxes)):
        confidence = float(boxes.conf[i].cpu().numpy())
        if confidence > best_confidence:
            # Guardar solo la mejor detección
            best_detection = {...}
            best_confidence = confidence
```

**Gráfico de pastel dinámico:**
```python
def _create_pie_chart(self, width: int, height: int):
    pie_result = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                       pctdistance=1.1,      # Porcentajes fuera
                       labeldistance=0.6)    # Nombres dentro
```

---

## 📊 Resultados Visuales

### 📌 Este taller **incluye un GIF animado**:

El sistema muestra en tiempo real:
- **Columna izquierda**: Imagen del animal con bounding boxes de detección
- **Columna derecha**: Gráfico de pastel dinámico con estadísticas

![Sistema de detección en tiempo real](./resultados/resultados.gif)


## 💬 Reflexión Final

### ¿Qué aprendiste o reforzaste con este taller?

Este taller me permitió profundizar en la integración de múltiples tecnologías para crear un sistema de visualización en tiempo real. Aprendí a combinar efectivamente el streaming de datos, la detección de objetos con IA, y la visualización dinámica en una sola aplicación cohesiva. La aplicación de principios SOLID fue fundamental para mantener el código modular y extensible.


## 📈 Estadísticas del Sistema

El sistema genera automáticamente:
- **Precisión general**: Porcentaje de detecciones correctas
- **Total de detecciones**: Número total de objetos detectados
- **Promedio por imagen**: Detecciones promedio por imagen procesada
- **Distribución por clase**: Gráfico visual de la distribución de detecciones