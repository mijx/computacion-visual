import React, { useState } from 'react'
import { Canvas } from '@react-three/fiber'
import SceneObjects from './components/SceneObjects'
import Cameras from './components/Cameras'
import CameraUI from './components/CameraUI'

export default function App() {
  const [isPerspective, setIsPerspective] = useState(true)
  const [orthoZoom, setOrthoZoom] = useState(5)
  const [perspFov, setPerspFov] = useState(50)

  return (
    <div style={styles.appContainer}>
      <div style={styles.canvasContainer}>
        <Canvas
          shadows
          style={{ height: '100%', width: '100%' }}
          camera={{ position: [0, 0, 10], near: 0.1, far: 1000 }}
        >
          <ambientLight intensity={0.5} />
          <directionalLight
            castShadow
            position={[10, 10, 10]}
            intensity={1}
            shadow-mapSize-width={1024}
            shadow-mapSize-height={1024}
          />
          <SceneObjects />
          <Cameras
            isPerspective={isPerspective}
            perspFov={perspFov}
            orthoZoom={orthoZoom}
          />
        </Canvas>
      </div>

      <div style={styles.panelContainer}>
        <CameraUI
          isPerspective={isPerspective}
          setIsPerspective={setIsPerspective}
          perspFov={perspFov}
          setPerspFov={setPerspFov}
          orthoZoom={orthoZoom}
          setOrthoZoom={setOrthoZoom}
        />
      </div>
    </div>
  )
}

const styles = {
  appContainer: {
    display: 'flex',
    height: '100vh',
    width: '100vw',
    overflow: 'hidden',
    backgroundColor: '#1c1c1c',
  },
  canvasContainer: {
    flex: 1,         // ocupa todo el espacio restante
    height: '100%',
  },
  panelContainer: {
    width: 360,      // ancho fijo para panel de control
    padding: '20px',
    boxSizing: 'border-box',
    backgroundColor: 'rgba(20,20,20,0.95)',
    boxShadow: '0 0 15px rgba(0,0,0,0.8)',
  },
}
