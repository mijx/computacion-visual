// App.jsx
import React, { useRef, useMemo } from 'react';
import { createRoot } from 'react-dom/client';
import { Canvas, useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import { Leva, useControls } from 'leva';

// Componente que define el objeto con shader personalizado
function ShaderObject() {
  const meshRef = useRef();

  // Uniforms básicos: tiempo y factor de velocidad desde el slider
  const uniforms = useMemo(
    () => ({
      uTime: { value: 0.0 },
      uSpeed: { value: 1.0 }
    }), []
  );

  // Slider Leva para controlar la velocidad de animación
  useControls('Animación', {
    speed: {
      value: 1,
      min: 0,
      max: 5,
      step: 0.1,
      onChange: (v) => { uniforms.uSpeed.value = v; }
    }
  });

  // Vertex Shader: transmite normales y coordenadas UV al fragment
  const vertexShader = /* glsl */`
    varying vec3 vNormal;
    varying vec2 vUv;
    void main() {
      vNormal = normal;
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `;

  // Fragment Shader: gradiente, pulso animado, toon shading y contorno UV
  const fragmentShader = /* glsl */`
    uniform float uTime;
    uniform float uSpeed;
    varying vec3 vNormal;
    varying vec2 vUv;

    void main() {
      // Gradiente vertical según UV.y
      vec3 gradColor = mix(vec3(0.0, 0.5, 1.0), vec3(1.0, 0.5, 0.0), vUv.y);

      // Animación pulsante basada en uTime y uSpeed
      float pulse = 0.5 + 0.5 * sin(uTime * uSpeed);
      vec3 pulseColor = mix(vec3(1.0), vec3(1.0, 0.0, 1.0), pulse);

      // Toon shading (3 niveles)
      vec3 lightDir = normalize(vec3(1.0, 1.0, 1.0));
      float diff = max(dot(normalize(vNormal), lightDir), 0.0);
      float toon = floor(diff * 3.0) / 3.0;

      // Combinar gradiente y pulso con toon shading
      vec3 color = mix(gradColor, pulseColor, 0.5) * toon;

      // Contorno estilo wireframe en UV
      vec2 grid = abs(fract(vUv * 8.0 - 0.5) - 0.5) / fwidth(vUv * 8.0);
      float line = min(grid.x, grid.y);
      float edge = 1.0 - min(line, 1.0);
      color = mix(color, vec3(0.0), edge);

      gl_FragColor = vec4(color, 1.0);
    }
  `;

  // Crear ShaderMaterial con los shaders y uniforms
  const shaderMaterial = useMemo(
    () => new THREE.ShaderMaterial({
      uniforms,
      vertexShader,
      fragmentShader
    }), [uniforms, vertexShader, fragmentShader]
  );

  // Actualizar uTime en cada frame respecto a uSpeed
  useFrame((state, delta) => {
    uniforms.uTime.value += delta;
    meshRef.current.material.uniforms.uTime.value = uniforms.uTime.value;
  });

  return (
    <mesh ref={meshRef} material={shaderMaterial}>
      {/* Geometría central: esfera */}
      <sphereGeometry args={[1, 64, 64]} />
    </mesh>
  );
}

// Componente principal de la aplicación
function App() {
  return (
    <>
      {/* Panel Leva para sliders */}
      <Leva collapsed={false} />

      <Canvas
        camera={{ position: [0, 0, 3], fov: 50 }}
        style={{ width: '100vw', height: '100vh' }}
      >
        <ambientLight intensity={0.3} />
        <directionalLight position={[5, 5, 5]} intensity={1} />
        <ShaderObject />
      </Canvas>
    </>
  );
}

// Montaje en el DOM
const root = createRoot(document.getElementById('root'));
root.render(<App />);

export default App;
