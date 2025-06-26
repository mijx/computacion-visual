# 🧪 Taller - Animaciones por Esqueleto: Importando y Reproduciendo Animaciones

## 🔍 Objetivo del taller

Trabajar con animaciones basadas en huesos (esqueleto) y reproducirlas desde archivos externos como `.FBX` o `.GLTF`. El objetivo es comprender cómo funcionan las animaciones esqueléticas, cómo importarlas correctamente y cómo integrarlas en escenas interactivas.

---

## 🧠 Conceptos Aprendidos

- Carga y visualización de modelos GLTF animados con esqueleto.
- Control de animaciones (play, pause, velocidad, selección) en React Three Fiber.
- Sincronización de eventos de sonido con animaciones usando Web Audio API.
- Implementación de controles de usuario personalizados y panel flotante.
- Organización y documentación de proyectos de animación 3D interactiva.

---

## 🔧 Herramientas y Entornos

- **React Three Fiber** (JavaScript, React, Vite)
- **@react-three/drei** para utilidades y controles de cámara
- **Web Audio API** para síntesis y reproducción de sonidos
- **GLTF** (modelos animados en `/threejs/public/`)
- **Vite** para desarrollo rápido

---

## 📁 Estructura del Proyecto

```
threejs/
├── public/
│   ├── Dorchester3D.com_Rumba+Dancing/
│   │   └── Rumba Dancing.glb
│   ├── ImageToStl.com_Jump/
│   │   ├── Jump.glb
│   │   └── readme.txt
│   └── ImageToStl.com_Running+Up+Stairs/
│       └── Running Up Stairs.glb
├── src/
│   ├── App.jsx
│   ├── App.css
│   ├── index.css
│   ├── main.jsx
│   ├── components/
│   │   ├── AnimatedModel.jsx
│   │   ├── AnimatedScene.jsx
│   │   ├── AnimationControls.jsx
│   │   ├── ErrorBoundary.jsx
│   │   ├── SoundEventIndicator.jsx
│   │   └── SoundEventIndicator.css
│   └── utils/
│       └── SoundManager.js
├── index.html
├── package.json
├── vite.config.js
├── eslint.config.js
└── README.md
```

---

## 🧪 Implementación

### 🔹 Etapas realizadas por tecnología

#### React Three Fiber

1. **Carga de modelos GLTF animados**: Se utilizan modelos con esqueleto y animaciones (baile, salto, escaleras).
2. **Panel de controles flotante y arrastrable**: Permite seleccionar modelo, animación, velocidad y sonido.
3. **Selección y control de animaciones**: El usuario puede pausar, reproducir, cambiar velocidad y elegir animación.
4. **Sincronización de eventos de sonido**: Se dispara sonido paramétrico (sintético) en momentos clave de la animación.
5. **Indicador visual de eventos de sonido**: Muestra un ícono y nombre del evento sincronizado.
6. **Renderizado interactivo**: Cámara orbital, luces y entorno HDRI para realismo.

---

### 🔹 Código relevante

#### Exportación de modelos (GLTF)

Los modelos `.glb` se encuentran en la carpeta `public/` y fueron obtenidos de fuentes externas, listos para ser cargados en la escena.

#### React Three Fiber

Fragmento representativo del componente principal ([`App.jsx`](threejs/src/App.jsx)):

```jsx
import React, { useState } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls, Environment } from "@react-three/drei";
import AnimatedModel from "./components/AnimatedModel";
import ErrorBoundary from "./components/ErrorBoundary";
import SoundEventIndicator from "./components/SoundEventIndicator";
import "./App.css";

const models = [
  {
    name: "Bailando Rumba",
    path: "/Dorchester3D.com_Rumba+Dancing/Rumba Dancing.glb",
  },
  { name: "Saltando", path: "/ImageToStl.com_Jump/Jump.glb" },
  {
    name: "Subiendo Escaleras",
    path: "/ImageToStl.com_Running+Up+Stairs/Running Up Stairs.glb",
  },
];

function App() {
  // ...estados y lógica de controles...

  return (
    <div className="app">
      {/* Panel de controles flotante */}
      {/* ...ver App.jsx para detalles... */}
      <div className="canvas-container">
        <Canvas camera={{ position: [0, 2, 5], fov: 50 }} shadows>
          <ambientLight intensity={0.3} />
          <directionalLight position={[10, 10, 5]} intensity={1} castShadow />
          <ErrorBoundary>
            <AnimatedModel
              modelPath={selectedModel}
              currentAnimation={currentAnimation}
              setCurrentAnimation={setCurrentAnimation}
              setAvailableAnimations={setAvailableAnimations}
              isPlaying={isPlaying}
              animationSpeed={animationSpeed}
              soundEnabled={soundEnabled}
              soundVolume={soundVolume}
              onSoundEvent={setCurrentSoundEvent}
            />
          </ErrorBoundary>
          <mesh
            receiveShadow
            rotation={[-Math.PI / 2, 0, 0]}
            position={[0, -0.5, 0]}
          >
            <planeGeometry args={[20, 20]} />
            <shadowMaterial opacity={0.3} />
          </mesh>
          <Environment preset="sunset" />
          <OrbitControls enablePan enableZoom enableRotate />
        </Canvas>
      </div>
      {/* Indicador de eventos de sonido */}
      <SoundEventIndicator
        soundEvent={currentSoundEvent}
        onComplete={() => setCurrentSoundEvent(null)}
      />
    </div>
  );
}
```

#### Sistema de sonido paramétrico ([`SoundManager.js`](threejs/src/utils/SoundManager.js))

- Genera sonidos sintéticos para pasos, saltos, aplausos, etc.
- Mapea eventos de animación a sonidos y los dispara en tiempo real.

```js
// Ejemplo de mapeo de eventos
export const animationSoundEvents = {
  jump: [
    { time: 0.0, sound: "whoosh", volume: 0.6 },
    { time: 0.3, sound: "jump", volume: 0.8 },
    { time: 0.8, sound: "land", volume: 0.7 },
  ],
  // ...
};
```

#### Indicador visual de eventos de sonido

![gif](resultados/resultado.gif)

Muestra un ícono y nombre del evento de sonido sincronizado con la animación.

---

## 📊 Resultados Visuales

A continuación se muestran ejemplos de visualización de la escena animada y los eventos de sonido.

### Modelos animados

- **Bailando Rumba**: Modelo con animación de baile y eventos de beat/aplauso.
- **Saltando**: Modelo con animación de salto, sonido de despegue y aterrizaje.
- **Subiendo Escaleras**: Modelo con animación de pasos sincronizados.

### Interfaz y eventos

- Panel flotante para seleccionar modelo, animación, velocidad y sonido.
- Indicador visual central para cada evento de sonido (👣, 🦘, 💥, 🎵, 👏, 💨).

---

## 🧩 Prompts Usados

```text
"¿Cómo cargo y visualizo modelos GLTF animados en React Three Fiber?"
"¿Cómo sincronizo sonidos con animaciones en Three.js?"
"¿Cómo genero sonidos sintéticos con Web Audio API?"
"¿Cómo implemento un panel de controles flotante y arrastrable en React?"
"¿Cómo muestro un indicador visual para eventos de sonido?"
```

---

## 💬 Reflexión Final

Este taller permitió experimentar con la integración de animaciones esqueléticas avanzadas y retroalimentación sonora en la web. La combinación de controles interactivos, animaciones complejas y eventos de sonido en tiempo real enriquece la experiencia de usuario y acerca el flujo de trabajo a estándares profesionales de visualización 3D. El mayor reto fue la sincronización precisa entre animación y sonido, así como la gestión eficiente de recursos en la web. Para futuros proyectos, sería interesante añadir soporte para FBX, blending de animaciones y sonidos personalizados cargados desde
