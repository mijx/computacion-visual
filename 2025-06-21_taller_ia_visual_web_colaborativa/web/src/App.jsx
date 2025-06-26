import { Suspense, useState, useEffect, useMemo } from 'react'
import { Canvas } from '@react-three/fiber'
import { useTexture, OrbitControls, Box, Html, Bounds } from '@react-three/drei'
import './App.css'

function DetectionBox({ detection, scale, imageSize, isSelected, onClick }) {
  const { box, class: className, confidence } = detection;
  const [x, y, w, h] = box;

  // Normalizar coordenadas y dimensiones
  const normX = (x + w / 2) - imageSize.width / 2;
  const normY = -(y + h / 2) + imageSize.height / 2;

  return (
    <group
      position={[normX * scale, normY * scale, 0]}
      onClick={(e) => {
        e.stopPropagation(); // Evita que el click se propague a OrbitControls
        onClick();
      }}
    >
      <Box args={[w * scale, h * scale, 1]}>
        <meshBasicMaterial color={isSelected ? '#ff4081' : 'lime'} wireframe />
      </Box>
      <Html position={[0, (-h / 2) * scale - 0.2, 0]}>
        <div style={{
            color: 'white',
            background: 'rgba(0,0,0,0.7)',
            padding: '4px 8px',
            borderRadius: '4px',
            fontSize: '12px',
            width: 'max-content',
            transform: 'translateX(-50%)',
        }}>
          {className} ({confidence.toFixed(2)})
        </div>
      </Html>
    </group>
  )
}

function Scene({ detections, onSelect, selectedId }) {
  const texture = useTexture('./resultados/deteccion.png');

  const { imageSize, scale, sceneSize } = useMemo(() => {
    const imageSize = { width: texture.image.width, height: texture.image.height };
    const viewportRatio = 15; // Unidades de Three.js para el lado más largo
    const scale = viewportRatio / Math.max(imageSize.width, imageSize.height);
    const sceneSize = { width: imageSize.width * scale, height: imageSize.height * scale };
    return { imageSize, scale, sceneSize };
  }, [texture]);

  return (
    <>
      <ambientLight intensity={2} />
      <OrbitControls makeDefault />

      <Bounds fit clip observe margin={1.4}>
          <group>
            <mesh>
              <planeGeometry args={[sceneSize.width, sceneSize.height]} />
              <meshBasicMaterial map={texture} />
            </mesh>

            {detections.map((detection, index) => (
              <DetectionBox
                key={index}
                detection={detection}
                scale={scale}
                imageSize={imageSize}
                isSelected={selectedId === index}
                onClick={() => onSelect(index)}
              />
            ))}
          </group>
      </Bounds>
    </>
  );
}

function DetectionsPanel({ detections, onSelect, selectedId }) {
    return (
        <div className="panel">
            <h3>Detecciones ({detections.length})</h3>
            <ul className="detection-list">
                {detections.map((det, index) => (
                    <li
                        key={index}
                        className={`detection-item ${selectedId === index ? 'selected' : ''}`}
                        onClick={() => onSelect(index)}
                    >
                        <p><span>{det.class}</span></p>
                        <p>Confianza: {(det.confidence * 100).toFixed(1)}%</p>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default function App() {
  const [detections, setDetections] = useState([]);
  const [selectedId, setSelectedId] = useState(null);

  useEffect(() => {
    fetch('./resultados/results.json')
      .then(res => res.json())
      .then(data => setDetections(data.objects || []))
      .catch(err => console.error("Error cargando detecciones:", err));
  }, []);

  const handleSelect = (id) => {
    setSelectedId(prevId => prevId === id ? null : id); // Clickea de nuevo para deseleccionar
  }

  return (
    <div className="app-container">
        <header className="header">
            <h1>Visor de Detecciones IA</h1>
        </header>
        <main className="main-content">
            <div className="canvas-container">
                <Canvas camera={{ position: [0, 0, 20], fov: 75 }}>
                  <Suspense fallback={<Html center><div style={{color: 'white'}}>Cargando Escena...</div></Html>}>
                    <Scene
                        detections={detections}
                        onSelect={handleSelect}
                        selectedId={selectedId}
                    />
                  </Suspense>
                </Canvas>
            </div>
            <DetectionsPanel
                detections={detections}
                onSelect={handleSelect}
                selectedId={selectedId}
            />
        </main>
    </div>
  )
}
