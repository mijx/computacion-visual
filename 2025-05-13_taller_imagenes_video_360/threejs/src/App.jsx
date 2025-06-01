import React, { useState } from 'react'
import { Canvas } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'
import Panorama from './components/Panorama'
import Video360 from './components/Video360'

export default function App() {
  const [showVideo, setShowVideo] = useState(false)

  return (
    <>
      <Canvas camera={{ position: [0, 0, 0.1], fov: 75 }} style={{ height: '100vh', width: '100vw' }}>
        {showVideo ? <Video360 /> : <Panorama />}
        <OrbitControls enableZoom={false} />
      </Canvas>

      <div style={styles.controlsContainer}>
        <button
          onClick={() => setShowVideo(false)}
          style={{
            ...styles.button,
            backgroundColor: !showVideo ? '#1e88e5' : 'rgba(30, 136, 229, 0.5)',
            boxShadow: !showVideo ? '0 5px 15px rgba(30,136,229,0.6)' : 'none',
          }}
          onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#1565c0'}
          onMouseLeave={(e) => e.currentTarget.style.backgroundColor = !showVideo ? '#1e88e5' : 'rgba(30, 136, 229, 0.5)'}
        >
          Imagen 360°
        </button>
        <button
          onClick={() => setShowVideo(true)}
          style={{
            ...styles.button,
            backgroundColor: showVideo ? '#1e88e5' : 'rgba(30, 136, 229, 0.5)',
            boxShadow: showVideo ? '0 5px 15px rgba(30,136,229,0.6)' : 'none',
          }}
          onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#1565c0'}
          onMouseLeave={(e) => e.currentTarget.style.backgroundColor = showVideo ? '#1e88e5' : 'rgba(30, 136, 229, 0.5)'}
        >
          Video 360°
        </button>
      </div>
    </>
  )
}

const styles = {
  controlsContainer: {
    position: 'fixed',
    top: 20,
    left: '50%',
    transform: 'translateX(-50%)',
    display: 'flex',
    gap: 15,
    padding: 10,
    backgroundColor: 'rgba(20,20,20,0.7)',
    borderRadius: 12,
    boxShadow: '0 4px 20px rgba(0,0,0,0.5)',
    zIndex: 1000,
  },
  button: {
    cursor: 'pointer',
    border: 'none',
    padding: '12px 26px',
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
    borderRadius: 8,
    transition: 'background-color 0.3s ease, box-shadow 0.3s ease',
    userSelect: 'none',
  },
}
