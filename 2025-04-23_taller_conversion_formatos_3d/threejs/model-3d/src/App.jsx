import { useState, Suspense } from 'react'
import './App.css'

import { Canvas } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'
import SharkGLB from './SharkGLB.jsx'
import SharkGLTF from './SharkGLTF.jsx'

function App() {
  const [selectedModel, setSelectedModel] = useState('GLTF')

  const handleChange = (e) => {
    setSelectedModel(e.target.value)
  }

  // Colores dinámicos para el título según el modelo
  const titleColor = selectedModel === 'GLB' ? '#1976d2' : '#2e7d32'

  return (
    <>
      {/* Menú y título */}
      <div style={{ position: 'absolute', top: 10, left: 10, zIndex: 1 }}>
        <h1 style={{ color: titleColor }}>
          Modelo cargado: {selectedModel === 'GLB' ? 'Shark GLB' : 'Shark GLTF'}
        </h1>
        <select value={selectedModel} onChange={handleChange}>
          <option value="GLTF">Shark GLTF</option>
          <option value="GLB">Shark GLB</option>
        </select>
      </div>

      <Canvas
        camera={{ position: [10, 0, 0], fov: 50 }}
        style={{ background: 'lightblue', width: '100vw', height: '100vh' }}
      >
        <ambientLight intensity={1.8} />
        <OrbitControls />
        <Suspense fallback={null}>
          {selectedModel === 'GLB' ? (
            <SharkGLB scale={1} position={[0, 20, 0]} rotation={[0, -0.5 * Math.PI, 0]} />
          ) : (
            <SharkGLTF scale={1} position={[0, 20, 0]} rotation={[0, -0.5 * Math.PI, 0]} />
          )}
        </Suspense>
      </Canvas>
    </>
  )
}

export default App
