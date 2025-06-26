import { useState, useEffect, useRef } from 'react'
import './App.css'
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls, Grid } from '@react-three/drei'
import WebSocketManager from './utils/WebSocketManager'
import * as THREE from 'three'

// Componente de la esfera animada
function AnimatedSphere({ peopleCount }) {
  // Referencias para las propiedades animadas
  const materialRef = useRef()
  const scaleRef = useRef(1)
  const colorRef = useRef(new THREE.Color('#ADD8E6'))
  const targetScale = 1 + (peopleCount * 0.2)
  
  // Colores para la interpolación
  const baseColor = new THREE.Color('#ADD8E6')  // Azul pálido
  const maxColor = new THREE.Color('#0066FF')   // Azul intenso
  
  // Calcular color objetivo basado en la cantidad de personas
  const targetColor = new THREE.Color().lerpColors(
    baseColor,
    maxColor,
    Math.min(peopleCount / 10, 1) // Máximo efecto a las 10 personas
  )

  // Animación suave en cada frame
  useFrame(() => {
    // Interpolar escala
    scaleRef.current = THREE.MathUtils.lerp(
      scaleRef.current,
      targetScale,
      0.05
    )

    // Interpolar color
    colorRef.current.lerp(targetColor, 0.05)

    // Actualizar material
    if (materialRef.current) {
      materialRef.current.color = colorRef.current
      materialRef.current.emissive = colorRef.current
      materialRef.current.emissiveIntensity = Math.min(peopleCount / 10, 1) * 0.5
    }
  })

  return (
    <mesh scale={scaleRef.current}>
      <sphereGeometry args={[0.25, 32, 32]} />
      <meshStandardMaterial
        ref={materialRef}
        metalness={0.1}
        roughness={0.3}
      />
    </mesh>
  )
}

function App() {
  const [peopleCount, setPeopleCount] = useState(0);
  const [isConnected, setIsConnected] = useState(false);
  const wsManagerRef = useRef(null);

  useEffect(() => {
    // Crear instancia de WebSocketManager
    wsManagerRef.current = new WebSocketManager();

    // Configurar callbacks
    wsManagerRef.current.onPeopleCount((count) => {
      setPeopleCount(count);
    });

    wsManagerRef.current.onConnectionChange((connected) => {
      setIsConnected(connected);
      // Si nos desconectamos, resetear el contador de personas
      if (!connected) {
        setPeopleCount(0);
      }
    });

    // Limpiar al desmontar
    return () => {
      if (wsManagerRef.current) {
        wsManagerRef.current.disconnect();
        wsManagerRef.current = null;
      }
    };
  }, []);

  const handleConnectionToggle = () => {
    if (!wsManagerRef.current) return;

    if (isConnected) {
      wsManagerRef.current.disconnect();
    } else {
      wsManagerRef.current.connect();
    }
  };

  return (
    <>
      <div id="canvas-container">
        {/* Panel de estado centrado */}
        <div style={{
          position: 'absolute',
          top: '20px',
          left: '50%',
          transform: 'translateX(-50%)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: '10px',
          zIndex: 1000
        }}>
          {/* Estado de conexión */}
          <div style={{
            padding: '8px 15px',
            backgroundColor: isConnected ? '#4CAF50' : '#f44336',
            color: 'white',
            borderRadius: '5px',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            fontSize: '14px'
          }}>
            {/* Indicador de estado */}
            <div style={{
              width: '8px',
              height: '8px',
              backgroundColor: 'white',
              borderRadius: '50%',
              opacity: isConnected ? '1' : '0.6'
            }}/>
            {isConnected ? 'Conectado' : 'Desconectado'}
          </div>

          {/* Contador de personas */}
          <div style={{
            padding: '8px 15px',
            backgroundColor: 'rgba(0,0,0,0.7)',
            color: 'white',
            borderRadius: '5px',
            fontSize: '14px'
          }}>
            Personas detectadas: {peopleCount}
          </div>

          {/* Botón de conexión/reconexión */}
          <button 
            onClick={handleConnectionToggle}
            style={{
              padding: '8px 15px',
              backgroundColor: '#2196F3',
              color: 'white',
              border: 'none',
              borderRadius: '5px',
              cursor: 'pointer',
              fontSize: '14px',
              transition: 'all 0.3s ease',
              ':hover': {
                backgroundColor: '#1976D2'
              }
            }}
          >
            {isConnected ? 'Desconectar' : 'Conectar'}
          </button>
        </div>

        <Canvas camera={{ position: [5, 5, 5], fov: 60 }}>
          {/* Iluminación profesional */}
          <ambientLight intensity={Math.PI / 2} />
          <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} decay={0} intensity={Math.PI} />
          <pointLight position={[-10, -10, -10]} decay={0} intensity={Math.PI} />
          
          {/* Esfera animada */}
          <AnimatedSphere peopleCount={peopleCount} />
          
          {/* Controles y Grid */}
          <OrbitControls 
            makeDefault
            enableDamping
            dampingFactor={0.05}
            minDistance={2}
            maxDistance={20}
            autoRotate
            autoRotateSpeed={0.8}
          />
          <Grid 
            infiniteGrid 
            cellSize={1}
            sectionSize={10}
            sectionColor={"#6f6f6f"}
            cellColor={"#a5a5a5"}
            fadeDistance={40}
          />
        </Canvas>
      </div>
    </>
  )
}

export default App
