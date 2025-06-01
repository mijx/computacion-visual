import React, { Suspense, useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, useGLTF, useTexture } from '@react-three/drei';
import { Leva, useControls } from 'leva';

// Componente que carga y muestra el modelo con textura UV ajustable
 
function ModelViewer({ url }) {
  // Cargar modelo GLTF
  const { scene } = useGLTF(url);

  // Cargar textura de cuadrícula UV
  const texture = useTexture('/textures/uv_grid.png');

  // Controles Leva para parámetros UV
  const { repeatX, repeatY, offsetX, offsetY, wrapS, wrapT } = useControls('UV Params', {
    repeatX: { value: 1, min: 1, max: 10, step: 1 },
    repeatY: { value: 1, min: 1, max: 10, step: 1 },
    offsetX: { value: 0, min: 0, max: 1, step: 0.01 },
    offsetY: { value: 0, min: 0, max: 1, step: 0.01 },
    wrapS: { options: { Repeat: 1000, Clamp: 1001, Mirror: 1002 } },
    wrapT: { options: { Repeat: 1000, Clamp: 1001, Mirror: 1002 } }
  });

  // Memoizar configuración UV para no recargar cada render
  useMemo(() => {
    texture.wrapS = wrapS;
    texture.wrapT = wrapT;
    texture.repeat.set(repeatX, repeatY);
    texture.offset.set(offsetX, offsetY);
    texture.needsUpdate = true;
  }, [texture, repeatX, repeatY, offsetX, offsetY, wrapS, wrapT]);

  // Aplicar textura a todos los meshes del modelo
  scene.traverse((child) => {
    if (child.isMesh) {
      child.material.map = texture;
      child.material.needsUpdate = true;
    }
  });

  return <primitive object={scene} />;
}

// Componente principal
 
function App() {
  // Lista de modelos disponibles y estado seleccionado
  const models = [
    { name: 'piedra', url: '/models/piedra.glb' }
  ];
  const [selected, setSelected] = useState(models[0].url);

  return (
    <>
      <Leva collapsed />
      {/* Dropdown para elegir modelo */}
      <div style={{ position: 'absolute', top: 20, left: 20, zIndex: 1 }}>
        <label htmlFor="model-select" style={{ marginRight: '8px' }}>Modelo:</label>
        <select id="model-select" onChange={(e) => setSelected(e.target.value)}>
          {models.map((m) => (
            <option key={m.url} value={m.url}>{m.name}</option>
          ))}
        </select>
      </div>

      {/* Canvas 3D */}
      <Canvas camera={{ position: [0, 0, 5], fov: 45 }}
              style={{ width: '100vw', height: '100vh' }}>
        <ambientLight intensity={0.5} />
        <directionalLight position={[5, 5, 5]} intensity={1} />
        <Suspense fallback={null}>
          <ModelViewer url={selected} />
        </Suspense>
        <OrbitControls />
      </Canvas>
    </>
  );
}

// Montaje de la app en el DOM
const rootElement = document.getElementById('root');
const root = createRoot(rootElement);
root.render(<App />);

export default App;
