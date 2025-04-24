import { useState, Suspense } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

// Importar canvas y orbit controls para interactividad
import { Canvas } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'
import Mouse from './Mouse.jsx'

function App() {
  const [count, setCount] = useState(0)
  return (
    <>
      <Canvas style={{ background: 'lightblue', width: '100vw', height: '100vh' }}>
        <ambientLight intensity={1.8} />
        <OrbitControls />
        <Suspense fallback={null}>
          <Mouse scale={0.55} position={[0, 0, 0]} />
        </Suspense>
      </Canvas>
    </>
  )
}

export default App
