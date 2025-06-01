import React, { useRef, useState, useEffect } from 'react'
import { useFrame } from '@react-three/fiber'

export default function InteractiveBox({ color, scale, rotationActive }) {
  const meshRef = useRef()
  const [clicked, setClicked] = useState(false)

  useFrame((state, delta) => {
    if (rotationActive && meshRef.current) {
      meshRef.current.rotation.x += delta * 0.5
      meshRef.current.rotation.y += delta * 0.7
    }
  })

  return (
    <mesh
      ref={meshRef}
      scale={scale}
      onClick={() => setClicked(!clicked)}
      castShadow
      receiveShadow
    >
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color={clicked ? 'hotpink' : color} />
    </mesh>
  )
}
