import { Canvas } from '@react-three/fiber'
import { useControls, Leva } from 'leva'
import { OrbitControls, Grid, Html, Stats } from '@react-three/drei'
import * as THREE from 'three'
import './App.css'

function MetalCube({ color = "red", position = [0, 0, 0], scale = [1, 1, 1] }) {
  return (
    <mesh position={position} scale={scale} castShadow>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial 
        color={color} 
        metalness={0.8} 
        roughness={0.2} 
      />
    </mesh>
  );
}

function MetalCubeScene({ isPerspective, cameraConfig }) {
  return (
      <Canvas
      shadows
      key={isPerspective ? 'perspective' : 'orthographic'} // Force re-render on camera type change
      orthographic={!isPerspective}
      camera={{
        ...cameraConfig,
        // Explicitly tell R3F which type of camera to create
        // This is crucial for the orthographic prop to work correctly with initial camera settings
        makeDefault: true, // Ensure this camera is the default
      }}
      style={{ backgroundColor: '#1a1a1a' }}
    >
      <ambientLight intensity={0.6} />
      <directionalLight
        castShadow
        position={[10, 15, 10]}
        intensity={1.5}
        shadow-mapSize-width={2048}
        shadow-mapSize-height={2048}
        shadow-camera-far={50}
        shadow-camera-left={-10}
        shadow-camera-right={10}
        shadow-camera-top={10}
        shadow-camera-bottom={-10}
      />

      <MetalCube color="#ff4136" position={[-2, 0.5, 0]} />
      <MetalCube color="#0074d9" position={[0, 0.5, -2]} scale={[0.8, 0.8, 0.8]} />
      <MetalCube color="#2ecc40" position={[2, 0.5, 0]} />
      <MetalCube color="#ffdc00" position={[0, 0.5, 2]} scale={[1.2, 1.2, 1.2]} />

      <Grid
        receiveShadow
        args={[30, 30]}
        position={[0, -0.01, 0]} // Slightly below cubes to avoid z-fighting
        cellSize={0.5}
        cellThickness={1}
        cellColor={new THREE.Color('#6f6f6f')}
        sectionSize={2.5}
        sectionThickness={1.5}
        sectionColor={new THREE.Color('#444444')}
        fadeDistance={35}
        fadeStrength={1}
        infiniteGrid
      />

      <OrbitControls makeDefault />
      <CameraViewHUD isPerspective={isPerspective} />
    </Canvas>
  );
}

function CameraViewHUD({ isPerspective }) {
  return (
    <Html>
      <div className="hud-text">
        {isPerspective ? 'Perspective View' : 'Orthographic View'}
      </div>
    </Html>
  );
}

function App() {
  const { isPerspective } = useControls({
    isPerspective: {
      value: true,
      label: 'Toggle Camera',
    },
  });

  const cameraConfig = isPerspective
    ? { // Perspective Camera Configuration
        fov: 75,
        position: [5, 4, 5],
        near: 0.1,
        far: 1000,
      }
    : { // Orthographic Camera Configuration
        left: -5,
        right: 5,
        top: 5,
        bottom: -5,
        position: [5, 4, 5],
        zoom: 1,
        near: 0.1,
        far: 1000,
      };

  return (
    <div id="canvas-container">
      <Leva />
      <MetalCubeScene isPerspective={isPerspective} cameraConfig={cameraConfig} />
    </div>
  );
}

export default App
