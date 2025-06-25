import React, { useRef, useState, useMemo, useEffect, useCallback } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Plane, Sphere, Line } from '@react-three/drei';
import { useControls, Leva } from 'leva';
import * as THREE from 'three';

// Componente para un segmento del brazo
function Segment({ position, children, length = 1, color = 'hotpink', onRef }) {
  const groupRef = useRef();

  useEffect(() => {
    if (groupRef.current && onRef) {
      onRef(groupRef.current);
    }
  }, [onRef]);

  return (
    <group ref={groupRef} position={position}>
      <mesh position={[0, 0, 0]}>
        <sphereGeometry args={[0.15, 16, 16]} />
        <meshStandardMaterial color="gray" />
      </mesh>
      <mesh position={[0, length / 2, 0]}>
        <boxGeometry args={[0.2, length, 0.2]} />
        <meshStandardMaterial color={color} />
      </mesh>
      <group position={[0, length, 0]}>{children}</group>
    </group>
  );
}

// Solver CCD (Cyclic Coordinate Descent) para cinemática inversa
const solveIK_CCD = (segments, target, iterations = 50, tolerance = 0.01) => {
  if (!segments || segments.length === 0) return;

  const effectorWorldPos = new THREE.Vector3();
  const targetWorldPos = new THREE.Vector3();

  target.getWorldPosition(targetWorldPos);

  for (let i = 0; i < iterations; i++) {
    segments[segments.length - 1].getWorldPosition(effectorWorldPos);

    if (effectorWorldPos.distanceTo(targetWorldPos) < tolerance) {
      break;
    }

    for (let j = segments.length - 2; j >= 0; j--) {
      const segment = segments[j];
      if (!segment) continue;

      const jointWorldPos = new THREE.Vector3();
      segment.getWorldPosition(jointWorldPos);

      segments[segments.length - 1].getWorldPosition(effectorWorldPos);
      target.getWorldPosition(targetWorldPos);

      const toEffector = effectorWorldPos.clone().sub(jointWorldPos).normalize();
      const toTarget = targetWorldPos.clone().sub(jointWorldPos).normalize();

      const axis = new THREE.Vector3().crossVectors(toEffector, toTarget).normalize();
      const angle = Math.acos(toEffector.dot(toTarget));

      if (isNaN(angle) || angle < 0.001) continue;

      const rotationQuaternion = new THREE.Quaternion().setFromAxisAngle(axis, angle);
      segment.quaternion.premultiply(rotationQuaternion);
      segment.updateMatrixWorld(true);
    }
  }
};

// Escena principal del brazo robótico con Cinemática Inversa
// Ahora recibe targetPosition como un único objeto prop
function ArmIKScene({ targetPosition }) {
  const { numSegments, segmentLength, showTargetLine } = useControls({
    numSegments: { value: 3, min: 1, max: 10, step: 1, label: 'Número de Segmentos' },
    segmentLength: { value: 2, min: 0.5, max: 5, step: 0.1, label: 'Longitud del Segmento' },
    showTargetLine: { value: true, label: 'Mostrar Línea al Objetivo' },
  });

  const armRef = useRef();
  const targetRef = useRef();

  const segmentRefs = useMemo(() => Array(numSegments).fill(null), [numSegments]);

  const setSegmentRef = useCallback((index, element) => {
    if (element) {
      segmentRefs[index] = element;
    }
  }, [segmentRefs]);

  const generateSegments = (count, length, currentDepth = 0) => {
    if (currentDepth >= count) {
      return null;
    }
    const colorIndex = currentDepth % segmentColors.length;
    return (
      <Segment
        key={currentDepth}
        length={length}
        position={[0, 0, 0]}
        color={segmentColors[colorIndex]}
        onRef={(el) => setSegmentRef(currentDepth, el)}
      >
        {generateSegments(count, length, currentDepth + 1)}
      </Segment>
    );
  };

  const segmentColors = useMemo(() => ['#826Aed', '#A79CFF', '#D2CBFF', '#FFD700', '#FFA500'], []);

  useFrame(() => {
    if (armRef.current && targetRef.current && segmentRefs.every(ref => ref !== null)) {
      // Usar el objeto targetPosition para actualizar la posición de la esfera
      targetRef.current.position.set(targetPosition.x, targetPosition.y, targetPosition.z);
      // console.log('ArmIKScene - Target Position in useFrame:', targetPosition.x, targetPosition.y, targetPosition.z); // DEBUG: Rastrea la posición en la escena

      solveIK_CCD(segmentRefs, targetRef.current);
    }
  });


  return (
    <>
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} />

      <Plane args={[20, 20]} rotation-x={-Math.PI / 2} position={[0, -0.01, 0]}>
        <meshStandardMaterial color="#333" />
      </Plane>

      {/* Esfera objetivo controlada por inputs manuales */}
      {/* La posición se establece aquí usando el objeto targetPosition */}
      <Sphere ref={targetRef} args={[0.3, 32, 32]} position={[targetPosition.x, targetPosition.y, targetPosition.z]}>
        <meshStandardMaterial color="red" />
      </Sphere>

      <mesh position={[0, 0.05, 0]}>
        <boxGeometry args={[0.5, 0.1, 0.5]} />
        <meshStandardMaterial color="gray" />
      </mesh>

      <group ref={armRef} position={[0, 0.1, 0]}>
        {generateSegments(numSegments, segmentLength)}
      </group>

      {/* Línea desde la base del brazo al objetivo para visualización */}
      {showTargetLine && (
        <Line
          points={[new THREE.Vector3(0, 0.1, 0), new THREE.Vector3(targetPosition.x, targetPosition.y, targetPosition.z)]}
          color="blue"
          lineWidth={2}
        />
      )}

      <OrbitControls />
    </>
  );
}

// Componente principal de la aplicación
export default function App() {
  // Ahora el estado de la posición del objetivo es un solo objeto
  const [targetPosition, setTargetPosition] = useState({ x: 3, y: 3, z: 3 });

  const handleTargetChange = (axis, value) => {
    const numValue = parseFloat(value);
    if (!isNaN(numValue)) {
      setTargetPosition(prev => {
        const newPos = { ...prev, [axis]: numValue };
        // console.log('App - New Target Position:', newPos); // DEBUG: Rastrea la nueva posición en la App
        return newPos;
      });
    }
  };

  return (
    <>
      <Leva collapsed />

      {/* Controles de posición del objetivo en pantalla */}
      <div style={{
        position: 'absolute',
        top: '10px',
        right: '10px',
        background: 'rgba(0,0,0,0.7)',
        padding: '10px',
        borderRadius: '8px',
        color: 'white',
        fontFamily: 'sans-serif',
        display: 'flex',
        flexDirection: 'column',
        gap: '8px',
        zIndex: 1000
      }}>
        <h3 style={{ margin: '0 0 5px 0', color: '#FFF' }}>Posición del Objetivo</h3>
        <label style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          X:
          <input
            type="number"
            value={targetPosition.x} // <-- Usa targetPosition.x
            onChange={(e) => handleTargetChange('x', e.target.value)}
            step="0.1"
            style={{ width: '80px', padding: '4px', borderRadius: '4px', border: 'none' }}
          />
        </label>
        <label style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          Y:
          <input
            type="number"
            value={targetPosition.y} // <-- Usa targetPosition.y
            onChange={(e) => handleTargetChange('y', e.target.value)}
            step="0.1"
            style={{ width: '80px', padding: '4px', borderRadius: '4px', border: 'none' }}
          />
        </label>
        <label style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          Z:
          <input
            type="number"
            value={targetPosition.z} // <-- Usa targetPosition.z
            onChange={(e) => handleTargetChange('z', e.target.value)}
            step="0.1"
            style={{ width: '80px', padding: '4px', borderRadius: '4px', border: 'none' }}
          />
        </label>
      </div>

      <Canvas camera={{ position: [8, 8, 8], fov: 75 }} style={{ width: '100vw', height: '100vh' }}>
        <color attach="background" args={['#222']} />
        {/* Pasa el objeto targetPosition completo */}
        <ArmIKScene targetPosition={targetPosition} />
      </Canvas>
    </>
  );
}
