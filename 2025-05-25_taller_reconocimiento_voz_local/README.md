# 🧪 Taller - Voz al Código: Comandos por Reconocimiento de Voz Local

## 📅 Fecha
`2025-05-26` – Fecha de entrega

---

## 🎯 Objetivo del Taller

Implementar una interfaz de voz local en Python para controlar visualmente un elemento gráfico mediante comandos hablados. La actividad se centra en conectar entrada de voz con visualización en Tkinter, incluyendo retroalimentación por voz.

---

## 🧠 Conceptos Aprendidos

- [x] Reconocimiento de voz con `speech_recognition`
- [x] Visualización en `tkinter` usando `Canvas`
- [x] Manejo de geometría y rotación en 2D
- [x] Uso de `pyttsx3` para retroalimentación hablada
- [x] Estructura de interfaces reactivas con hilos

---

## 🔧 Herramientas y Entornos

- Python 3.10
- speech_recognition
- pyttsx3
- tkinter (visualización)
- threading (manejo asincrónico)

---

## 📁 Estructura del Proyecto

```
2025-05-25_taller_reconocimiento_voz_local/
├── python/
│   └── voz_control_tkinter.py
├── resultado/
│   └── demo_control_voz.mp4
├── README.md
```

---

## 🧪 Implementación

### 🔹 Etapas realizadas
1. Se configuró el micrófono y el entorno de reconocimiento de voz usando `speech_recognition`.
2. Se diseñó una interfaz en `tkinter` con un triángulo dibujado en un `Canvas`.
3. Se implementó rotación del triángulo con comandos "izquierda" y "derecha".
4. Se agregó cambio de color con comandos como “rojo”, “verde”, etc.
5. Se añadió retroalimentación por voz con `pyttsx3`.
6. Se integró el proceso de escucha en hilos para mantener la interfaz reactiva.

### 🔹 Código relevante

```python
if texto == "derecha":
    angulo_actual = (angulo_actual + 30) % 360
    estado_lbl.config(text="Girando a la derecha")
    hablar("Girando a la derecha")
elif texto == "izquierda":
    angulo_actual = (angulo_actual - 30) % 360
    estado_lbl.config(text="Girando a la izquierda")
    hablar("Girando a la izquierda")
```

---

## 📊 Resultados Visuales

El resultado es una ventana que muestra un triángulo cuyo color y orientación puede cambiarse mediante comandos hablados en español:
- Comandos de color: rojo, verde, amarillo, negro, blanco.
- Comandos de orientación: derecha, izquierda (cada uno realizando una rotación de 30°).

El sistema indica la ejecución del comando con texto y lectura en voz alta. Se dispone de un botón para activar el reconocimiento de voz.

https://github.com/user-attachments/assets/6d62b19a-600a-4c71-877a-92db3c9a4ad3

---

## 🧩 Prompts Usados

```text
"Dame el algoritmo para girar el triángulo 30 grados."
"Escribe el código para cambiar el color del triángulo."
"Genera un botón para iniciar la entrada de comandos de voz."
```

---

## 💬 Reflexión Final

Este taller fue una excelente oportunidad para integrar múltiples aspectos de programación interactiva: reconocimiento de voz, geometría en 2D y visualización gráfica. Pude experimentar cómo controlar una figura en pantalla usando comandos hablados en español, y aprendpi el uso de bibliotecas como `speech_recognition` y `tkinter`.

---

## ✅ Checklist de Entrega

- [x] Carpeta `2025-05-25_taller_reconocimiento_voz_local`
- [x] Código limpio y funcional
- [x] Video captura de pantalla con demo funcionando
- [x] README completo y claro
- [x] Commits descriptivos en inglés

---
