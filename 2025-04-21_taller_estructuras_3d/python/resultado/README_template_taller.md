# 🧪 Taller - Construyendo el Mundo 3D: Vértices, Aristas y Caras

## 📅 Fecha
`2025-04-21`

---

## 🎯 Objetivo del Taller

Describe brevemente el objetivo del taller: ¿qué se pretende explorar, aplicar o construir?

---

## 🧠 Conceptos Aprendidos

Lista los principales conceptos aplicados:

- [x] Transformaciones geométricas (escala, rotación, traslación)
- [x] Segmentación de imágenes
- [x] Shaders y efectos visuales
- [x] Entrenamiento de modelos IA
- [x] Comunicación por gestos o voz
- [ ] Etc...

---

## 🔧 Herramientas y Entornos

Especifica los entornos usados:

- Python (`opencv-python`, `torch`, `mediapipe`, `diffusers`, etc.)


---

## 📁 Estructura del Proyecto

```
2025-04-21_taller_estructuras_3d/
├── python/
├── threejs/
├── README.md

```

---

## 🧪 Implementación

Explica el proceso:

### 🔹 Etapas realizadas
1. Preparación de datos o escena.
2. Aplicación de modelo o algoritmo.
3. Visualización o interacción.
4. Guardado de resultados.

### 🔹 Código relevante

Incluye un fragmento que resuma el corazón del taller:

```python
# Segmentación semántica con DeepLab
output = model(input_tensor)['out']
prediction = output.argmax(1).squeeze().cpu().numpy()
```

---

## 📊 Resultados Visuales

<img src="resultado\threejsModels.gif" width="50%" />

  Espacio para pegar el output de terminal (yo lo hago luego)
---

## 🧩 Prompts Usados

Enumera los prompts utilizados (resumidos):

```text
"Create a photorealistic image of a robot painting a mural using Stable Diffusion"
"Segment a car and a person using SAM at point (200, 300)"
```

---

## 💬 Reflexión Final

Responde en 2-3 párrafos:

- ¿Qué aprendiste o reforzaste con este taller?
- ¿Qué parte fue más compleja o interesante?
- ¿Qué mejorarías o qué aplicarías en futuros proyectos?

---

## 👥 Contribuciones Grupales (si aplica)

Describe exactamente lo que hiciste tú:

```markdown
- Programé el detector de postura en MediaPipe
- Generé los GIFs y documentación
- Integré el control de voz con visualización en Unity
```

---

## ✅ Checklist de Entrega

- [x] Carpeta `YYYY-MM-DD_nombre_taller`
- [x] Código limpio y funcional
- [x] GIF incluido con nombre descriptivo (si el taller lo requiere)
- [x] Visualizaciones o métricas exportadas
- [x] README completo y claro
- [x] Commits descriptivos en inglés

---