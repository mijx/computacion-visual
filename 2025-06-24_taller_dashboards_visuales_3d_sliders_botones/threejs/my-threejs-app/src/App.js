import React, { useRef, useState } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { useControls } from 'leva';

// Componente para el cubo 3D
function MyBox() {
  // Referencia al mesh para acceder a sus propiedades
  const meshRef = useRef();
  // Estado para controlar la rotación automática
  const [autoRotate, setAutoRotate] = useState(false);

  // Definir controles con Leva
  // Se ha modificado la forma de definir el botón 'Rotación Automática'
  // Ahora es una función directamente, lo que Leva interpreta como un botón
  const { scale, color } = useControls({
    scale: { value: 1, min: 0.1, max: 3, step: 0.1, label: 'Escala' },
    color: { value: '#ff0000', label: 'Color Material' },
    'Rotación Automática': () => setAutoRotate((prev) => !prev), // Leva interpreta funciones como botones
  });

  // Usar useFrame para animaciones o actualizaciones por frame
  useFrame(() => {
    if (meshRef.current && autoRotate) {
      meshRef.current.rotation.x += 0.01;
      meshRef.current.rotation.y += 0.01;
    }
  });

  return (
    <mesh ref={meshRef} scale={[scale, scale, scale]}>
      {/* Geometría de la caja */}
      <boxGeometry args={[1, 1, 1]} />
      {/* Material del mesh, usando el color de Leva */}
      <meshStandardMaterial color={color} />
    </mesh>
  );
}

// Componente principal de la aplicación
export default function App() {
  // Controles para la luz (bonus)
  const { lightIntensity, lightColor, lightPositionX, lightPositionY, lightPositionZ } = useControls('Luz', {
    lightIntensity: { value: 1, min: 0, max: 5, step: 0.1, label: 'Intensidad de Luz' },
    lightColor: { value: '#ffffff', label: 'Color de Luz' },
    lightPositionX: { value: 5, min: -10, max: 10, step: 0.1, label: 'Posición X' },
    lightPositionY: { value: 5, min: -10, max: 10, step: 0.1, label: 'Posición Y' },
    lightPositionZ: { value: 5, min: -10, max: 10, step: 0.1, label: 'Posición Z' },
  });

  return (
    <div style={{ height: '100vh', width: '100vw', background: '#222' }}>
      {/* Canvas de Three.js con react-three-fiber */}
      <Canvas camera={{ position: [0, 0, 5], fov: 75 }}>
        {/* Luz ambiente para una iluminación básica */}
        <ambientLight intensity={0.5} />
        {/* Luz direccional, controlada por Leva */}
        <directionalLight
          position={[lightPositionX, lightPositionY, lightPositionZ]}
          intensity={lightIntensity}
          color={lightColor}
        />
        {/* Componente del cubo */}
        <MyBox />
        {/* Controles de órbita para mover la cámara */}
        <OrbitControls />
      </Canvas>
    </div>
  );
}
