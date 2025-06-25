import React, { useRef, useState, useEffect } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import * as THREE from 'three';


function Box() {
 const meshRef = useRef();
 const [data, setData] = useState({ x: 0, y: 0, color: 'red' });


 useEffect(() => {
 const socket = new WebSocket("ws://localhost:8765");


 socket.onopen = () => {
 console.log("Conectado al servidor WebSocket.");
 };


 socket.onmessage = (event) => {
 const receivedData = JSON.parse(event.data);
 console.log("Datos recibidos:", receivedData);
 setData(receivedData);
 };


 socket.onclose = () => {
 console.log("Desconectado del servidor WebSocket.");
 };


 socket.onerror = (error) => {
 console.error("Error en WebSocket:", error);
 };


 return () => {
 socket.close();
 };
 }, []);


 useFrame(() => {
 if (meshRef.current) {
 meshRef.current.position.x = data.x;
 meshRef.current.position.y = data.y;


 let newColor = new THREE.Color(data.color);
 if (meshRef.current.material) {
 meshRef.current.material.color.set(newColor);
 }
 }
 });


 return (
 <mesh ref={meshRef}>
 <boxGeometry args={[1, 1, 1]} />
 <meshStandardMaterial color={data.color} />
 </mesh>
 );
}


function App() {
 return (
 <div style={{ width: '100vw', height: '100vh' }}>
 <Canvas camera={{ position: [0, 0, 5] }}> {/* Cámara un poco más cerca */}
 <ambientLight intensity={0.5} />
 <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} />
 <pointLight position={[-10, -10, -10]} />
 <Box />
 <OrbitControls />
 </Canvas>
 </div>
 );
}


export default App;