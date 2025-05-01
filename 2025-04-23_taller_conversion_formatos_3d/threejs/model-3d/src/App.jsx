import { useState, Suspense } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

// Importar canvas y orbit controls para interactividad
import { Canvas } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'
import MouseGLB from './MouseGLB.jsx'
import Shark from './Shark.jsx'

function App() {
  const [count, setCount] = useState(0)
  return (
    <>
      <Canvas
      camera={{ position: [10, 0, 0], fov: 50}}
      style={{ background: 'lightblue', width: '100vw', height: '100vh' }}
      >
        <ambientLight intensity={1.8} />
        <OrbitControls />
        <Suspense fallback={null}>
          <Shark scale={1} position={[0, 20, 0]} rotation={[0, -0.5*Math.PI, 0]}/>
        </Suspense>
      </Canvas>
    </>
  )
}

export default App
