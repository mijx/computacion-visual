# Taller 2
## Three JS
[Enlace a la implementación en el repositorio](https://github.com/mijx/computacion-visual/tree/main/2025-04-21_taller_jerarquias_transformaciones/threejs)

### Resumen de la implementación

Se creó una escena en React Three Fiber compuesta por un nodo padre (group) y dos nodos hijos (mesh) representados como cubos. Se utilizaron sliders de la librería Leva para controlar en tiempo real la rotación y traslación tanto del grupo padre como de cada hijo de manera independiente, permitiendo visualizar las transformaciones jerárquicas en 3D.

#### Muestra #1: desplazar nodo padre
<img src="threejs\gifs\animacion1padre.gif" width="50%" />

Al trasladar el nodo padre en el eje Y, ambos cubos (hijos) se movieron juntos, manteniendo su posición relativa entre sí. Como están agrupados dentro del group, cualquier traslación aplicada al padre afecta a toda la estructura de forma conjunta, desplazando los hijos como un solo bloque.

#### Muestra #2: desplazar hijos y padre
<img src="threejs\gifs\animacion2hijosypadre.gif" width="50%" />

Cuando se desplazó o rotó cada hijo, usando los sliders del control individual, estos se movieron localmente respecto al grupo y no afectó la posición del otro hijo.

Luego, todo el grupo (incluyendo la nueva posición de los hijos) se trasladó en bloque hacia arriba o abajo. Esto evidencia que las transformaciones locales de los hijos se aplican primero, y luego la transformación global del padre afecta a todo el conjunto.

### Descripción de los prompts
A lo largo de la immplementación, se recurrió al apoyo de herramientas LLM, realizando consultas sobre:
* Utilizar useControls de Leva para generar sliders interactivos que modifican propiedades específicas: rotación en el eje Y y posición en Y del grupo padre, y rotación en X y posición en X de cada cubo hijo.

### Dificultades presentadas
* Inicialmente los cubos se veían oscuros por falta de iluminación adecuada, lo que se solucionó añadiendo una luz ambiental y un pointLight con mayor intensidad.
* Añadir sliders para lograr que tanto los hijos como el padre pudieran ser manipulados de forma independiente agregó un nivel más de complejidad.

### Aprendizajes obtenidos
* Se comprendió mejor cómo funciona la estructura jerárquica de transformación en React Three Fiber.
* El uso de group para agrupar objetos y mesh para crear hijos en el grupo.
* Integrar Leva para modificar dinámicamente parámetros en la escena.
* La correcta configuración de la luz en una escena 3D.
