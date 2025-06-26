import React, { useState, useEffect } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Environment } from '@react-three/drei';
import AnimatedModel from './components/AnimatedModel';  // Importar el componente AnimatedModel
import AnimationControls from './components/AnimationControls';  // Importar el componente AnimationControls

function App() {
  const [currentAnimation, setCurrentAnimation] = useState('Idle');

  const changeAnimation = (animation) => {
    setCurrentAnimation(animation);
  };

  return (
    <>
      {/* Controles de animación */}
      <AnimationControls changeAnimation={changeAnimation} />

      {/* Canvas 3D */}
      <Canvas camera={{ position: [0, 2, 5], fov: 50 }}>
        {/* Entorno y luces */}
        <ambientLight intensity={0.4} />
        <directionalLight position={[10, 10, 5]} intensity={1.2} />
        <Environment preset="sunset" />
        
        {/* Modelo 3D animado */}
        <AnimatedModel currentAnimation={currentAnimation} onAnimationComplete={changeAnimation} />
        
        {/* Controles de cámara */}
        <OrbitControls />
      </Canvas>
    </>
  );
}

export default App;
