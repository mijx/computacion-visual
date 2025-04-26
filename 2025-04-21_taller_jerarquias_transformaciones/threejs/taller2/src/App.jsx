import { Canvas } from '@react-three/fiber'
import { useControls } from 'leva'
import { useRef } from 'react'

function Scene() {
  const groupRef = useRef()

  // Sliders de leva para rotación en Y y posición en Y
  const { rotationY, positionY } = useControls({
    rotationY: { value: 0, min: -Math.PI, max: Math.PI, step: 0.01 },
    positionY: { value: 0, min: -5, max: 5, step: 0.1 }
  })

  return (
    <Canvas>
      {/* Cámara y luces básicas */}
      <ambientLight />
      <pointLight position={[5, 5, 5]} intensity={2} />

      {/* Nodo padre */}
      <group ref={groupRef} rotation={[0, rotationY, 0]} position={[0, positionY, 0]}>
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
