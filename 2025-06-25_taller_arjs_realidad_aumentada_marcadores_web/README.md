# 🧪 Taller AR Web - Realidad Aumentada con Three.js

## 📅 Fecha
`2025-06-25`

---

## 🎯 Objetivo del Taller

Implementar una experiencia básica de realidad aumentada en el navegador que permita visualizar modelos 3D superpuestos sobre la cámara del dispositivo. Inicialmente se planteó usar marcadores físicos con AR.js, pero debido a limitaciones técnicas se desarrolló una solución híbrida usando Three.js puro y la API nativa de cámara del navegador.

---

## 🧠 Conceptos Aprendidos

Lista los principales conceptos aplicados:

- [x] Transformaciones geométricas (escala, rotación, traslación)
- [x] Renderizado 3D en tiempo real con Three.js
- [x] Acceso a cámara web con WebRTC
- [x] Superposición de capas (video + canvas)
- [x] Carga y visualización de modelos 3D (formato GLB)
- [x] Animaciones suaves con JavaScript
- [x] Otro: **Realidad Aumentada Web sin marcadores**

---

## 🔧 Herramientas y Entornos

Especifica los entornos usados:

- **Three.js** - Librería de renderizado 3D
- **HTML5/CSS3/JavaScript ES6+** - Tecnologías web estándar
- **WebRTC** - API para acceso a cámara
- **GLTFLoader** - Carga de modelos 3D
- **Servidor HTTP/HTTPS** - Para desarrollo local
- **ngrok** - Túnel HTTPS para pruebas locales

📌 **Nota importante**: Requiere HTTPS para acceso a cámara en navegadores modernos


📎 Proyecto desarrollado como taller introductorio de realidad aumentada web

---

## 🧪 Implementación

### 🔹 Etapas realizadas

1. **Intento inicial con AR.js**: Se implementó detección de marcadores Hiro y personalizados, pero se encontraron problemas de compatibilidad y rendimiento.

2. **Transición a Three.js puro**: Debido a conflictos entre A-Frame y Three.js, se migró a una solución híbrida más estable.

3. **Configuración de cámara nativa**: Implementación de acceso directo a la cámara usando WebRTC sin dependencias de AR.js.

4. **Visualización 3D superpuesta**: El modelo 3D se renderiza en un canvas transparente sobre el stream de video de la cámara.

### 🔹 Código relevante

Fragmento clave que muestra la configuración híbrida:

```javascript
// Configuración de cámara nativa
const stream = await navigator.mediaDevices.getUserMedia({
    video: {
        width: { ideal: 1280, min: 640 },
        height: { ideal: 720, min: 480 },
        facingMode: { ideal: 'environment', fallback: 'user' }
    }
});
video.srcObject = stream;

// Renderer Three.js con fondo transparente
renderer = new THREE.WebGLRenderer({ 
    canvas: canvas, 
    alpha: true, 
    antialias: true 
});
renderer.setClearColor(0x000000, 0); // Completamente transparente
```

### 🔹 Desafíos técnicos encontrados

**1. Problemas con AR.js:**
- Conflictos entre A-Frame y Three.js (múltiples instancias)
- Cámara se cerraba inesperadamente
- Detección de marcadores inconsistente

**2. Requisito de HTTPS:**
- Los navegadores modernos requieren HTTPS para acceso a cámara
- Desarrollo local complicado sin certificados SSL
- **Solución**: Uso de ngrok para túneles HTTPS

**3. Compatibilidad de navegadores:**
- Safari requiere configuraciones específicas
- Diferentes APIs de cámara entre navegadores

---

## 📊 Resultados Visuales

![output.gif](resultados/output.gif)

**Funcionalidades implementadas:**
- Cámara en tiempo real como fondo
- Modelo 3D del marcianito superpuesto
- Rotación automática suave
- Control de visibilidad con botón
- Interfaz responsive para móviles

---

## 🧩 Configuración para Desarrollo Local

### Servidor HTTP básico:
```bash
# Python
python -m http.server 8000

# Node.js
npx http-server
```

### Túnel HTTPS con ngrok (RECOMENDADO):
```bash
# Instalar ngrok desde https://ngrok.com/
ngrok http 8000

# Usar la URL HTTPS generada para acceder desde dispositivos móviles
```

### Alternativas de despliegue:
```text
- GitHub Pages (automático HTTPS)
- Netlify Drop (drag & drop)
- Vercel (integración Git)
```

---

## 💬 Reflexión Final

**¿Qué aprendiste o reforzaste con este taller?**

Este taller demostró la importancia de la flexibilidad en el desarrollo web. Aunque el objetivo inicial era usar AR.js con marcadores físicos, los problemas técnicos nos llevaron a explorar una solución más robusta con Three.js puro. Aprendí sobre las limitaciones de las librerías de AR web actuales y la importancia de los requisitos de seguridad (HTTPS) en las APIs modernas del navegador.

**¿Qué parte fue más compleja o interesante?**

La parte más compleja fue diagnosticar los conflictos entre A-Frame y Three.js, que generaban múltiples instancias y problemas de acceso a cámara. Lo más interesante fue descubrir que se puede lograr un efecto de realidad aumentada convincente sin marcadores físicos, simplemente superponiendo un canvas 3D transparente sobre el stream de video.

---

**🎯 Logro**: Implementación exitosa de realidad aumentada web usando tecnologías estándar del navegador y la librería de ThreeJS para el uso de modelos 3D en el navegador.