# 🧪 Taller Colisiones y Partículas: Reacciones Visuales Interactivas en Three.js

## 📅 Fecha
`2025-05-26` – Fecha de entrega

---

## 🎯 Objetivo del Taller

Implementar escenas interactivas donde los objetos reaccionan visualmente al colisionar, mediante sistemas de partículas y uso de colisiones físicas o detección de contacto. El objetivo es entender cómo conectar eventos de colisión con respuestas visuales.

---

## 🧠 Conceptos Aprendidos

Lista los principales conceptos aplicados:

- [x] Integración de físicas en Three.js con `@react-three/cannon`
- [x] Creación de geometrías dinámicas en `@react-three/fiber`
- [x] Detección de colisiones y ejecución de reacciones visuales
- [x] Uso de hooks para manejo de estado visual
- [x] Iluminación y sombras en escenas 3D interactivas

---

## 🔧 Herramientas y Entornos

- React + Vite
- @react-three/fiber
- @react-three/cannon
- @react-three/drei
- three.js
- Visual Studio Code

---

## 📁 Estructura del Proyecto

```
2025-05-26_taller_colisiones_y_particulas/
├── threejs/               # Código fuente en React Three Fiber
├── resultado/
├── README.md
```

---

## 🧪 Implementación

### 🔹 Etapas realizadas
1. Inicialización del proyecto con Vite y React.
2. Instalación de librerías: `@react-three/fiber`, `@react-three/cannon`, `@react-three/drei`, `three`.
3. Creación de una escena con un plano como suelo.
4. Implementación de 5 esferas con físicas y rebote al colisionar.

### 🔹 Código relevante

```jsx
function Ball({ position }) {
  const [color, setColor] = useState('white')
  const [ref] = useSphere(() => ({
    mass: 1,
    position,
    args: [0.5],
    material: { restitution: 0.8 },
    onCollide: () => setColor('hotpink')
  }))
  return (
    <mesh ref={ref} castShadow>
      <sphereGeometry args={[0.5, 32, 32]} />
      <meshStandardMaterial color={color} />
    </mesh>
  )
}
```

---

## 📊 Resultados Visuales

Al ejecutar el proyecto, se observa cómo cinco esferas caen desde una altura, y rebotan de forma realista entre sí y con el suelo cuando colisionan.

![resultado.gif](resultados/demo_colision.gif)

---

## 🧩 Prompts Usados

```text
"¿Cómo lograr que las 5 bolas caigan en el mismo lugar y colisionen entre sí?"
"¿Teniendo ya la física de gravedad, cómo lograr que las pelotas reboten?"
```

---

## 💬 Reflexión Final

Este taller permitió aplicar de manera práctica conceptos de físicas y visualización interactiva en Three.js con React. La implementación de colisiones realistas con respuestas visuales fue especialmente útil para entender cómo conectar eventos físicos con animaciones o cambios visuales usando hooks en React.

Lo más interesante fue ver cómo una pequeña escena cobra vida al integrar iluminación, físicas y reacciones visuales. Para futuros proyectos, me gustaría explorar eventos más complejos como múltiples colisiones en cadena o efectos de sonido.

---

## ✅ Checklist de Entrega

- [x] Carpeta `2025-05-26_taller_colisiones_y_particulas`
- [x] Código limpio y funcional
- [x] GIF incluido con nombre descriptivo
- [x] README completo y claro
- [x] Commits descriptivos en inglés

---
