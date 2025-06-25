import React, { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Line, Sphere, Box } from '@react-three/drei';
import { Vector3, Quaternion, MathUtils, CatmullRomCurve3 } from 'three';
import { useControls } from 'leva';

/**
 * Componente para el objeto 3D animado que utiliza LERP y SLERP.
 * Se encarga de la interpolación de posición y rotación.
 */
function AnimatedObject({ startPosition, endPosition, startRotation, endRotation, t, interpolationType }) {
  const meshRef = useRef<THREE.Mesh>(null); // Referencia al mesh del objeto 3D

  // Vector de posición inicial y final para LERP (interpolación lineal)
  const p1 = new Vector3(...startPosition);
  const p2 = new Vector3(...endPosition);

  // Cuaterniones de rotación inicial y final para SLERP (interpolación esférica lineal)
  // Un cuaternión representa rotaciones de manera más robusta que los ángulos de Euler
  // para evitar el problema de "Gimbal Lock".
  const q1 = new Quaternion().setFromEuler(startRotation);
  const q2 = new Quaternion().setFromEuler(endRotation);

  // Hook useFrame se ejecuta en cada fotograma de la animación
  useFrame(() => {
    if (meshRef.current) {
      if (interpolationType === 'lerp') {
        // LERP: Interpolación lineal para la posición
        // El objeto se mueve en línea recta entre p1 y p2.
        meshRef.current.position.lerpVectors(p1, p2, t);

        // Para la rotación con LERP, interpolamos los ángulos de Euler directamente.
        // Esto puede causar movimientos no naturales o "Gimbal Lock" en ciertos casos.
        meshRef.current.rotation.x = MathUtils.lerp(startRotation.x, endRotation.x, t);
        meshRef.current.rotation.y = MathUtils.lerp(startRotation.y, endRotation.y, t);
        meshRef.current.rotation.z = MathUtils.lerp(startRotation.z, endRotation.z, t);
      } else if (interpolationType === 'slerp-position') {
        // En este modo, la posición sigue usando LERP (Vector3.lerpVectors),
        // ya que SLERP es específicamente para rotaciones.
        meshRef.current.position.lerpVectors(p1, p2, t);

        // SLERP: Interpolación esférica lineal para la rotación
        // Proporciona una interpolación de rotación más suave y predecible.
        meshRef.current.quaternion.slerpQuaternions(q1, q2, t);
      }
    }
  });

  return (
    <Box ref={meshRef} args={[0.5, 0.5, 0.5]}>
      <meshStandardMaterial color="hotpink" />
    </Box>
  );
}

/**
 * Componente que dibuja una curva Bézier (usando CatmullRomCurve3 como aproximación)
 * y un objeto que se mueve a lo largo de esta curva.
 */
function BezierPathAndObject({ startPoint, controlPoint1, controlPoint2, endPoint, t }) {
  const animatedObjectRef = useRef<THREE.Mesh>(null); // Referencia al objeto que se mueve en la curva

  // Define una curva Catmull-Rom. Aunque no es una Bézier cúbica pura,
  // CatmullRomCurve3 es útil para crear curvas suaves que pasan por puntos dados,
  // lo cual visualmente simula el concepto de una trayectoria curva para este taller.
  // Para una Bézier cúbica estricta, se debería implementar la fórmula de Bézier
  // P(t) = (1-t)^3*P0 + 3(1-t)^2*t*P1 + 3(1-t)*t^2*P2 + t^3*P3
  const curve = new CatmullRomCurve3([
    startPoint,
    controlPoint1,
    controlPoint2,
    endPoint,
  ]);

  // Hook useFrame para actualizar la posición del objeto en cada fotograma
  useFrame(() => {
    if (animatedObjectRef.current) {
      // Obtiene el punto en la curva correspondiente al valor 't'
      const point = curve.getPointAt(t);
      // Asigna la posición calculada al objeto
      animatedObjectRef.current.position.copy(point);
    }
  });

  return (
    <>
      {/* Dibuja la línea que representa la curva */}
      <Line
        points={curve.getPoints(50).map((p) => [p.x, p.y, p.z])} // Genera 50 puntos a lo largo de la curva para dibujarla
        color="purple"
        lineWidth={2}
      />

      {/* Objeto animado que se mueve a lo largo de la curva */}
      <Sphere ref={animatedObjectRef} args={[0.15, 16, 16]}>
        <meshStandardMaterial color="orange" />
      </Sphere>
    </>
  );
}

/**
 * Componente principal de la aplicación.
 * Configura la escena 3D y los controles de interpolación.
 */
function App() {
  // Puntos de inicio y fin para las trayectorias de interpolación
  const startPos: [number, number, number] = [-2, 0, 0];
  const endPos: [number, number, number] = [2, 0, 0];

  // Rotaciones de inicio y fin para el objeto animado (en radianes Euler X, Y, Z)
  const startRot = new Vector3(0, 0, 0); // Sin rotación
  const endRot = new Vector3(0, Math.PI, 0); // Rotación de 180 grados (PI radianes) alrededor del eje Y

  // Puntos de control para la curva Bézier (afectan la forma de la curva)
  const controlPoint1: [number, number, number] = [0, 2, -1];
  const controlPoint2: [number, number, number] = [0, -2, 1];

  // Configuración de la interfaz de usuario con Leva para controlar la animación
  const { interpolationType, t } = useControls({
    interpolationType: {
      value: 'lerp', // Valor inicial
      options: ['lerp', 'slerp-position', 'bezier'], // Opciones disponibles
      label: 'Tipo de Interpolación',
    },
    t: { value: 0, min: 0, max: 1, step: 0.01, label: 'Progreso (t)' }, // Control para el progreso de la animación
  });

  return (
    <div style={{ height: '100vh', width: '100vw', background: '#222' }}>
    <Canvas camera={{ position: [0, 5, 5], fov: 60 }}>
      {/* Luces de la escena */}
      <ambientLight intensity={0.5} /> {/* Luz ambiental que ilumina uniformemente */}
      <pointLight position={[10, 10, 10]} /> {/* Luz puntual desde una posición específica */}

      {/* Esfera de inicio (visualización del punto de partida) */}
      <Sphere position={startPos} args={[0.1, 16, 16]}>
        <meshBasicMaterial color="green" />
      </Sphere>

      {/* Esfera de fin (visualización del punto de llegada) */}
      <Sphere position={endPos} args={[0.1, 16, 16]}>
        <meshBasicMaterial color="red" />
      </Sphere>

      {/* Renderizado condicional del objeto animado o la curva Bézier */}
      {interpolationType !== 'bezier' ? (
        // Si no es Bézier, renderiza el objeto que usa LERP/SLERP
        <AnimatedObject
          startPosition={startPos}
          endPosition={endPos}
          startRotation={startRot}
          endRotation={endRot}
          t={t}
          interpolationType={interpolationType}
        />
      ) : (
        // Si es Bézier, renderiza la curva y el objeto que la sigue
        <>
          <BezierPathAndObject
            startPoint={new Vector3(...startPos)}
            controlPoint1={new Vector3(...controlPoint1)}
            controlPoint2={new Vector3(...controlPoint2)}
            endPoint={new Vector3(...endPos)}
            t={t}
          />
          {/* Esferas para visualizar los puntos de control de la curva Bézier */}
          <Sphere position={controlPoint1} args={[0.08, 16, 16]}>
            <meshBasicMaterial color="blue" />
          </Sphere>
          <Sphere position={controlPoint2} args={[0.08, 16, 16]}>
            <meshBasicMaterial color="blue" />
          </Sphere>
        </>
      )}

      {/* OrbitControls permite interactuar con la cámara para rotar, hacer zoom, etc. */}
      <OrbitControls />
    </Canvas>
    </div>
  );
}

export default App;
