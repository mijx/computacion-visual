import { Physics, usePlane, useSphere } from '@react-three/cannon'
import { OrbitControls } from '@react-three/drei'
import React, { useState } from 'react'

// Crear un material físico con rebote
const ballProps = {
  mass: 1,
  args: [0.5],
  material: { restitution: 0.8 }, // rebote
}

function Floor() {
  const [ref] = usePlane(() => ({
    rotation: [-Math.PI / 2, 0, 0],
    material: { restitution: 0.8 }, // rebote en el suelo también
  }))
  return (
    <mesh ref={ref} receiveShadow>
      <planeGeometry args={[100, 100]} />
      <meshStandardMaterial color="#222" />
    </mesh>
  )
}

function Ball({ position }) {
  const [color, setColor] = useState('white')
  const [ref] = useSphere(() => ({
    ...ballProps,
    position,
    onCollide: () => {
      setColor('hotpink') // cambia color al colisionar
    },
  }))

  return (
    <mesh ref={ref} castShadow>
      <sphereGeometry args={[0.5, 32, 32]} />
      <meshStandardMaterial color={color} />
    </mesh>
  )
}

export default function App() {
  const startPosition = [0, 5, 0]

  return (
    <>
      <ambientLight intensity={0.4} />
      <directionalLight
        castShadow
        position={[5, 10, 5]}
        intensity={1.5}
        shadow-mapSize={1024}
      />
      <OrbitControls />
      <Physics>
        <Floor />
        {[...Array(5)].map((_, i) => (
          <Ball
            key={i}
            position={[startPosition[0], startPosition[1] + i * 0.5, startPosition[2]]}
          />
        ))}
      </Physics>
    </>
  )
}
