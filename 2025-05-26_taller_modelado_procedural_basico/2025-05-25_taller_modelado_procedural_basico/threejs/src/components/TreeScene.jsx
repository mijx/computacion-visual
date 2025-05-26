// TreeGenerator.jsx
import React, { useState } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Grid } from '@react-three/drei';
import * as THREE from 'three';

// Componente de una rama
const Branch = ({ position, rotation, depth, maxDepth, seed }) => {
  if (depth > maxDepth) return null;

  const length = 2 / (depth + 1);
  const radiusTop = 0.1 * (1 - depth / maxDepth);
  const radiusBottom = radiusTop + 0.05;

  // Usar el seed para generar números pseudo-aleatorios consistentes
  const random = () => {
    seed = (seed * 16807) % 2147483647;
    return (seed - 1) / 2147483646;
  };

  const numChildren = 2 + Math.floor(random() * 2);
  const childBranches = [];

  for (let i = 0; i < numChildren; i++) {
    const angle = (i / numChildren) * Math.PI * 2 + random() * 0.2;
    const childRotation = [
      -Math.PI / 4 + random() * 0.2,
      angle,
      0,
    ];

    childBranches.push(
      <Branch
        key={i}
        position={[0, length, 0]}
        rotation={childRotation}
        depth={depth + 1}
        maxDepth={maxDepth}
        seed={seed + i}
      />
    );
  }

  return (
    <group position={position} rotation={rotation}>
      <mesh position={[0, length / 2, 0]}>
        <cylinderGeometry args={[radiusTop, radiusBottom, length, 6]} />
        <meshStandardMaterial color="#8B4513" />
      </mesh>
      <group>
        {depth === maxDepth ? (
          <mesh position={[0, length, 0]}>
            <sphereGeometry args={[0.2, 6, 6]} />
            <meshStandardMaterial color="green" />
          </mesh>
        ) : (
          childBranches
        )}
      </group>
    </group>
  );
};

const Controls = ({ maxDepth, setMaxDepth, onRegenerate }) => {
  return (
    <div style={{
      position: 'absolute',
      top: '20px',
      left: '20px',
      background: 'rgba(255, 255, 255, 0.8)',
      padding: '20px',
      borderRadius: '8px',
    }}>
      <div style={{ marginBottom: '10px' }}>
        <label>Profundidad: {maxDepth}</label>
        <input
          type="range"
          min="1"
          max="8"
          value={maxDepth}
          onChange={(e) => setMaxDepth(parseInt(e.target.value))}
          style={{ display: 'block', width: '200px' }}
        />
      </div>
      <button
        onClick={onRegenerate}
        style={{
          padding: '8px 16px',
          background: '#4CAF50',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer',
        }}
      >
        Regenerar Árbol
      </button>
    </div>
  );
};

// Escena principal
const TreeScene = () => {
  const [maxDepth, setMaxDepth] = useState(5);
  const [seed, setSeed] = useState(Math.random() * 1000000);

  const handleRegenerate = () => {
    setSeed(Math.random() * 1000000);
  };

  return (
    <>
      <Canvas id="canvas" camera={{ position: [0, 5, 10], fov: 50 }}>
        <ambientLight intensity={0.5} />
        <directionalLight position={[5, 10, 5]} intensity={1} />
        <Grid
          args={[20, 20]}
          cellSize={1}
          cellThickness={1}
          cellColor="#6f6f6f"
          sectionSize={5}
        />
        <Branch
          position={[0, 0, 0]}
          rotation={[0, 0, 0]}
          depth={0}
          maxDepth={maxDepth}
          seed={seed}
        />
        <OrbitControls />
      </Canvas>
      <Controls
        maxDepth={maxDepth}
        setMaxDepth={setMaxDepth}
        onRegenerate={handleRegenerate}
      />
    </>
  );
};

export default TreeScene;