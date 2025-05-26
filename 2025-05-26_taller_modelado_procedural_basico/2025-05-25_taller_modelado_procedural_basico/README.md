# 🌳 Taller de Modelado Procedural Básico: Generación de Árboles 3D

## 📅 Fecha
`2025-05-25`

---

## 🎯 Objetivo del Taller

Implementar un generador procedural de árboles 3D utilizando React Three Fiber y Three.js, aplicando conceptos de recursividad y aleatoriedad controlada para crear estructuras orgánicas y visualmente interesantes.

---

## 🧠 Conceptos Aprendidos

- [x] Transformaciones geométricas (escala, rotación, traslación)
- [x] Generación procedural de geometría
- [x] Recursividad en modelado 3D
- [x] Sistemas de partículas y ramificación
- [x] Interactividad en tiempo real con Three.js

---

## 🔧 Herramientas y Entornos

- React Three Fiber
- Three.js
- React.js
- Vite

---

## 🧪 Implementación

### 🔹 Etapas realizadas
1. Implementación del sistema de generación recursiva de ramas
2. Desarrollo del control de profundidad y aleatoriedad
3. Creación de la interfaz de usuario para controlar parámetros
4. Implementación de controles de cámara y visualización 3D

### 🔹 Código relevante

El corazón del proyecto reside en la generación recursiva de ramas:

```jsx
const Branch = ({ position, rotation, depth, maxDepth, seed }) => {
  if (depth > maxDepth) return null;

  const length = 2 / (depth + 1);
  const radiusTop = 0.1 * (1 - depth / maxDepth);
  const radiusBottom = radiusTop + 0.05;

  // Usar el seed para generar números pseudo-aleatorios consistentes
  const random = () => {
    seed = (seed * 16807) % 2147483647;
    return (seed - 1) / 2147483646;
  };

  const numChildren = 2 + Math.floor(random() * 2);
  const childBranches = [];

  for (let i = 0; i < numChildren; i++) {
    const angle = (i / numChildren) * Math.PI * 2 + random() * 0.2;
    const childRotation = [
      -Math.PI / 4 + random() * 0.2,
      angle,
      0,
    ];

    childBranches.push(
      <Branch
        key={i}
        position={[0, length, 0]}
        rotation={childRotation}
        depth={depth + 1}
        maxDepth={maxDepth}
        seed={seed + i}
      />
    );
  }

  return (
    <group position={position} rotation={rotation}>
      <mesh position={[0, length / 2, 0]}>
        <cylinderGeometry args={[radiusTop, radiusBottom, length, 6]} />
        <meshStandardMaterial color="#8B4513" />
      </mesh>
      <group>
        {depth === maxDepth ? (
          <mesh position={[0, length, 0]}>
            <sphereGeometry args={[0.2, 6, 6]} />
            <meshStandardMaterial color="green" />
          </mesh>
        ) : (
          childBranches
        )}
      </group>
    </group>
  );
};

const TreeScene = () => {
  const [maxDepth, setMaxDepth] = useState(5);
  const [seed, setSeed] = useState(Math.random() * 1000000);

  const handleRegenerate = () => {
    setSeed(Math.random() * 1000000);
  };

  return (
    <>
      <Canvas id="canvas" camera={{ position: [0, 5, 10], fov: 50 }}>
        <ambientLight intensity={0.5} />
        <directionalLight position={[5, 10, 5]} intensity={1} />
        <Grid
          args={[20, 20]}
          cellSize={1}
          cellThickness={1}
          cellColor="#6f6f6f"
          sectionSize={5}
        />
        <Branch
          position={[0, 0, 0]}
          rotation={[0, 0, 0]}
          depth={0}
          maxDepth={maxDepth}
          seed={seed}
        />
        <OrbitControls />
      </Canvas>
      <Controls
        maxDepth={maxDepth}
        setMaxDepth={setMaxDepth}
        onRegenerate={handleRegenerate}
      />
    </>
  );
};
```

---

## 📊 Resultados Visuales

![demo](resultados/demo.gif)

---

## 💬 Reflexión Final

Este proyecto permitió explorar conceptos fundamentales de la generación procedural de contenido 3D. La implementación de un sistema recursivo para la creación de estructuras orgánicas presentó desafíos interesantes, especialmente en el balance entre aleatoriedad y control para generar resultados visualmente atractivos.

La parte más compleja fue implementar un sistema de generación de ramas que produjera resultados naturales y variados, mientras se mantenía un rendimiento aceptable incluso con árboles de gran profundidad.

Para futuras iteraciones, sería interesante implementar:
- Texturas y materiales más realistas
- Animaciones de crecimiento
- Variaciones en el tipo de árbol
- Sistema de estaciones que afecte la apariencia