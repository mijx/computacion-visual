import React, { useState } from 'react'

export default function CameraUI({
  isPerspective,
  setIsPerspective,
  perspFov,
  setPerspFov,
  orthoZoom,
  setOrthoZoom,
}) {
  const [hover, setHover] = useState(false)

  return (
    <div style={styles.uiPanel}>
      <h2 style={{ margin: '0 0 20px 0', lineHeight: 1.3 }}>Control de Cámara</h2>

      <button
        onClick={() => setIsPerspective(!isPerspective)}
        style={{ ...styles.button, ...(hover ? styles.buttonHover : {}) }}
        onMouseEnter={() => setHover(true)}
        onMouseLeave={() => setHover(false)}
      >
        Cambiar a {isPerspective ? 'Ortográfica' : 'Perspectiva'}
      </button>

      {isPerspective ? (
        <>
          <label htmlFor="fovRange" style={styles.label}>
            Campo de visión (FOV): {perspFov}°
          </label>
          <input
            id="fovRange"
            type="range"
            min={10}
            max={90}
            value={perspFov}
            onChange={(e) => setPerspFov(Number(e.target.value))}
            style={styles.slider}
          />
        </>
      ) : (
        <>
          <label htmlFor="orthoZoomRange" style={styles.label}>
            Zoom Ortográfico: {orthoZoom.toFixed(1)}
          </label>
          <input
            id="orthoZoomRange"
            type="range"
            min={1}
            max={10}
            step={0.1}
            value={orthoZoom}
            onChange={(e) => setOrthoZoom(Number(e.target.value))}
            style={styles.slider}
          />
        </>
      )}
    </div>
  )
}

const styles = {
  uiPanel: {
    width: '100%',
    background: 'rgba(25, 25, 25, 0.85)',
    backdropFilter: 'blur(12px)',
    padding: '24px 28px',
    borderRadius: 14,
    color: '#f0f0f0',
    boxShadow: '0 10px 30px rgba(0,0,0,0.5)',
    fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
    userSelect: 'none',
    border: '1.5px solid rgba(255,255,255,0.2)',
  },
  button: {
    width: '100%',
    padding: '14px 0',
    background: '#1e90ff',
    border: 'none',
    borderRadius: 10,
    color: '#fff',
    fontWeight: '700',
    cursor: 'pointer',
    fontSize: 18,
    marginBottom: 22,
    transition: 'background-color 0.3s ease',
    boxShadow: '0 5px 16px rgba(30,144,255,0.55)',
  },
  buttonHover: {
    background: '#1c86ee',
  },
  label: {
    fontSize: 16,
    marginBottom: 16,
    display: 'block',
    fontWeight: '600',
    letterSpacing: '0.02em',
    lineHeight: 1.4,
  },
  slider: {
    width: '100%',
    marginBottom: 28,
    cursor: 'pointer',
    accentColor: '#1e90ff',
    height: 12,
    borderRadius: 8,
  },
}
