# Taller 8
## Three JS
[Enlace a la implementación en el repositorio](https://github.com/mijx/computacion-visual/tree/main/2025-04-23_taller_conversion_formatos_3d/threejs/taller8)

### Resumen de la implementación

Se implementó una escena 3D utilizando `react-three-fiber` y `@react-three/drei`, donde se carga un modelo de tiburón animado en formatos `.glb` y `.gltf`. Se añadió un menú desplegable para seleccionar entre ambos formatos y mostrar el modelo correspondiente, centrado en pantalla. También se incluye un título que cambia dinámicamente según la selección del modelo y un cambio de color asociado.

### Resultado
<img src="resultado\threejsModels.gif" width="50%" />

La aplicación renderiza el modelo seleccionado (.glb o .gltf) y permite cambiar entre ellos desde un menú. El título cambia de texto y color dependiendo del modelo activo. La escena cuenta con controles de órbita para navegación y una luz ambiental para iluminación básica.

### Descripción de los prompts
A lo largo de la implementación, se recurrió al apoyo de herramientas LLM, realizando consultas sobre:
* Cómo centrar correctamente un modelo cargado en la escena.
* Cómo distinguir y cargar condicionalmente modelos `.glb` y `.gltf`.
* Cómo cambiar dinámicamente el contenido y estilo del texto en React con base en un `select`.
* Cómo depurar modelos en Three.js usando helpers.

### Recursos utilizados
* Modelo de tiburón para Three.js obtenido de [Fab](https://www.fab.com/listings/24d6dc8f-7a25-4252-b7d3-c46f01c02b04), que provee la conversión entre archivos.
* Tutorial para cargar modelos GLB: [Sabbir Zaman Blog](https://www.sabbirz.com/blog/from-glb-to-jsx-integrating-3d-models-into-your-react-app)
* Nota: Si se cambia el nombre de los archivos `model.gltf` y `model.bin` correspondientes, recordar cambiar también el nombre referenciado a `model.bin` dentro de `model.gltf`.

### Dificultades presentadas
* El modelo no aparecía centrado a pesar de estar posicionado en `(0, 0, 0)`; se resolvió inspeccionando las transformaciones internas del archivo glTF/GLB.
* Algunos modelos no se veían correctamente sin ajustes de escala o rotación.
* Inicialmente no aparecía nada en pantalla debido a la falta de un `Suspense` o errores silenciosos al cargar el modelo.

### Aprendizajes obtenidos
* Cómo utilizar `SkeletonUtils.clone` para manipular instancias de modelos animados sin errores de referencia.
* Cómo controlar la carga condicional de componentes en React.
* Cómo ajustar posición, escala y rotación de modelos para asegurar su visibilidad.
* Cómo usar helpers (`axesHelper`, `gridHelper`) para depurar la ubicación y orientación de modelos en Three.js.
