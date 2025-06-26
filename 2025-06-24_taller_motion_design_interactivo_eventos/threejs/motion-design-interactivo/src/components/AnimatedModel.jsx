import { useState, useEffect, useRef } from 'react';
import { useGLTF, useAnimations } from '@react-three/drei';

const AnimatedModel = ({ currentAnimation, onAnimationComplete }) => {
  const { scene, animations } = useGLTF('/models/result.gltf');  // Asegúrate de que la ruta sea correcta
  const { actions } = useAnimations(animations, scene);
  const group = useRef();

  useEffect(() => {
    if (actions[currentAnimation]) {
      actions[currentAnimation].play();
    }

    return () => {
      if (actions[currentAnimation]) actions[currentAnimation].stop();
    };
  }, [currentAnimation, actions]);

  return (
    <group ref={group}>
      <primitive object={scene} />
    </group>
  );
};

export default AnimatedModel;
