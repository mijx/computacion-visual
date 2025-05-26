// main.jsx: Punto de entrada principal de la aplicación React.
import React from 'react'
import ReactDOM from 'react-dom/client'
import { Canvas } from '@react-three/fiber'
import App from './App' // Asegúrate de que este archivo App.jsx exista y contenga tus componentes 3D.
import './index.css' // ¡IMPORTANTE! Importa tu archivo CSS aquí. Asegúrate de que la ruta sea correcta.

// Renderiza la aplicación React en el elemento con id 'root'.
ReactDOM.createRoot(document.getElementById('root')).render(
  // Canvas de @react-three/fiber para renderizar escenas 3D.
  <Canvas shadows camera={{ position: [0, 6, 15], fov: 50 }}>
    {/* Componente principal de tu aplicación 3D */}
    <App />
  </Canvas>
)
