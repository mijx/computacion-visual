# 🌀 Taller 64 - Visualización de Imágenes y Video 360° en Unity y Three.js

## 🎯 Objetivo del Taller

Aprender a cargar e integrar **imágenes panorámicas (equirectangulares)** y **videos 360°** dentro de entornos 3D inmersivos usando **Unity** y **Three.js con React**. Este tipo de contenido es clave para experiencias XR, recorridos virtuales y visualización inmersiva.

---

## 🧠 Conceptos Aprendidos

- Mapeo de texturas panorámicas en geometría esférica.
- Reproducción de video 360° como textura en tiempo real.
- Uso de React Three Fiber y Drei para escenas 3D interactivas.
- Implementación de controles de cámara tipo órbita.
- Alternancia dinámica entre diferentes tipos de contenido inmersivo.

---

## 🔧 Herramientas y Entornos

- React Three Fiber (JavaScript, React, Vite)
- @react-three/drei (OrbitControls)
- Vite (entorno de desarrollo)
- Archivos multimedia: imagen panorámica y video 360°

---

## 📁 Estructura del Proyecto

```
threejs/
│   ├── public/
│   │   ├── panorama.jpg
│   │   ├── video.mp4
│   │   └── vite.svg
│   ├── src/
│   │   ├── App.css
│   │   ├── App.jsx
│   │   ├── index.css
│   │   ├── main.jsx
│   │   └── components/
│   │       ├── Panorama.jsx
│   │       └── Video360.jsx
│   ├── .gitignore
│   ├── eslint.config.js
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── README.md
```

---

## 🧪 Implementación

### 🔹 Etapas realizadas

1. Creación del proyecto con Vite y React Three Fiber.
2. Implementación de un componente para visualizar una imagen panorámica 360° sobre una esfera.
3. Implementación de un componente para reproducir un video 360° como textura esférica.
4. Alternancia interactiva entre imagen y video mediante botones.
5. Integración de controles de órbita para navegación libre en la escena.

---

### 🔹 Código relevante

A continuación se muestra un fragmento representativo de la lógica principal de la aplicación:

```jsx
// src/App.jsx
import React, { useState } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import Panorama from "./components/Panorama";
import Video360 from "./components/Video360";

export default function App() {
  const [showVideo, setShowVideo] = useState(false);

  return (
    <>
      <Canvas
        camera={{ position: [0, 0, 0.1], fov: 75 }}
        style={{ height: "100vh", width: "100vw" }}
      >
        {showVideo ? <Video360 /> : <Panorama />}
        <OrbitControls enableZoom={false} />
      </Canvas>

      <div style={styles.controlsContainer}>
        <button
          onClick={() => setShowVideo(false)}
          style={{
            ...styles.button,
            backgroundColor: !showVideo ? "#1e88e5" : "rgba(30, 136, 229, 0.5)",
            boxShadow: !showVideo ? "0 5px 15px rgba(30,136,229,0.6)" : "none",
          }}
        >
          Imagen 360°
        </button>
        <button
          onClick={() => setShowVideo(true)}
          style={{
            ...styles.button,
            backgroundColor: showVideo ? "#1e88e5" : "rgba(30, 136, 229, 0.5)",
            boxShadow: showVideo ? "0 5px 15px rgba(30,136,229,0.6)" : "none",
          }}
        >
          Video 360°
        </button>
      </div>
    </>
  );
}
```

---

## 📊 Resultados Visuales

A continuación se muestran ejemplos de visualización interactiva de la imagen y el video 360° en la web. El usuario puede alternar entre ambos modos y navegar libremente por la escena.

![resultado360](./resultados/resultado.gif)

---

## 🧩 Prompts Usados

```text
"¿Cómo visualizo una imagen panorámica 360° en React Three Fiber?"
"¿Cómo aplico un video como textura esférica en Three.js?"
"¿Cómo alterno entre imagen y video 360° en una escena interactiva?"
```

---

## 💬 Reflexión Final

Este taller permitió comprender cómo integrar imágenes y videos 360° en aplicaciones web interactivas usando React Three Fiber. La implementación de controles de cámara y la alternancia dinámica entre diferentes tipos de contenido inmersivo facilitaron la exploración de técnicas modernas de visualización. El mayor reto fue manejar correctamente las texturas de video en tiempo real y asegurar una experiencia fluida en la navegación de la escena.

Para futuros proyectos, sería interesante agregar soporte para múltiples videos, hotspots interactivos o integración con dispositivos de realidad virtual para una experiencia aún más inmersiva.
