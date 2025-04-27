# Taller 4
## Python
[Enlace a la implementación en el repositorio](https://github.com/mijx/computacion-visual/tree/main/2025-04-21_taller_segmentacion_formas/python/taller4)

### Resumen de la implementación

Se realizó la segmentación binaria de una imagen cargada con OpenCV, seguida de la detección de contornos, cálculo de centros de masa y cajas delimitadoras (bounding boxes), y se calcularon métricas básicas como número de formas, área y perímetro promedio. Además, se aplicaron filtros básicos de procesamiento de imágenes.

La imagen sobre la cual se trabajó fue:

<img src="python\taller4\img\aurora.png" width="50%" />

#### Segmentación binaria
##### Umbral fijo:
<img src="python\taller4\img\umbralfijo.jpg" width="50%" />

Se aplicó un umbral fijo utilizando `cv2.threshold`, estableciendo un valor de 127 para separar los pixeles en blanco y negro.

##### Umbral adaptativo:
<img src="python\taller4\img\umbraladaptativo.jpg" width="50%" />

Se aplicó un umbral adaptativo usando `cv2.adaptiveThreshold`, permitiendo que el umbral varíe de acuerdo a la vecindad de cada píxel, logrando una segmentación más precisa en condiciones de iluminación no uniforme.

#### Detección de contornos
<img src="python\taller4\img\contornos.jpg" width="50%" />

Se detectaron los contornos de las formas binarizadas utilizando `cv2.findContours`, extrayendo los bordes externos de cada objeto identificado en la imagen.

#### Centro de masa y bounding boxes
<img src="python\taller4\img\centrosyboxes.jpg" width="50%" />

Se calcularon los centros de masa con `cv2.moments` y se dibujaron círculos rojos en esos puntos. Además, se trazaron cajas delimitadoras (bounding boxes) alrededor de cada forma usando `cv2.boundingRect`.

#### Métricas básicas
Se calcularon las métricas principales a partir de los contornos detectados, y los resultados fueron:

    Número de formas detectadas: 2
    Área promedio: 40550.00
    Perímetro promedio: 765.09

### Descripción de los prompts
A lo largo de la implementación, se recurrió al apoyo de herramientas LLM, realizando consultas sobre:
* Cómo realizar segmentación binaria con umbral fijo y adaptativo.
* Cómo detectar y dibujar contornos en una imagen.
* Cómo calcular centros de masa y bounding boxes.
* Cómo calcular métricas básicas de formas detectadas.

### Dificultades presentadas
* Realizar un preprocesamiento adecuado a la imagen antes de calcular contornos.
* Ajustar correctamente los parámetros de umbral adaptativo para lograr una buena segmentación.

### Aprendizajes obtenidos
* Uso de técnicas de segmentación y detección de contornos en imágenes.
* Aplicación de momentos para hallar centros de masa.
* Cálculo de métricas geométricas básicas en procesamiento de imágenes.
