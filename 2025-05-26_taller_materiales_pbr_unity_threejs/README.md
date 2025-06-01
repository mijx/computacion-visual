# 🧪 Taller - Materiales Realistas: Introducción a PBR en Unity y Three.js

## 🔍 Objetivo del taller

Comprender los principios del renderizado basado en física (PBR, _Physically-Based Rendering_) y aplicarlos a modelos 3D para mejorar su realismo visual. Este taller permite comparar cómo la luz interactúa con diferentes tipos de materiales y cómo las texturas afectan el resultado visual final.

---

## 🧠 Conceptos Aprendidos

- Principios de materiales PBR y su importancia en el realismo visual.
- Uso de mapas de texturas: albedo, normal, metalness y roughness.
- Configuración de materiales PBR en Three.js y React Three Fiber.
- Comparación de flujos de trabajo entre Unity y Three.js.
- Organización de proyectos para visualización de materiales.

---

## 🔧 Herramientas y Entornos

- **Three.js** (JavaScript, React, Vite)
- **React Three Fiber** (para integración con React)
- **@react-three/drei** (OrbitControls, utilidades)
- **Leva** (controles interactivos de parámetros)
- **Texturas PBR** (archivos .jpg en `/src/assets/`)
- **Unity** (no incluido en este repositorio, pero referenciado en el taller)

---

## 📁 Estructura del Proyecto

```
threejs/
│   ├── public/
│   │   └── vite.svg
│   ├── src/
│   │   ├── App.css
│   │   ├── App.jsx
│   │   ├── index.css
│   │   ├── main.jsx
│   │   ├── assets/
│   │   │   ├── albedo.jpg
│   │   │   ├── floor.jpg
│   │   │   ├── metalness.jpg
│   │   │   ├── normal.jpg
│   │   │   ├── roughness.jpg
│   │   │   └── react.svg
│   │   └── components/
│   │       ├── ControlsUI.jsx
│   │       └── ScenePBR.jsx
│   ├── .gitignore
│   ├── eslint.config.js
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── README.md
resultados/
│   └── chrome_hyApqdzdqF.gif
```

---

## 🧪 Implementación

### 🔹 Etapas realizadas

1. Creación de un proyecto con Vite y React Three Fiber.
2. Implementación de una escena 3D con materiales PBR usando mapas de texturas (albedo, normal, metalness, roughness).
3. Integración de controles interactivos con Leva para modificar parámetros de los materiales en tiempo real.
4. Visualización en el navegador con controles de órbita y comparación visual de materiales.
5. Exportación de resultados visuales (GIFs) para documentación.

---

### 🔹 Código relevante

A continuación se muestra un fragmento representativo de cómo se implementó la escena PBR y los controles interactivos:

```javascript
// src/components/ScenePBR.jsx
import React from "react";
import { useTexture } from "@react-three/drei";
import { useControls } from "leva";

export default function ScenePBR() {
  const textures = useTexture({
    map: "/src/assets/albedo.jpg",
    normalMap: "/src/assets/normal.jpg",
    metalnessMap: "/src/assets/metalness.jpg",
    roughnessMap: "/src/assets/roughness.jpg",
  });

  const { metalness, roughness } = useControls({
    metalness: { value: 1, min: 0, max: 1, step: 0.01 },
    roughness: { value: 0.5, min: 0, max: 1, step: 0.01 },
  });

  return (
    <mesh position={[0, 1, 0]}>
      <sphereGeometry args={[1, 64, 64]} />
      <meshStandardMaterial
        {...textures}
        metalness={metalness}
        roughness={roughness}
      />
    </mesh>
  );
}
```

---

## 📊 Resultados Visuales

La siguiente imagen/GIF muestra la escena con materiales PBR aplicados, donde se observa el efecto de las texturas y los parámetros interactivos sobre la apariencia del material:

![threejs_pbr](./resultados/resultado.gif)

---

## 🧩 Prompts Usados

```text
"¿Cómo aplico materiales PBR con texturas en React Three Fiber?"
"¿Cómo uso mapas de metalness y roughness en Three.js?"
"¿Cómo agrego controles interactivos para modificar materiales en tiempo real?"
```

---

## 💬 Reflexión Final

Este taller permitió experimentar con la configuración de materiales PBR y la importancia de los mapas de texturas para lograr realismo visual. La integración de controles interactivos facilitó la exploración de parámetros y la visualización inmediata de los cambios.

El mayor reto fue ajustar correctamente los mapas y comprender el impacto de cada parámetro en la apariencia final. Para futuros proyectos, sería interesante comparar más a fondo los resultados entre Unity y Three.js, e incorporar modelos 3D más complejos para resaltar las diferencias en la representación de materiales.
