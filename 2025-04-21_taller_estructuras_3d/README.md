# Taller 1
## Three JS
[Enlace a la implementación en el repositorio](https://github.com/mijx/computacion-visual/tree/main/2025-04-21_taller_estructuras_3d/threejs/model-3d)

### Resumen de la implementación

<img src="threejs\model-3d\public\resultado\orbitcontrols.gif" width="50%" />

La implementación consistió en integrar un modelo 3D en una aplicación web desarrollada con React, usando las librerías React Three Fiber y Drei para el manejo de gráficos 3D.

Primero, se obtuvo el modelo 3D en [esta publicación](https://www.fab.com/listings/2ef5089c-69b6-4152-879b-896dfb21dfd6). Luego, se transformó el archivo .gltf en un componente .jsx utilizando la herramienta gltfjsx, lo que permitió importar y manipular el modelo dentro de la escena de manera más sencilla.

Dentro del componente principal App.jsx, se creó un Canvas como contenedor 3D, configurado con luz ambiental y controles de cámara interactivos brindados por OrbitControls.

Se ajustó el modelo en escala, rotación y posición para que apareciera adecuadamente en la vista inicial. Finalmente, se cuidaron detalles de estilo CSS para asegurar que el Canvas ocupara correctamente el espacio deseado en la pantalla.

### Descripción de los prompts
A lo largo de la immplementación, se recurrió al apoyo de herramientas LLM, realizando consultas sobre:
* Ajuste del tamaño, fondo y posición del Canvas.
* Escalado y rotación del modelo para mejorar su presentación inicial.
* Solución de problemas comunes como rutas de importación incorrectas, errores de carga, y modelo diminuto o desalineado.

### Dificultades presentadas
* Inicialmente el modelo no era visible debido a problemas de escala muy pequeña, y también porque la vista inicial mostraba un ángulo lateral no deseado.
* Ajustes de layout CSS: El Canvas inicialmente generaba una barra deslizadora horizontal o no ocupaba el tamaño deseado. Se requirió ajustar el #root en CSS y definir correctamente el tamaño del Canvas para mantener una presentación limpia y sin desbordamientos.
* A pesar de aumentar la escala, el modelo estaba desplazado hacia abajo y el personaje estaba de perfil, lo que obligó a realizar transformaciones de posición y rotación.

### Aprendizajes aprendidos

* Importar y manejar modelos .gltf en React Three Fiber.
* Uso básico de materiales en Three.js.
* Configuración de la escena y control de cámara.
* Manejo de errores de importación y buenas prácticas para organizar los archivos del proyecto.
* Estilización de la visualización mediante CSS.
