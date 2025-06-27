# 🎯 Taller: Detección de Objetos en Tiempo Real con YOLO y Webcam

## 📅 Fecha
`2025-06-25`

---

## 🎯 Objetivo del Taller

Desarrollar una aplicación de escritorio moderna usando Python y Tkinter con tema oscuro que implemente detección de objetos en tiempo real utilizando YOLOv8. El sistema debe capturar video desde la webcam, procesar cada frame con el modelo preentrenado, mostrar detecciones con bounding boxes, etiquetas y nivel de confianza, además de visualizar métricas de rendimiento (FPS) y estadísticas de detección en una interfaz gráfica profesional.

---

## 🧠 Conceptos Aprendidos

Lista los principales conceptos aplicados:

- [x] Detección de objetos con modelos YOLO preentrenados
- [x] Procesamiento de video en tiempo real con OpenCV
- [x] Interfaces gráficas modernas con Tkinter y tema oscuro
- [x] Threading para procesamiento concurrente
- [x] Visualización de métricas y estadísticas en tiempo real
- [x] Filtrado dinámico por clases de objetos
- [x] Control de parámetros de detección (umbral de confianza)
- [x] Arquitectura modular siguiendo principios SOLID

---

## 🔧 Herramientas y Entornos

Especifica los entornos usados:

- **Python** (`opencv-python`, `ultralytics`, `numpy`, `tkinter`, `PIL`, `torch`, `matplotlib`)
- **Modelo**: YOLOv8 Nano para detección optimizada en tiempo real
- **GUI**: Tkinter con tema oscuro personalizado y componentes TTK
- **Visualización**: Matplotlib para gráficas de FPS integradas

📌 Todas las dependencias están especificadas en `requirements.txt`

---

## 📁 Estructura del Proyecto

```
2025-06-25_taller_yolo_deteccion_webcam_tiempo_real/
├── python/
│   └── main.py               # Aplicación principal con GUI moderna
├── requirements.txt          # Dependencias del proyecto
└── README.md                # Documentación completa
```

📎 Estructura optimizada para desarrollo y despliegue local

---

## 🧪 Implementación

Explica el proceso:

### 🔹 Etapas realizadas
1. **Configuración del entorno**: Instalación de YOLOv8, OpenCV y dependencias gráficas
2. **Diseño de interfaz**: GUI moderna con tema oscuro, paneles organizados y controles intuitivos
3. **Integración YOLO**: Carga de modelo YOLOv8 Nano con configuración optimizada
4. **Procesamiento en tiempo real**: Loop de detección con threading para mantener fluidez
5. **Visualización avanzada**: Métricas FPS, estadísticas por clase y filtros dinámicos
6. **Optimización de rendimiento**: Balance entre calidad y velocidad de procesamiento

### 🔹 Código relevante

Núcleo del sistema de detección YOLO optimizado:

```python
def detect_objects(self, frame):
    if self.model is None:
        return frame, {}
        
    try:
        start_time = time.time()
        results = self.model(frame, verbose=False, conf=self.confidence_threshold)
        inference_time = time.time() - start_time
        
        annotated_frame = frame.copy()
        current_detections = defaultdict(int)
        
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    confidence = float(box.conf[0])
                    class_id = int(box.cls[0])
                    class_name = self.model.names[class_id]
                    
                    # Filtrar por clases seleccionadas
                    if self.selected_classes and class_name not in self.selected_classes:
                        continue
                        
                    current_detections[class_name] += 1
                    
                    # Dibujar bounding box con color único por clase
                    color = self.get_class_color(class_name)
                    cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
                    
                    # Etiqueta con fondo sólido
                    label = f"{class_name}: {confidence:.2f}"
                    label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
                    cv2.rectangle(annotated_frame, (x1, y1 - label_size[1] - 10), 
                                (x1 + label_size[0], y1), color, -1)
                    cv2.putText(annotated_frame, label, (x1, y1 - 5), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Calcular FPS en tiempo real
        fps = 1.0 / inference_time if inference_time > 0 else 0
        
        return annotated_frame, current_detections
        
    except Exception as e:
        self.log(f"❌ Error en detección: {str(e)}")
        return frame, {}
```

Interfaz gráfica moderna con tema oscuro y controles avanzados:

```python
def configure_dark_theme(self):
    """Configurar tema oscuro profesional"""
    self.colors = {
        'bg_primary': '#1e1e1e',      # Fondo principal
        'bg_secondary': '#2d2d2d',    # Fondo secundario
        'bg_accent': '#3d3d3d',       # Acentos
        'bg_card': '#2d2d2d',         # Tarjetas
        'text_primary': '#ffffff',    # Texto principal
        'text_secondary': '#b0b0b0',  # Texto secundario
        'accent_green': '#00ff41',    # Verde neón
        'accent_blue': '#00b4d8',     # Azul moderno
        'accent_orange': '#ff6b35',   # Naranja vibrante
    }
    
    # Configuración de estilos TTK personalizados
    self.style = ttk.Style()
    self.style.theme_use('clam')
    
    self.style.configure('DarkLabelFrame.TLabelframe', 
                       background=self.colors['bg_secondary'], 
                       bordercolor=self.colors['accent_green'],
                       borderwidth=2)
```

---

## 📊 Resultados Visuales

![output.gif](resultados/output.gif)

### 🖥️ Funcionalidades Implementadas

**Detección Avanzada:**
- **YOLOv8 Nano**: Modelo optimizado para tiempo real
- **Filtro por clases**: Selección dinámica de objetos a detectar
- **Umbral configurable**: Control de sensibilidad de detección
- **Colores únicos**: Cada clase tiene su color distintivo

**Interfaz Profesional:**
- **Tema oscuro moderno**: Diseño inspirado en GitHub Dark
- **Panel de estadísticas**: Gráfica de FPS en tiempo real
- **Métricas detalladas**: Contador por clase y totales
- **Controles intuitivos**: Botones, sliders y checkboxes estilizados

**Rendimiento Optimizado:**
- **Threading concurrente**: Procesamiento sin bloqueo de GUI
- **FPS dinámico**: Cálculo y visualización en tiempo real
- **Captura de frames**: Guardado instantáneo con timestamp

---

## 💬 Reflexión Final

Este taller representa un avance significativo en la implementación de sistemas de visión por computador con interfaces profesionales. La integración de YOLOv8 con Tkinter demuestra cómo combinar modelos de deep learning modernos con interfaces gráficas tradicionales pero estilizadas.

La parte más compleja fue la optimización del rendimiento, balanceando la calidad de detección con la fluidez de la interfaz. El sistema de threading concurrente y la gestión eficiente de memoria fueron cruciales para mantener ~20-30 FPS consistentes. La experiencia de crear una GUI moderna con tema oscuro también expandió las habilidades en diseño de interfaces profesionales.

Para futuros proyectos, implementaría tracking persistente de objetos detectados, soporte para múltiples modelos YOLO especializados (personas, vehículos, etc.), y configuración de alertas por detección específica. También exploraría la integración con cámaras IP y el procesamiento distribuido para aplicaciones de videovigilancia.

---

## ✅ Checklist de Entrega

- [x] Carpeta `2025-06-25_taller_yolo_deteccion_webcam_tiempo_real`
- [x] Código limpio y funcional con arquitectura modular
- [x] Interfaz gráfica moderna con tema oscuro profesional
- [x] Sistema completo de detección YOLO en tiempo real
- [x] GIF demostrativo de la aplicación funcionando
- [x] Métricas de rendimiento y estadísticas visuales
- [x] Controles avanzados (filtros, umbral, captura)
- [x] Documentación técnica completa
- [x] Gestión de dependencias con requirements.txt
- [x] README estructurado según plantilla oficial

