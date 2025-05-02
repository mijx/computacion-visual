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

## Python
[Enlace a la implementación en el repositorio](https://github.com/mijx/computacion-visual/tree/main/2025-04-21_taller_estructuras_3d/python)

### Resumen de la implementación

<img src="python\resultado\PythonMuestra1.gif" width="50%" />

<img src="python\resultado\PythonMuestra2.gif" width="50%" />

*Salida del terminal:*

     Modelo cargado:
     Número de vértices: 3549
     Número de caras: 6112
     Número de aristas: 18336

La implementación en Python consistió en la carga y visualización de un modelo 3D en formato `.glb` utilizando las librerías `trimesh` y `open3d`.

Primero, se cargó el archivo usando `trimesh`, que permite manipular tanto escenas como mallas individuales. En caso de que el archivo contuviera múltiples objetos, se unificaron usando `trimesh.util.concatenate`.

Luego, los datos de vértices y caras se transformaron en una malla compatible con Open3D para poder visualizarla. Se calcularon las normales de los vértices para mejorar la iluminación de la malla. Finalmente, se mostró la geometría en una ventana interactiva donde se pueden usar controles de orbitación con el mouse.

### Descripción de los prompts

Durante el desarrollo se utilizaron herramientas LLM para consultar y resolver:
* Cómo cargar un archivo `.glb` desde una ruta relativa correctamente.
* Qué hacer cuando `open3d` no visualizaba colores o el modelo parecía estar vacío.
* Cómo convertir una `trimesh.Scene` a una única malla para visualizarla en Open3D.
* Cómo mostrar estadísticas como número de vértices, caras y aristas en consola.

### Dificultades presentadas

* El modelo no se cargaba al principio porque la ruta usada no coincidía con el directorio de ejecución. Se solucionó utilizando `os.path.abspath(__file__)` para construir rutas absolutas.
* `open3d` no reconocía los colores directamente desde el archivo `.glb`, ya que solo se importaban vértices y caras. Se intentaron varias estrategias para recuperar los colores, pero finalmente se optó por visualizar la malla sin texturas.
* La malla no se mostraba cuando el archivo estaba vacío o mal convertido; también surgió un error al acceder a `vertex_colors` en un objeto de tipo `TextureVisuals`.

### Aprendizajes aprendidos

* Uso combinado de `trimesh` y `open3d` para cargar y visualizar modelos 3D.
* Transformación de escenas en mallas para simplificar la visualización.
* Visualización básica interactiva con Open3D y cálculo de normales.
* Manejo de rutas relativas/absolutas en Python para asegurar portabilidad del código.
* Recuperación e impresión de información estructural de un modelo: número de vértices, caras y aristas.
