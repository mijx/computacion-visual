import React, { useState, useEffect } from 'react'
import { Canvas } from '@react-three/fiber'
import { OrbitControls, Stats } from '@react-three/drei'
import InteractiveBox from './components/InteractiveBox'
import './App.css'

export default function App() {
  const [rotationActive, setRotationActive] = useState(false)
  const [color, setColor] = useState('#4169e1') // royalblue
  const [scale, setScale] = useState(1)

  // Detectar tecla 'r' para resetear
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'r') {
        setRotationActive(false)
        setColor('#4169e1')
        setScale(1)
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [])

  return (
    <>
      <Canvas
        shadows
        camera={{ position: [3, 3, 5], fov: 60 }}
        style={{ height: '100vh', background: '#121212' }}
      >
        <ambientLight intensity={0.4} />
        <directionalLight
          position={[5, 10, 7]}
          intensity={0.8}
          castShadow
          shadow-mapSize-width={1024}
          shadow-mapSize-height={1024}
        />
        <InteractiveBox color={color} scale={scale} rotationActive={rotationActive} />
        <OrbitControls enableDamping dampingFactor={0.1} />
        <Stats />
      </Canvas>

      <div className="ui-panel">
        <h2>Control del Cubo</h2>

        <label htmlFor="rotationToggle">Rotación automática</label>
        <button onClick={() => setRotationActive(!rotationActive)}>
          {rotationActive ? 'Detener rotación' : 'Iniciar rotación'}
        </button>

        <label htmlFor="colorPicker">Color</label>
        <input
          id="colorPicker"
          type="color"
          value={color}
          onChange={(e) => setColor(e.target.value)}
        />

        <label htmlFor="scaleRange">Tamaño</label>
        <input
          id="scaleRange"
          type="range"
          min={0.5}
          max={3}
          step={0.01}
          value={scale}
          onChange={(e) => setScale(parseFloat(e.target.value))}
        />

        <p style={{ marginTop: '10px', fontSize: '0.9rem', color: '#ccc' }}>
          Presiona <b>r</b> para resetear valores.
        </p>
      </div>
    </>
  )
}