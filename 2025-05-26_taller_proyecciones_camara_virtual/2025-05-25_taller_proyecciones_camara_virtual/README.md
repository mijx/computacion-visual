# 🧪 Exploración de Proyecciones de Cámara con React Three Fiber

## 📅 Fecha
`2025-05-25`

---

## 🎯 Objetivo del Taller

El objetivo de este taller es entender cómo se genera una escena tridimensional desde el punto de vista de una cámara, explorando los efectos de proyección en perspectiva y ortográfica. Se busca visualizar cómo los cambios en la cámara (tipo y parámetros) afectan directamente la representación en pantalla y comprender el papel conceptual de las matrices de proyección mediante el uso de React Three Fiber.

---

## 🧠 Conceptos Aprendidos

Lista los principales conceptos aplicados:

- [x] Proyección Perspectiva y sus parámetros (FOV, aspect, near, far).
- [x] Proyección Ortográfica y sus parámetros (left, right, top, bottom, zoom, near, far).
- [x] Diferencias visuales entre proyecciones.
- [x] Uso de React Three Fiber (`@react-three/fiber`) para crear escenas 3D.
- [x] Componentes de `@react-three/drei` como `OrbitControls`, `Grid`, `Html`, `Stats`.
- [x] Manejo de estado en React para controlar el tipo de cámara.
- [x] Configuración de iluminación (ambiental y direccional) y sombras.
- [x] Creación de interfaces de usuario (HUD) dentro de un canvas 3D con `<Html>`.
- [x] Uso de `leva` para controles de GUI interactivos.
- [x] Renderizado 3D en el navegador y manipulación de cámara.

---

## 🔧 Herramientas y Entornos

Especifica los entornos usados:

- React Three Fiber (`@react-three/fiber`, `@react-three/drei`)
- `leva` (para controles de GUI)
- `three` (como motor subyacente de R3F)
- React.js con Vite
- Node.js y npm para la gestión de dependencias y ejecución del proyecto.

📌 Se utilizaron las herramientas según las guías de instalación y configuración estándar para un proyecto de React con Vite.

---


## 🧪 Implementación

Explica el proceso:

### 🔹 Etapas realizadas
1.  **Configuración Inicial**: Creación de un proyecto React + Vite.
2.  **Instalación de Dependencias**: Se añadieron `@react-three/fiber`, `@react-three/drei`, `three`, y `leva`.
3.  **Creación de Componentes Base**:
    *   `MetalCube`: Componente para renderizar cubos 3D con material metálico y capacidad de proyectar sombras.
    *   `CameraViewHUD`: Componente para mostrar el tipo de cámara activa ("Perspective View" / "Orthographic View") usando `<Html>` de `@react-three/drei`.
4.  **Componente Principal `App`**:
    *   Se utilizó `leva` para crear un control que permite al usuario alternar la variable de estado `isPerspective`.
    *   Se definió `cameraConfig` que ajusta los parámetros de la cámara (FOV, frustum, posición, zoom) dinámicamente según `isPerspective`.
5.  **Configuración del `Canvas` R3F**:
    *   Se configuró el `Canvas` para habilitar sombras (`shadows`).
    *   La prop `orthographic={!isPerspective}` y una `key` dinámica (`key={isPerspective ? 'perspective' : 'orthographic'}`) se usaron para forzar la reconstrucción de la cámara al cambiar de tipo.
    *   Se pasaron las propiedades de `cameraConfig` al prop `camera` del `Canvas`, incluyendo `makeDefault: true`.
6.  **Escena 3D**:
    *   Se añadieron varias instancias de `MetalCube` con diferentes colores, posiciones y escalas.
    *   Se implementó un suelo utilizando el componente `<Grid>` de `@react-three/drei`, configurado para ser infinito y recibir sombras.
    *   Se configuró iluminación con `<ambientLight>` y `<directionalLight>`, esta última para proyectar sombras.
7.  **Interactividad y Ayudas Visuales**:
    *   Se añadió `<OrbitControls makeDefault />` para permitir la manipulación de la cámara (rotar, pan, zoom).
    *   Se incluyó el componente `<CameraViewHUD>` dentro del `Canvas` para el texto informativo.
    *   Se añadió `<Stats />` para monitorizar el rendimiento.
8.  **Estilización**: Se modificó `App.css` para dar estilo al contenedor del canvas y al texto del HUD.

### 🔹 Código relevante

Fragmento del componente `App.jsx` mostrando la configuración del Canvas y la lógica de cambio de cámara:

```jsx
function MetalCubeScene({ isPerspective, cameraConfig }) {
  return (
      <Canvas
      shadows
      key={isPerspective ? 'perspective' : 'orthographic'} // Force re-render on camera type change
      orthographic={!isPerspective}
      camera={{
        ...cameraConfig,
        // Explicitly tell R3F which type of camera to create
        // This is crucial for the orthographic prop to work correctly with initial camera settings
        makeDefault: true, // Ensure this camera is the default
      }}
      style={{ backgroundColor: '#1a1a1a' }}
    >
      <ambientLight intensity={0.6} />
      <directionalLight
        castShadow
        position={[10, 15, 10]}
        intensity={1.5}
        shadow-mapSize-width={2048}
        shadow-mapSize-height={2048}
        shadow-camera-far={50}
        shadow-camera-left={-10}
        shadow-camera-right={10}
        shadow-camera-top={10}
        shadow-camera-bottom={-10}
      />

      <MetalCube color="#ff4136" position={[-2, 0.5, 0]} />
      <MetalCube color="#0074d9" position={[0, 0.5, -2]} scale={[0.8, 0.8, 0.8]} />
      <MetalCube color="#2ecc40" position={[2, 0.5, 0]} />
      <MetalCube color="#ffdc00" position={[0, 0.5, 2]} scale={[1.2, 1.2, 1.2]} />

      <Grid
        receiveShadow
        args={[30, 30]}
        position={[0, -0.01, 0]} // Slightly below cubes to avoid z-fighting
        cellSize={0.5}
        cellThickness={1}
        cellColor={new THREE.Color('#6f6f6f')}
        sectionSize={2.5}
        sectionThickness={1.5}
        sectionColor={new THREE.Color('#444444')}
        fadeDistance={35}
        fadeStrength={1}
        infiniteGrid
      />

      <OrbitControls makeDefault />
      <CameraViewHUD isPerspective={isPerspective} />
    </Canvas>
  );
}

function App() {
  const { isPerspective } = useControls({
    isPerspective: {
      value: true,
      label: 'Toggle Camera',
    },
  });

  const cameraConfig = isPerspective
    ? { // Perspective Camera Configuration
        fov: 75,
        position: [5, 4, 5],
        near: 0.1,
        far: 1000,
      }
    : { // Orthographic Camera Configuration
        left: -5,
        right: 5,
        top: 5,
        bottom: -5,
        position: [5, 4, 5],
        zoom: 1,
        near: 0.1,
        far: 1000,
      };

  return (
    <div id="canvas-container">
      <Leva />
      <MetalCubeScene isPerspective={isPerspective} cameraConfig={cameraConfig} />
    </div>
  );
}
```

---

## 📊 Resultados Visuales

![demo](resultados/demo.gif)
---

## 🧩 Prompts Usados

El prompt inicial que guio el desarrollo fue:

```text
Quiero entender cómo se genera una escena tridimensional desde el punto de vista de una cámara, explorando los efectos de proyección en perspectiva y ortográfica. El propósito de este proyecto es visualizar cómo los cambios en la cámara afectan directamente la representación en pantalla, y comprender el papel de las matrices de proyección.

Modifica este proyecto de React + VITE para que usando las herramientas de React Three Fiber, haga lo siguiente:

- Crear una escena básica con varios <Box /> o <Sphere /> distribuidos a diferentes distancias del usuario.
- Usar una <PerspectiveCamera> y un <OrthographicCamera>, alternables con un botón o estado React.
- Utilizar OrbitControls para permitir manipulación de la cámara en tiempo real.
- Mostrar información textual en pantalla:
    * Tipo de cámara activa.
    * Valores de fov, aspect, near, far (para perspectiva).
    * Tamaños de left, right, top, bottom (para ortográfica).
```
Durante el desarrollo, se utilizaron prompts adicionales para refinar la implementación, solucionar errores y mejorar la calidad visual, interactuando con el asistente de IA.

📎 Usa buenas prácticas de prompts según la [guía de IA actualizada](./guia_prompts_inteligencias_artificiales_actualizada.md)

---

## 💬 Reflexión Final

Responde en 2-3 párrafos:

Este taller fue una excelente introducción práctica a los conceptos de proyección de cámara en gráficos 3D por computadora, utilizando la biblioteca React Three Fiber. Se reforzó la comprensión de cómo los parámetros de las cámaras de perspectiva (FOV, aspect ratio) y ortográficas (planos de frustum, zoom) alteran fundamentalmente la percepción de la profundidad y la escala en una escena. La capacidad de alternar entre los dos tipos de cámara en tiempo real, junto con los controles orbitales, proporcionó una forma intuitiva de observar estas diferencias.

La parte más interesante fue configurar la lógica para el cambio dinámico de cámaras y asegurar que los parámetros se aplicaran correctamente para cada tipo, especialmente al integrar el control de `leva`. También fue un buen ejercicio de depuración entender por qué ciertos hooks de R3F no funcionaban fuera del contexto del `Canvas` o cómo renderizar HTML (`<Html>`) dentro de la escena 3D. El aspecto más desafiante fue inicialmente lograr una diferencia visual clara entre las dos proyecciones, lo que requirió ajustar la disposición de la escena y los parámetros de la cámara de forma más significativa.

En futuros proyectos, aplicaría estos conocimientos para crear visualizaciones más complejas o herramientas interactivas para la educación en gráficos por computadora. Mejoraría este taller añadiendo más controles interactivos (por ejemplo, sliders en `leva` para FOV, zoom, posición de la cámara), más tipos de geometrías, y quizás una representación visual del frustum de la cámara.
