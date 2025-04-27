# Taller 5
## Python
[Enlace a la implementación en el repositorio](https://github.com/mijx/computacion-visual/tree/main/2025-04-21_taller_imagen_matriz_pixeles/python/taller5)

### Resumen de la implementación
Se realizaron operaciones básicas de procesamiento de imágenes con OpenCV y Matplotlib, incluyendo la visualización de canales de color, manipulación de regiones mediante slicing, cálculo de histogramas de intensidades, y ajustes de brillo y contraste.

Imagen base utilizada:

<img src="python\taller5\img\aurora.png" width="50%" />

#### Mostrar los canales RGB por separado
Se separaron los canales de color rojo, verde y azul de la imagen para observar su contribución individual.

Canal R:

<img src="python\taller5\img\canal_r.png" width="50%" />

Canal G:

<img src="python\taller5\img\canal_g.png" width="50%" />

Canal B:

<img src="python\taller5\img\canal_b.png" width="50%" />

#### Mostrar los canales HSV por separado
Se convirtió la imagen al espacio de color HSV para analizar la tonalidad (Hue), saturación (Saturation) y valor (Value) de la imagen.

Canal H:

<img src="python\taller5\img\canal_h.png" width="50%" />

Canal S:

<img src="python\taller5\img\canal_s.png" width="50%" />

Canal V:

<img src="python\taller5\img\canal_v.png" width="50%" />

#### Slicing de matrices

##### Cambiar el color de un área rectangular
<img src="python\taller5\img\slicingcolor.png" width="50%" />

Se modificó el color de un área rectangular ubicada en el centro de la imagen, aplicando un color rojo intenso.

##### Sustituir una región por otra parte de la imagen
<img src="python\taller5\img\slicingsustitucion.png" width="50%" />

La mitad derecha de la imagen fue sustituida por una copia de la mitad izquierda.

#### Histograma de intensidades
<img src="python\taller5\img\histograma.png" width="50%" />

Se calcularon y visualizaron los histogramas de intensidades en escala de grises, utilizando tanto `cv2.calcHist()` como `matplotlib.pyplot.hist()`.

#### Ajuste de brillo y contraste
<img src="python\taller5\img\contrastbrightness.png" width="50%" />

Se modificó el brillo y el contraste de la imagen usando `cv2.convertScaleAbs()`, incrementando ambos valores para realzar la imagen.

### Descripción de los prompts
A lo largo de la implementación, se recurrió al apoyo de herramientas LLM, realizando consultas sobre:
* Cómo separar y visualizar los canales RGB y HSV de una imagen.
* Cómo modificar regiones específicas usando slicing.
* Cómo calcular y graficar histogramas de intensidades.
* Cómo aplicar ajustes de brillo y contraste de manera programática.

### Dificultades presentadas
* Entender la relación entre slicing de matrices y coordenadas de imagen (orden filas/columnas).
* Ajustar los parámetros de brillo y contraste para no saturar la imagen.

### Aprendizajes obtenidos
* La composición de los diferentes espacios de color (BGR, RGB, HSV).
* Cómo construir histogramas de intensidad.
* Cómo modificar dinámicamente propiedades visuales como brillo y contraste.
