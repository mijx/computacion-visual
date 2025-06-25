import React, { useRef, useState, useMemo, useEffect, useCallback } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Line } from '@react-three/drei';
import { useControls } from 'leva';
import * as THREE from 'three';


// Array de colores para los segmentos
const segmentColors = ['skyblue', 'lightcoral', 'lightgreen'];


// Componente para un eslabón del brazo
function ArmSegment({ position, rotationOffset, children, name, onUpdateEndEffector, color }) {
 const meshRef = useRef();
 const groupRef = useRef(); // Para la rotación jerárquica
 const [endEffectorPosition, setEndEffectorPosition] = useState(new THREE.Vector3());


 // Sliders para ajustar la rotación de cada eslabón
 const { angle } = useControls(`${name} Rotation`, {
 angle: {
 value: 0,
 min: -Math.PI,
 max: Math.PI,
 step: 0.01,
 },
 });


 useFrame((state, delta) => {
 if (groupRef.current) {
 // Aplica la rotación controlada por el slider
 groupRef.current.rotation.z = angle + rotationOffset;


 // Actualiza la posición global del extremo de este eslabón
 if (onUpdateEndEffector) {
 meshRef.current.getWorldPosition(endEffectorPosition);
 onUpdateEndEffector(endEffectorPosition);
 }
 }
 });


 return (
 <group ref={groupRef} position={position}>
 <mesh ref={meshRef}>
 <boxGeometry args={[1, 0.2, 0.2]} />
 <meshStandardMaterial color={color} />
 </mesh>
 {children}
 </group>
 );
}


// Componente principal del brazo robótico
export default function RobotArm() {
 const [linePoints, setLinePoints] = useState([]);
 const MAX_POINTS = 500; // Número máximo de puntos a almacenar para el trazado
 const canvasRef = useRef();


 // Función para actualizar la posición del efector final y añadirla a los puntos de la línea
 const updateEndEffectorPoints = useCallback((position) => {
 setLinePoints((prevPoints) => {
 const newPoints = [...prevPoints, position.clone()]; // Clona el vector para evitar mutaciones
 if (newPoints.length > MAX_POINTS) {
 newPoints.shift(); // Elimina el punto más antiguo
 }
 return newPoints;
 });
 }, []);


 useEffect(() => {
 // Limpia los puntos al montar o reiniciar
 setLinePoints([]);
 }, []);


 return (
 <div style={{ width: '100vw', height: '100vh' }} ref={canvasRef}>
 <Canvas camera={{ position: [3, 3, 3], fov: 75 }}>
 <ambientLight intensity={0.5} />
 <pointLight position={[10, 10, 10]} />
 <OrbitControls />


 {/* Brazo Robótico */}
 <group position={[0, 0, 0]}>
 {/* Eslabón 1 (base) */}
 <ArmSegment position={[0.5, 0, 0]} rotationOffset={0} name="Segmento 1" color={segmentColors [0]}>
 {/* Eslabón 2 (hijo del eslabón 1) */}
 <ArmSegment position={[0.5, 0, 0]} rotationOffset={0} name="Segmento 2" color={segmentColors [1]}>
 {/* Eslabón 3 (hijo del eslabón 2) - Este es el efector final */}
 <ArmSegment
 position={[0.5, 0, 0]}
 rotationOffset={0}
 name="Segmento 3"
 onUpdateEndEffector={updateEndEffectorPoints}
 color={segmentColors [2]}
 />
 </ArmSegment>
 </ArmSegment>
 </group>


 {/* Línea que traza el movimiento del extremo */}
 {linePoints.length > 1 && (
 <Line
 points={linePoints}
 color="hotpink"
 lineWidth={3}
 transparent
 opacity={0.7}
 />
 )}
 </Canvas>
 </div>
 );
}