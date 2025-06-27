# 🧪 Taller: Cámara en Vivo - Procesamiento en Tiempo Real con YOLO y OpenCV

## 📅 Fecha
`2025-06-25`

---

## 🎯 Objetivo del Taller

Desarrollar una aplicación completa de visión por computador que capture video en tiempo real desde webcam, aplique filtros clásicos de procesamiento de imágenes e integre detección de objetos usando YOLOv8. El sistema debe ser interactivo, visualmente moderno y educativo, demostrando conceptos fundamentales de visión artificial con una interfaz gráfica profesional.

---

## 🧠 Conceptos Aprendidos

Lista los principales conceptos aplicados:

- [x] Captura y procesamiento de video en tiempo real
- [x] Filtros clásicos de visión por computador (escala de grises, binarización, detección de bordes)
- [x] Detección de objetos con modelos YOLO preentrenados
- [x] Interfaces gráficas modernas con tkinter y tema oscuro
- [x] Threading para procesamiento concurrente
- [x] Integración de modelos de deep learning con aplicaciones interactivas
- [x] Arquitectura modular siguiendo principios SOLID

---

## 🔧 Herramientas y Entornos

Especifica los entornos usados:

- **Python** (`opencv-python`, `ultralytics`, `numpy`, `tkinter`, `PIL`, `torch`)
- **Modelos**: YOLOv8 Nano para detección de objetos en tiempo real
- **GUI**: tkinter con tema oscuro personalizado
- **Procesamiento**: OpenCV para filtros y transformaciones

📌 Todas las dependencias están especificadas en `requirements.txt`

---

## 📁 Estructura del Proyecto

```
2025-06-25_taller_camara_en_vivo_yolo_opencv/
├── python/
│   └── main.py           # Aplicación principal con GUI
├── requirements.txt      # Dependencias del proyecto
└── README.md            # Documentación completa
```

---

## 🧪 Implementación

### 🔹 Etapas realizadas

1. **Configuración del entorno**: Instalación de OpenCV, YOLOv8 y dependencias
2. **Captura de video**: Acceso a webcam con configuración optimizada
3. **Filtros de procesamiento**: Implementación de filtros clásicos modulares
4. **Integración YOLO**: Detección de objetos con visualización en tiempo real
5. **Interfaz gráfica**: GUI moderna con tema oscuro y controles interactivos
6. **Threading**: Procesamiento concurrente para mantener fluidez

### 🔹 Código relevante

Núcleo del sistema de detección YOLO integrado:

```python
def detect_objects(self, frame):
    if self.model is None:
        return frame
        
    results = self.model(frame, verbose=False)
    annotated_frame = frame.copy()
    current_objects = {}
    
    for result in results:
        boxes = result.boxes
        if boxes is not None:
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])
                class_name = self.model.names[class_id]
                
                if confidence > 0.5:
                    current_objects[class_name] = current_objects.get(class_name, 0) + 1
                    cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    
                    label = f"{class_name}: {confidence:.2f}"
                    cv2.putText(annotated_frame, label, (x1, y1 - 5), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    
    return annotated_frame
```

Aplicación modular de filtros con arquitectura extensible:

```python
def process_frame(self, frame):
    if self.current_filter == 'grayscale':
        processed = self.apply_grayscale_filter(frame)
        processed = cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR)
    elif self.current_filter == 'binary':
        processed = self.apply_binary_filter(frame)
        processed = cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR)
    elif self.current_filter == 'edges':
        processed = self.apply_edge_detection(frame)
        processed = cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR)
    elif self.current_filter == 'yolo':
        processed = self.detect_objects(frame)
    else:
        processed = frame.copy()
    
    return processed
```

---

## 📊 Resultados Visuales

### 🖥️ Interfaz Gráfica Moderna

La aplicación cuenta con una **interfaz gráfica unificada de 1280x720px** con tema oscuro profesional:

![output.gif](resultados/output.gif)

### 🎮 Funcionalidades Implementadas

**Filtros Disponibles:**
- **Original**: Stream directo de webcam
- **Escala de Grises**: Conversión a monocromático
- **Binario**: Binarización con umbral fijo
- **Bordes**: Detección de bordes con algoritmo Canny
- **Blur**: Suavizado gaussiano
- **YOLO**: Detección de objetos con bounding boxes

**Controles Interactivos:**
- Botones GUI: Iniciar, Pausar, Capturar, Ayuda
- Teclas rápidas: g, b, e, l, o, y, p, s, h, q
- Selección de filtros con radio buttons
- Captura de imágenes con timestamp

---

## 💬 Reflexión Final

Este taller ha sido fundamental para comprender la integración práctica entre visión por computador clásica y modelos modernos de deep learning. La implementación de filtros tradicionales como escala de grises y detección de bordes junto con YOLOv8 demuestra la evolución y complementariedad de las técnicas en visión artificial.

La parte más compleja fue la optimización del rendimiento en tiempo real, balanceando la calidad de procesamiento con la fluidez de la interfaz. El threading concurrente y la gestión eficiente de memoria fueron cruciales para mantener ~30 FPS. La experiencia de crear una GUI moderna con tema oscuro también amplió mis conocimientos en diseño de interfaces profesionales.

Para futuros proyectos, implementaría tracking persistente de objetos, soporte para múltiples modelos YOLO especializados, y configuración dinámica de parámetros. También exploraría la integración con cámaras IP y el procesamiento distribuido para aplicaciones de mayor escala.

---

## ✅ Checklist de Entrega

- [x] Carpeta `2025-06-25_taller_camara_en_vivo_yolo_opencv`
- [x] Código limpio y funcional con arquitectura modular
- [x] Interfaz gráfica moderna con tema oscuro
- [x] Sistema completo de captura, filtros y detección YOLO
- [x] Documentación completa y técnica
- [x] Gestión de dependencias con requirements.txt
- [x] Commits descriptivos en inglés
