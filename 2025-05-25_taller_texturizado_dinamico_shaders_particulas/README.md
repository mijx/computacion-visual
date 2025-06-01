# 🧪 Taller - Texturizado Creativo: Materiales Dinámicos con Shaders y Datos

## 🗓️ Fecha

2025-05-25

---

## 🎯 Objetivo del Taller

Crear materiales que reaccionen en tiempo real a eventos como el paso del tiempo, el hover del usuario o clics. Complementar visualmente el efecto con partículas que simulen fenómenos naturales como energía, fuego o explosiones.

---

## 🧐 Conceptos Aprendidos

* Uso de shaders personalizados (`ShaderMaterial`) con `uniforms` reactivos.
* Creación de efectos visuales a través de `fragmentShader` y `vertexShader`.
* Sistema básico de partículas con `BufferGeometry` y `PointsMaterial`.
* Animación de partículas mediante `useFrame` y `Math`.
* Interacción del usuario: `hover`, `click`, `uTime`.

---

## 🔧 Herramientas y Entornos

* React Three Fiber (Three.js en React).
* Shaders GLSL.
* `@react-three/fiber`, `three`, `react`, `@react-three/drei` (opcional).

---

## 📁 Estructura del Proyecto

```
2025-05-25_taller_texturizado_dinamico_shaders_particulas/
├── public/
├── src/
│   └── App.jsx
├── resultados/
│   └── shader_efecto_y_particulas_interaccion.gif
└── README.md
```

---

## 💡 Implementación Clave en React Three Fiber

### 🔹 Shaders Dinámicos

```js
const vertexShader = `
  varying vec2 vUv;
  void main() {
    vUv = uv;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
  }
`;

const fragmentShader = `
  uniform float uTime;
  uniform float uHover;
  varying vec2 vUv;

  float ripple(vec2 uv, float t) {
    return 0.5 + 0.5 * sin(10.0 * length(uv - 0.5) - t * 4.0);
  }

  void main() {
    float r = ripple(vUv, uTime);
    vec3 base = mix(vec3(0.0, 0.3, 0.0), vec3(0.6, 1.0, 0.3), r);
    float circle = smoothstep(0.5, 0.45, length(vUv - 0.5));
    base *= circle;
    base = mix(base, vec3(0.8, 1.0, 0.5), uHover);
    gl_FragColor = vec4(base, 1.0);
  }
`;
```

* `uTime`: permite animar el efecto de ondas radiales en el tiempo.
* `uHover`: intensifica el color al pasar el mouse por encima del objeto.

### 💪 Sistema de Partículas Interactivo

```js
const positions = new Float32Array(count * 3);
// Aleatoriedad en la generación de posiciones de partículas
positions[i * 3 + 0] = (Math.random() - 0.5) * 0.5;
```

```js
useFrame((state, delta) => {
  uniforms.uTime.value += delta;

  // Oscilación y color animado
  for (let i = 0; i < sizes.length; i++) {
    sizes[i] = 0.02 + Math.sin(uniforms.uTime.value * 2 + i) * 0.02;
    colors[i * 3 + 0] = Math.abs(Math.sin(uniforms.uTime.value + i));
  }

  // Dispersión en clic
  if (explosion) {
    positions[i] += (Math.random() - 0.5) * 0.1;
  }
});
```

---

## 📊 Resultados Visuales

### 🔹 Shader Dinámico e Interacción de Partículas

![shader_efecto_y_particulas_interaccion.gif](resultados/shader_efecto_y_particulas_interaccion.gif)

---

## 🔎 Prompts Utilizados

* "GLSL shader para efecto radiante tipo energía"
* "Three.js sistema de partículas reactivo con puntos"
* "Cómo controlar atributos de geometría buffer con useFrame"
* "click para generar efecto de explosión en partículas"
* "Animar color de puntos en sistema de partículas Three.js"

---

## 💬 Reflexión Final

El efecto más interesante fue el uso del `fragmentShader` para crear una textura animada estilo "energía radioactiva" que responde al paso del tiempo y al `hover`. Fue desafiante integrar esto con partículas controladas manualmente usando `BufferGeometry`, especialmente al sincronizar su color, tamaño y posición en tiempo real. La combinación de interacción (hover y clic) con visuales en GLSL y geometría buffer hizo que el resultado fuera visualmente impactante y didáctico para comprender el potencial de materiales programables.

---
