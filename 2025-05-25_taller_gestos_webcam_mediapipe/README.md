# 🧪 Detección de Gestos y Medición con MediaPipe

## 📅 Fecha
2025-05-30

---

## 🎯 Objetivo del Taller

Implementar un sistema de visión por computadora que permita detectar gestos de la mano en tiempo real, con capacidad para contar dedos levantados y medir la distancia entre el dedo índice y pulgar utilizando MediaPipe.

---

## 🧠 Conceptos Aprendidos

- [x] Procesamiento de video en tiempo real con OpenCV
- [x] Detección de landmarks de manos con MediaPipe
- [x] Análisis geométrico para medición de distancias
- [x] Tracking de gestos y poses de dedos
- [x] Visualización de datos en tiempo real

---

## 🔧 Herramientas y Entornos

- Python 3.11.4
- OpenCV (`cv2`)
- MediaPipe
- NumPy
- Jupyter Notebook

## 🧪 Implementación

### 🔹 Etapas realizadas

1. **Inicialización de MediaPipe Hands**
   - Configuración del detector de manos
   - Establecimiento de parámetros de confianza

2. **Detección de Dedos Levantados**
   - Análisis de posición de landmarks
   - Implementación de lógica para contar dedos

3. **Medición de Distancia**
   - Cálculo de distancia entre índice y pulgar
   - Visualización de mediciones en tiempo real

### 🔹 Código relevante

El corazón del sistema reside en dos funciones principales:

```python
def count_fingers(self, hand_landmarks):
    finger_tips = [8, 12, 16, 20]  # Índices de puntas de dedos
    thumb_tip = 4
    count = 0
    
    # Verificación del pulgar
    if hand_landmarks.landmark[thumb_tip].x < hand_landmarks.landmark[thumb_tip - 1].x:
        count += 1
        
    # Verificación de otros dedos
    for tip in finger_tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            count += 1
            
    return count

def calculate_distance(self, p1, p2, hand_landmarks):
    x1, y1 = hand_landmarks.landmark[p1].x, hand_landmarks.landmark[p1].y
    x2, y2 = hand_landmarks.landmark[p2].x, hand_landmarks.landmark[p2].y
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
```

---

## 📊 Resultados Visuales

### 🟢 Conteo de dedos levantados
![conteo](resultados/count.gif)

### 🟢 Medir distancia entre dedos
![distance](resultados/distance.gif)

---

## 💬 Reflexión Final

El proyecto demuestra la potencia de MediaPipe para el análisis de gestos en tiempo real. La implementación de la detección de dedos y medición de distancias presenta desafíos interesantes en términos de precisión y rendimiento. La combinación de OpenCV para el procesamiento de video y MediaPipe para la detección de landmarks proporciona una base sólida para aplicaciones de interacción gestual.