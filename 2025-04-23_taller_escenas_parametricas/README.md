# Taller 9
## Three JS
[Enlace a la implementación en el repositorio](https://github.com/mijx/computacion-visual/tree/main/2025-04-23_taller_escenas_parametricas/threejs/taller9)

### Resumen de la implementación

Se cargó un modelo 3D tipo glb (Burger lowpoly), obtenido de [Fab](https://www.fab.com/listings/e4579c6c-2e83-460e-8295-621c843852d5):

Se instanció un array de objetos en escena mediante `map`, asignando a cada instancia una posición, rotación y escala distinta. Esto permitió ver múltiples versiones del mismo modelo en diferentes ubicaciones del espacio 3D.

Se agregaron controles con Leva para modificar dinámicamente desde la interfaz la rotación y escala de cada objeto individual, facilitando la experimentación visual y la interacción en tiempo real.

### Resultado 1: OrbitControls
<img src="resultados\threejsMuestra1.gif" width="50%" />

Explicación: Se utilizó el componente `OrbitControls` de `@react-three/drei` para permitir la rotación libre de la cámara alrededor de la escena. Esto permite visualizar claramente la disposición tridimensional del array de objetos, con interacción fluida del usuario.

#### Resultado 2: controles con Leva
<img src="resultados\threejsMuestra2.gif" width="50%" />

Explicación: En la imagen se aprecia cómo cada objeto tiene controles independientes en Leva. Es posible modificar su escala y rotación en tiempo real usando sliders, lo que demuestra la integración entre React Three Fiber y la interfaz de usuario de Leva.

### Descripción de los prompts
A lo largo de la implementación, se recurrió al apoyo de herramientas LLM, realizando consultas sobre:
* Cómo hacer que el `<Canvas />` ocupe toda la pantalla.
* Cómo usar `map` para instanciar múltiples modelos con diferentes transformaciones.
* Cómo integrar `leva` con React Three Fiber para modificar propiedades como rotación y escala.
* Cómo organizar el código eficientemente usando índices para generar carpetas o estructuras dinámicas de UI.

### Dificultades presentadas
* Ajustar correctamente el tamaño del `<Canvas />` para ocupar la pantalla completa.
* Sincronizar el estado de Leva con cada instancia del objeto renderizado, asegurando que los controles no se superpongan.
* Comprender cómo escalar adecuadamente los modelos sin afectar la visualización general.

### Aprendizajes obtenidos
* Uso avanzado de React Three Fiber para renderizar múltiples modelos desde un array.
* Implementación de OrbitControls y Environment para mejorar la interacción y ambientación visual.
* Uso de la librería Leva para crear interfaces de control dinámico y en tiempo real en proyectos 3D.
