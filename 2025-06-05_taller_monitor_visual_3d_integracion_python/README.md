# 🧪 Monitor Visual 3D con Integración Python-ThreeJS

## 📅 Fecha
`2025-06-05`

---

## 🎯 Objetivo del Taller

Desarrollar un sistema en tiempo real que detecte personas en un video usando YOLOv8 y visualice los resultados en una escena 3D interactiva. La comunicación entre el backend (Python) y el frontend (ThreeJS) se realiza mediante WebSockets, permitiendo una actualización fluida y en tiempo real de la visualización.

---

## 🧠 Conceptos Aplicados

- [x] Detección de objetos en tiempo real con YOLOv8
- [x] Comunicación asíncrona mediante WebSockets
- [x] Visualización 3D interactiva con ThreeJS/React Three Fiber
- [x] Animaciones y transiciones suaves en 3D
- [x] Integración de sistemas Python-JavaScript
- [x] Manejo de estados y eventos en tiempo real

---

## 🔧 Herramientas y Entornos

### Backend (Python)
- `ultralytics` (YOLOv8) para detección de personas
- `opencv-python` para procesamiento de video
- `aiohttp` para servidor WebSocket
- `asyncio` para manejo asíncrono

### Frontend (ThreeJS)
- React + Vite
- React Three Fiber
- Three.js para gráficos 3D
- WebSocket API para comunicación en tiempo real

---

## 🧪 Implementación

### 🔹 Backend (Python)
1. **Detección de Personas**
   - YOLOv8 procesa cada frame del video
   - OpenCV maneja la visualización del video
   - Ventana redimensionable con controles

2. **Servidor WebSocket**
   - Manejo asíncrono de conexiones
   - Broadcast del conteo de personas
   - Sistema de apagado controlado

Código relevante del backend:
```python
# Detección y broadcast
results = model.predict(frame, classes=0, conf=0.5, verbose=False)
amnt_people = len(results[0].boxes)
await broadcast_people_count(amnt_people)
```

### 🔹 Frontend (ThreeJS)
1. **Visualización 3D**
   - Esfera reactiva a datos en tiempo real
   - Transiciones suaves de tamaño y color
   - Controles orbitales y grid de referencia

2. **Gestión de WebSocket**
   - Conexión/desconexión manual
   - Manejo de estados de conexión
   - Actualización fluida de la UI

Código relevante del frontend:
```javascript
// Animación de la esfera
useFrame(() => {
  scaleRef.current = THREE.MathUtils.lerp(
    scaleRef.current,
    1 + (peopleCount * 0.2),
    0.05
  )
  colorRef.current.lerp(targetColor, 0.05)
})
```

---

## 📊 Resultados Visuales

![demo](RESULTADOS/demo.gif)

---

## 💬 Reflexión Final

Este proyecto demuestra la integración efectiva entre sistemas de visión por computador y visualización 3D en tiempo real. La combinación de YOLOv8 para detección y ThreeJS para visualización, unidos mediante WebSockets, permite crear una experiencia interactiva y fluida.

Los desafíos principales incluyeron:
- Mantener la sincronización en tiempo real entre backend y frontend
- Implementar transiciones suaves en la visualización 3D
- Manejar estados de conexión y reconexión de forma robusta

El sistema podría expandirse para incluir más análisis visuales y representaciones 3D más complejas, como modelos anatómicos o visualizaciones de datos más elaboradas.
