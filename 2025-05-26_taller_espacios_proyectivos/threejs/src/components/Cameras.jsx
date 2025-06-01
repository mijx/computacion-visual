import React from 'react'
import {
  OrbitControls,
  PerspectiveCamera,
  OrthographicCamera,
} from '@react-three/drei'

export default function Cameras({ isPerspective, perspFov, orthoZoom }) {
  const left = -orthoZoom
  const right = orthoZoom
  const top = orthoZoom
  const bottom = -orthoZoom

  return (
    <>
      {isPerspective ? (
        <PerspectiveCamera
          makeDefault
          position={[0, 0, 10]}
          fov={perspFov}
          near={0.1}
          far={1000}
        />
      ) : (
        <OrthographicCamera
          makeDefault
          position={[0, 0, 10]}
          zoom={1}
          near={0.1}
          far={1000}
          left={left}
          right={right}
          top={top}
          bottom={bottom}
        />
      )}

      <OrbitControls
        enableDamping
        dampingFactor={0.1}
        rotateSpeed={0.7}
        zoomSpeed={0.5}
      />
    </>
  )
}
