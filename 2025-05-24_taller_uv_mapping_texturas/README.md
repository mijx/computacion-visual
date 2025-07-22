# 🧪 Taller - UV Mapping: Texturas que Encajan

## 🗓️ Fecha

2025-05-24

---

## 🎯 Objetivo del Taller

Explorar el mapeo UV como técnica fundamental para aplicar correctamente texturas 2D sobre modelos 3D sin distorsión. El objetivo es entender cómo se proyectan las texturas y cómo se pueden ajustar las coordenadas UV para mejorar el resultado visual.

---

## 🧠 Conceptos Aprendidos

* Qué son las coordenadas UV y su relación con las texturas.
* Cómo aplicar texturas en React Three Fiber usando `useGLTF`, `useTexture` y `MeshStandardMaterial`.
* Modificación de `repeat`, `offset`, `wrapS`, `wrapT` para mejorar la proyección.
* Uso de cuadrículas de prueba para evidenciar distorsiones.

---

## 🔧 Herramientas y Entornos

* React Three Fiber (Three.js en React).
* Leva para controles interactivos.
* Modelos 3D `.glb` y texturas `.png`.

---

## 📁 Estructura del Proyecto

```
2025-05-24_taller_mapping_texturas_uv/
├── public/
│   ├── models/
│   │   └── piedra.glb
│   └── textures/
│       └── uv_grid.png
├── src/
│   └── App.jsx
├── resultados/
│   └── resultado.gif
└── README.md
```

---

## 💡 Implementación en React Three Fiber

### 🔹 Carga de Modelo y Textura UV

```jsx
const { scene } = useGLTF(url);
const texture = useTexture('/textures/uv_grid.png');
```

Se carga un modelo `.glb` y una textura tipo cuadrícula que permite evidenciar distorsiones.

### 🛠️ Controles Interactivos con Leva

```jsx
const { repeatX, repeatY, offsetX, offsetY, wrapS, wrapT } = useControls('UV Params', {...})
```

Permiten modificar en tiempo real los valores UV de la textura:

* **repeat**: cantidad de veces que se repite la textura.
* **offset**: desplazamiento horizontal y vertical de la textura.
* **wrapS / wrapT**: comportamiento del borde (Repeat, Clamp, Mirror).

### ⚙️ Configuración de la Textura UV

```jsx
useMemo(() => {
  texture.wrapS = wrapS;
  texture.wrapT = wrapT;
  texture.repeat.set(repeatX, repeatY);
  texture.offset.set(offsetX, offsetY);
  texture.needsUpdate = true;
}, [texture, repeatX, repeatY, offsetX, offsetY, wrapS, wrapT]);
```

Optimiza el renderizado evitando recargas innecesarias y aplicando los parámetros elegidos.

### 🧱 Aplicación de Textura al Modelo

```jsx
scene.traverse((child) => {
  if (child.isMesh) {
    child.material.map = texture;
    child.material.needsUpdate = true;
  }
});
```

Cada `mesh` del modelo recibe la textura con las coordenadas UV ajustadas.

---

## 📈 Resultados Visuales

* Vista interactiva del modelo con textura cuadrícula:

![resultado.gif](resultados/resultado.gif)

---

## 🔎 Prompts Utilizados

* "Como plicar textura a modelo GLTF usando useGLTF y useTexture"
* "Modificar coordenadas UV de textura en Three.js"
* "wrapS vs wrapT en textura Three.js"
* "Cómo evitar distorsiones de textura en objetos 3D"
* "Cuadrícula UV para verificar mapeo"
* "Aplicar misma textura a todos los mesh del modelo"

---

## 💬 Reflexión Final

Este taller ayudó a comprender la importancia de las coordenadas UV al aplicar texturas. Aprendimos a visualizar errores comunes mediante cuadrículas y a corregirlos modificando los parámetros `repeat`, `offset` y `wrap`. El reto principal fue aplicar la textura a todos los `mesh` dentro del modelo cargado y garantizar que los cambios se reflejen en tiempo real. El uso de `Leva` fue clave para experimentar rápidamente con configuraciones y observar los efectos de manera visual e inmediata.

---
