import React from 'react'

export default function SceneObjects() {
  return (
    <>
      <mesh position={[0, 0, 0]} castShadow receiveShadow>
        <boxGeometry args={[1, 1, 1]} />
        <meshStandardMaterial color="#e74c3c" />
      </mesh>

      <mesh position={[-2, 1, -3]} castShadow receiveShadow>
        <sphereGeometry args={[0.75, 32, 32]} />
        <meshStandardMaterial color="#27ae60" />
      </mesh>

      <mesh position={[2, -1, -6]} castShadow receiveShadow>
        <torusGeometry args={[0.75, 0.3, 16, 100]} />
        <meshStandardMaterial color="#2980b9" />
      </mesh>
    </>
  )
}
