# 🧪 Interacción Multimodal: Gestos y Voz

## 📅 Fecha
`2025-05-26` – Fecha de entrega

---

## 🎯 Objetivo del Taller

Fusionar gestos y comandos de voz para realizar acciones compuestas dentro de una interfaz visual. Este taller introduce los fundamentos de los sistemas de interacción multimodal, combinando dos formas de entrada humana para enriquecer la experiencia de control.

---

## 🧠 Conceptos Aprendidos

- Detección de movimiento con OpenCV
- Reconocimiento de voz con SpeechRecognition
- Uso de hilos (threading) para entradas simultáneas
- Lógica condicional multimodal
- Visualización interactiva con pygame
- Retroalimentación auditiva con pyttsx3

---

## 🔧 Herramientas y Entornos

- Python 3.13
- Librerías: opencv-python, pygame, speech_recognition, pyttsx3, numpy, pyaudio

---

## 📁 Estructura del Proyecto

```
2025-05-26_taller_interfaces_multimodales_voz_gestos/
├── python/
├── resultado/
├── README.md
```

---

## 🧪 Implementación

### 🔹 Etapas realizadas
1. Configuración de entorno Python y librerías
2. Captura de video desde webcam
3. Detección de gestos a partir del movimiento
5. Captura y reconocimiento de comandos de voz
6. Lógica combinada gesto + voz para controlar una figura
7. Retroalimentación visual (texto en pantalla) y auditiva (voz)

### 🔹 Código relevante

```python
if comando and gesto:
    if gesto == 'mano_abierta':
        if comando in ['rojo', 'azul', 'verde', 'amarillo']:
            color = colores[comando]
            hablar(f"Color cambiado a {comando}")
    elif gesto == 'puno':
        if comando == 'rotar':
            angulo = (angulo + 30) % 360
            hablar("Rotando 30 grados")
    elif gesto == 'v':
        if comando == 'ocultar':
            cuadro_visible = False
            hablar("Ocultando figura")
        elif comando == 'mostrar':
            cuadro_visible = True
            hablar("Mostrando figura")
```

---

## 📊 Resultados Visuales

El sistema reacciona en tiempo real al movimiento de la cámara y un cuadrado dibujado en pantalla responde a las acciones:
- Cambio de color: si se dice el color y se muestra la mano abierta.
- Rotar: si se dice "rotar" y se muestra el puño cerrado.
- Mostrar u ocultar: diciendo el comando mientras se hace una V con los dedos de una mano.

![resultado.gif](resultados/demo_camara_y_voz.gif)

---

## 🧩 Prompts Usados

```text
“Provee el código para detectar la siguiente combinación comando-gesto de mano: [...]”
“Dame el código para mostrar en terminal el gesto y comando detectado, junto a "escuchando..."
“La detección de cámara va muy rápido para procesar al tiempo el comando de voz, ¿cómo corregirlo?"
```

---

## 💬 Reflexión Final

Este taller me permitió aplicar entradas multimodales y coordinar múltiples hilos de entrada en un solo sistema interactivo. Fue muy útil para entender cómo combinar detección visual con audio, y cómo simplificar gestos sin dependencias complejas como MediaPipe.

La parte más desafiante fue sincronizar el tiempo de reconocimiento de voz con los gestos. Solucioné esto añadiendo una pausa mínima entre gestos detectados. Para futuros proyectos.

---

## ✅ Checklist de Entrega

- [x] Carpeta `2025-05-26_taller_interfaces_multimodales_voz_gestos`
- [x] Código limpio y funcional
- [x] Visualización implementada en pygame
- [x] Retroalimentación auditiva con voz sintetizada
- [x] README completo y claro
