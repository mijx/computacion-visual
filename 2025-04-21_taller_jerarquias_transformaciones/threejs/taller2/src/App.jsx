import { Canvas } from '@react-three/fiber'
import { useControls } from 'leva'
import { useRef } from 'react'

function Scene() {
  const groupRef = useRef()

  // Slider de leva para rotación en Y
  const { rotationY } = useControls({
    rotationY: { value: 0, min: -Math.PI, max: Math.PI, step: 0.01 }
  })

  return (
    <Canvas>
      {/* Cámara y luces básicas */}
      <ambientLight />
      <pointLight position={[5, 5, 5]} intensity={2} />

      {/* Nodo padre */}
      <group ref={groupRef} rotation={[0, rotationY, 0]}>
        {/* Hijo 1 */}
        <mesh position={[-2, 0, 0]}>
          <boxGeometry args={[1, 1, 1]} />
          <meshStandardMaterial color="hotpink" />
        </mesh>

        {/* Hijo 2 */}
        <mesh position={[2, 0, 0]}>
          <boxGeometry args={[1, 1, 1]} />
          <meshStandardMaterial color="skyblue" />
        </mesh>
      </group>
    </Canvas>
  )
}

export default function App() {
  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      <Scene />
    </div>
  )
}
