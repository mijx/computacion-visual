# Taller 3
## Python
[Enlace a la implementación en el repositorio](https://github.com/mijx/computacion-visual/tree/main/2025-04-21_taller_ojos_digitales/python/taller3)

### Resumen de la implementación

Se implementaron varios filtros de procesamiento de imágenes usando OpenCV y Numpy en Python. Se aplicaron transformaciones como escala de grises, desenfoque (blur), cambio de color, enfoque (sharpen), y detección de bordes mediante los filtros de Sobel y Laplaciano.

La imagen sobre la cual se trabajó fue:
<img src="python\taller3\img\aurora.png" width="50%" />

#### Filtro Escala de grises
<img src="python\taller3\img\blackwhite.jpg" width="50%" />

Se convirtió la imagen original a escala de grises usando `cv2.cvtColor`, facilitando la detección de contrastes y formas sin distracción de colores.

#### Filtro Blur
<img src="python\taller3\img\blurred.jpg" width="50%" />

Se aplicó un desenfoque a la imagen utilizando un filtro de suavizado (`cv2.GaussianBlur`), reduciendo el ruido y suavizando detalles pequeños.

#### Filtro Cambio de color
<img src="python\taller3\img\rose.jpg" width="50%" />

Se transformó el tono de la imagen hacia un color rosáceo, modificando el canal de tono (Hue) en el espacio de color HSV para lograr un resultado más natural.

#### Filtro Sharpened (enfocar)
<img src="python\taller3\img\sharpened.jpg" width="50%" />

Se utilizó un filtro de enfoque aplicando una máscara de convolución que resalta los bordes y detalles finos de la imagen.

#### Detección de bordes

##### Filtro Sobel:
<img src="python\taller3\img\sobel.jpg" width="50%" />

Se detectaron bordes en direcciones X e Y aplicando el operador de Sobel y combinando sus magnitudes para identificar las transiciones fuertes en la imagen.

##### Filtro Laplaciano:
<img src="python\taller3\img\laplacian.jpg" width="50%" />

Se aplicó el operador Laplaciano para detectar bordes mediante un enfoque de segunda derivada, resaltando cambios abruptos de intensidad.

### Descripción de los prompts
A lo largo de la implementación, se recurrió al apoyo de herramientas LLM, realizando consultas sobre:
* Aplicación de filtros de Sobel y Laplaciano en OpenCV.
* Cómo transformar imágenes de BGR a HSV y aplicar cambios de tono.
* Guardar imágenes modificadas correctamente en formato BGR usando `cv2.imwrite`.

### Dificultades presentadas
* Ajustar los cambios de color de manera que se vieran naturales y no forzados.
* Manejar correctamente las conversiones entre formatos de color (BGR, RGB, HSV) para que las imágenes se guardaran y visualizaran adecuadamente.

### Aprendizajes obtenidos
* Manipulación básica de imágenes en OpenCV.
* Aplicación de filtros convolucionales para modificación y detección de bordes.
* Importancia del manejo de espacios de color para cambios de tono y guardado de imágenes.
