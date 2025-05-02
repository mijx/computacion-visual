import React from 'react'
import { Canvas } from '@react-three/fiber'
import { OrbitControls, Environment } from '@react-three/drei'
import { useControls } from 'leva'
import Model from './Burger'

const objects = [
  { position: [0, 0, 0], rotation: [0, Math.PI / 4, 0], scale: 3 },
  { position: [2, 0, 5], rotation: [0, Math.PI / 2, 0], scale: 3 },
  { position: [-5, 0, -1], rotation: [0, -Math.PI / 6, 0], scale: 3 },
]

export default function App() {
  const objectControls = objects.map((obj, index) =>
    useControls(`Object ${index + 1}`, {
      rotationY: { value: obj.rotation[1], min: -Math.PI, max: Math.PI, step: 0.01 },
      scale: { value: obj.scale, min: 1, max: 5, step: 0.1 },
    })
  )

  return (
    <div style={{ width: '100vw', height: '100vh', margin: 0, overflow: 'hidden' }}>
      <Canvas camera={{ position: [-3, 6, 13], fov: 50 }}>
        <ambientLight intensity={0.5} />
        <directionalLight position={[5, 5, 5]} intensity={1} />
        <Environment preset="sunset" />
        <OrbitControls />
        {objects.map((obj, index) => (
          <Model
            key={index}
            position={obj.position}
            rotation={[obj.rotation[0], objectControls[index].rotationY, obj.rotation[2]]}
            scale={objectControls[index].scale}
          />
        ))}
      </Canvas>
    </div>
  )
}
