// App.jsx
import React, { useRef, useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { Canvas, useFrame } from '@react-three/fiber';
import * as THREE from 'three';

// Componente con shader y partículas
function DynamicScene() {
  const meshRef = useRef();
  const particlesRef = useRef();
  const [explosion, setExplosion] = useState(false);

  // Uniforms para animación y hover
  const uniforms = useMemo(() => ({
    uTime: { value: 0 },
    uHover: { value: 0 }
  }), []);

  // Vertex Shader: pasa las UV al fragment shader
  const vertexShader = `
    varying vec2 vUv;
    void main() {
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `;

  // Fragment Shader: efecto animado tipo energía radioactiva
  const fragmentShader = `
    uniform float uTime;
    uniform float uHover;
    varying vec2 vUv;

    float ripple(vec2 uv, float t) {
      return 0.5 + 0.5 * sin(10.0 * length(uv - 0.5) - t * 4.0);
    }

    void main() {
      float r = ripple(vUv, uTime);
      // Verde oscuro y verde claro (radioactivo)
      vec3 base = mix(vec3(0.0, 0.3, 0.0), vec3(0.6, 1.0, 0.3), r);
      float circle = smoothstep(0.5, 0.45, length(vUv - 0.5));
      base *= circle;
      base = mix(base, vec3(0.8, 1.0, 0.5), uHover);
      gl_FragColor = vec4(base, 1.0);
    }
  `;

  const material = useMemo(() => new THREE.ShaderMaterial({
    uniforms,
    vertexShader,
    fragmentShader
  }), [fragmentShader, uniforms, vertexShader]);

  const [particleSizes] = useState(() => new Float32Array(100).map(() => Math.random() * 0.1 + 0.02));
  const [particleColors] = useState(() => new Float32Array(100 * 3).map(() => Math.random()));

  const particles = useMemo(() => {
    const count = 100;
    const positions = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      positions[i * 3 + 0] = (Math.random() - 0.5) * 0.5;
      positions[i * 3 + 1] = (Math.random() - 0.5) * 0.5;
      positions[i * 3 + 2] = (Math.random() - 0.5) * 0.5;
    }
    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('size', new THREE.BufferAttribute(particleSizes, 1));
    geometry.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));
    return geometry;
  }, [particleSizes, particleColors]);

  // Actualizar tiempo, partículas y efectos en tiempo real
  useFrame((state, delta) => {
    uniforms.uTime.value += delta;

    if (particlesRef.current) {
      const sizes = particlesRef.current.geometry.attributes.size.array;
      const colors = particlesRef.current.geometry.attributes.color.array;
      for (let i = 0; i < sizes.length; i++) {
        sizes[i] = 0.02 + Math.sin(uniforms.uTime.value * 2 + i) * 0.02;
        colors[i * 3 + 0] = Math.abs(Math.sin(uniforms.uTime.value + i));
        colors[i * 3 + 1] = Math.abs(Math.cos(uniforms.uTime.value + i));
        colors[i * 3 + 2] = Math.abs(Math.sin(uniforms.uTime.value * 0.5 + i));
      }
      particlesRef.current.geometry.attributes.size.needsUpdate = true;
      particlesRef.current.geometry.attributes.color.needsUpdate = true;
    }

    if (explosion && particlesRef.current) {
      const positions = particlesRef.current.geometry.attributes.position.array;
      for (let i = 0; i < positions.length; i += 3) {
        positions[i] += (Math.random() - 0.5) * 0.1;
        positions[i + 1] += (Math.random() - 0.5) * 0.1;
        positions[i + 2] += (Math.random() - 0.5) * 0.1;
      }
      particlesRef.current.geometry.attributes.position.needsUpdate = true;
    }
  });

  return (
    <>
      {/* Objeto central interactivo */}
      <mesh
        ref={meshRef}
        material={material}
        onPointerOver={() => (uniforms.uHover.value = 1)}
        onPointerOut={() => (uniforms.uHover.value = 0)}
        onClick={() => setExplosion(true)}
      >
        <sphereGeometry args={[0.6, 64, 64]} />
      </mesh>

      {/* Partículas visuales */}
      <points ref={particlesRef} geometry={particles}>
        <pointsMaterial
          vertexColors
          size={0.05}
          sizeAttenuation
          transparent
          opacity={0.8}
        />
      </points>
    </>
  );
}

function App() {
  return (
    <Canvas
      camera={{ position: [0, 0, 3] }}
      style={{ width: '100vw', height: '100vh', background: '#111' }}
    >
      <ambientLight intensity={0.3} />
      <pointLight position={[5, 5, 5]} intensity={1} />
      <DynamicScene />
    </Canvas>
  );
}

const root = createRoot(document.getElementById('root'));
root.render(<App />);

export default App;