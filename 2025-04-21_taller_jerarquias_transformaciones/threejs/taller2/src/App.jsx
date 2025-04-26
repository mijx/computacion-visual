import { Canvas } from '@react-three/fiber'

function Scene() {
  return (
    <Canvas>
      {/* Cámara y luces básicas */}
      <ambientLight />
      <pointLight position={[10, 10, 10]} />

      {/* Nodo padre */}
      <group>
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
