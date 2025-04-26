import { Canvas } from '@react-three/fiber'
import { useControls } from 'leva'
import { useRef } from 'react'

function Scene() {
  const groupRef = useRef()
  const child1Ref = useRef()
  const child2Ref = useRef()

  // Sliders de leva para rotación y posición del nodo padre
  const { rotateYFather, moveYFather } = useControls({
    rotateYFather: { value: 0, min: -Math.PI, max: Math.PI, step: 0.01 },
    moveYFather: { value: 0, min: -5, max: 5, step: 0.1 }
  })

  // Sliders para rotar y trasladar el hijo 1 (cubo rosa)
  const { rotateXChild1, moveXChild1 } = useControls({
    rotateXChild1: { value: 0, min: -Math.PI, max: Math.PI, step: 0.01 },
    moveXChild1: { value: -2, min: -5, max: 5, step: 0.1 }
  })

  // Sliders para rotar y trasladar el hijo 2 (cubo azul)
  const { rotateXChild2, moveXChild2 } = useControls({
    rotateXChild2: { value: 0, min: -Math.PI, max: Math.PI, step: 0.01 },
    moveXChild2: { value: 2, min: -5, max: 5, step: 0.1 }
  })

  return (
    <Canvas>
      {/* Cámara y luces básicas */}
      <ambientLight />
      <pointLight position={[5, 5, 5]} intensity={2} />

      {/* Nodo padre */}
      <group ref={groupRef} rotation={[0, rotateYFather, 0]} position={[0, moveYFather, 0]}>
        {/* Hijo 1 (con controles de rotación y traslación en X) */}
        <mesh
          ref={child1Ref}
          position={[moveXChild1, 0, 0]} // Traslación en X
          rotation={[rotateXChild1, 0, 0]} // Rotación en X
        >
          <boxGeometry args={[1, 1, 1]} />
          <meshStandardMaterial color="hotpink" />
        </mesh>

        {/* Hijo 2 (con controles de rotación y traslación en X) */}
        <mesh
          ref={child2Ref}
          position={[moveXChild2, 0, 0]} // Traslación en X
          rotation={[rotateXChild2, 0, 0]} // Rotación en X
        >
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
