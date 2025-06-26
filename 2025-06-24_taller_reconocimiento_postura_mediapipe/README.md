# 🧪 Taller - Reconocimiento de Acciones Simples con Detección de Postura

## 📅 Fecha

`2025-06-24` – Fecha de entrega

---

## 🔍 Objetivo del taller

Implementar el reconocimiento de **acciones simples** (como sentarse, levantar brazos o caminar frente a cámara) usando **MediaPipe Pose** para detectar la postura corporal. El objetivo es utilizar puntos clave del cuerpo (landmarks) para interpretar la acción y responder visual o sonoramente.

---

## 🧠 Conceptos Aprendidos

Lista los principales conceptos aplicados:

- [x] Detección de pose humana con `mediapipe`
- [x] Procesamiento de video en tiempo real con `opencv`
- [x] Extracción y análisis de landmarks corporales
- [x] Lógica condicional para clasificación de posturas
- [x] Visualización y anotación de resultados en la imagen

---

## 🔧 Herramientas y Entornos

- Python 3.9.7
- MediaPipe
- OpenCV
- NumPy
- Visual Studio Code

---

## 📁 Estructura del Proyecto

```
2025-06-24_taller_reconocimiento_postura_mediapipe/
├── python/
│   ├── .python-version
│   └── solucion.py
├── resultado/
│   └── python_EHUY6fzo3E.gif
├── README.md
```

---

## 🧪 Implementación

### 🔹 Etapas realizadas

1. Inicialización de la captura de video con OpenCV.
2. Configuración del detector de pose de MediaPipe.
3. Procesamiento de cada frame: conversión a RGB y detección de landmarks.
4. Extracción de puntos clave relevantes (hombros, muñecas, caderas, rodillas).
5. Implementación de lógica para clasificar acciones/posturas:
   - Levantando brazos
   - Sentado
   - Caminando
   - Acción no reconocida
6. Visualización de los landmarks y la acción detectada sobre el video en tiempo real.
7. Finalización segura de la captura y cierre de ventanas.

### 🔹 Código relevante

```python
import cv2
import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("No se pudo leer el frame.")
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        landmarks = results.pose_landmarks.landmark
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
        left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE]
        right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE]

        if left_wrist.y < left_shoulder.y and right_wrist.y < right_shoulder.y:
            action = "Levantando brazos"
        elif left_hip.y > left_knee.y and right_hip.y > right_knee.y:
            action = "Sentado"
        elif abs(left_hip.y - right_hip.y) < 0.05 and abs(left_knee.y - right_knee.y) < 0.05:
            action = "Caminando"
        else:
            action = "Accion no reconocida"

        cv2.putText(frame, f"Acción: {action}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow("Reconocimiento de Postura", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
```

---

## 📊 Resultados Visuales

Al ejecutar el proyecto, la cámara detecta la postura del usuario en tiempo real y muestra en pantalla la acción reconocida (por ejemplo, "Levantando brazos", "Sentado", "Caminando") junto con los puntos clave del cuerpo.

![python_EHUY6fzo3E.gif](resultado/python_EHUY6fzo3E.gif)

---

## 🧩 Prompts Usados

```text
"¿Cómo detectar si una persona está levantando los brazos usando MediaPipe?"
"¿Cómo clasificar posturas básicas con landmarks de pose en Python?"
"¿Cómo mostrar el nombre de la acción detectada sobre el video en OpenCV?"
```

---

## 💬 Reflexión Final

Este taller permitió aplicar de manera práctica el reconocimiento de posturas humanas usando visión por computadora. La integración de MediaPipe y OpenCV facilitó la detección y visualización de landmarks, mientras que la lógica condicional permitió clasificar acciones básicas de forma sencilla. El mayor reto fue definir reglas robustas para distinguir entre posturas similares y asegurar la respuesta en tiempo real.

Para futuros proyectos, sería interesante ampliar el sistema para reconocer más acciones, mejorar la robustez ante diferentes posiciones de cámara y explorar la integración con retroalimentación auditiva o control de interfaces.

---

## ✅ Checklist de Entrega

- [x] Carpeta `2025-06-24_taller_reconocimiento_postura_mediapipe`
- [x] Código limpio y funcional
- [x] GIF incluido con nombre descriptivo
- [x] README completo y claro
- [x] Commits descriptivos en inglés

---
