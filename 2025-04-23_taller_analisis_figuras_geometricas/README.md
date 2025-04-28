# Taller 7
## Python
[Enlace a la implementación en el repositorio](https://github.com/mijx/computacion-visual/tree/main/2025-04-23_taller_analisis_figuras_geometricas/python/taller7)

### Resumen de la implementación

Se trabajó con la carga de una imagen binarizada, la detección de contornos usando OpenCV, el cálculo de propiedades geométricas básicas (área, perímetro y centroide) y la visualización de estos datos sobre la imagen. Todo el procesamiento se realizó utilizando Python, OpenCV y Matplotlib para la visualización.

La imagen binarizada base para el ejercicio fue:
<img src="python\taller7\img\binarizada.jpg" width="50%" />

#### Dibujar contornos
<img src="python\taller7\img\contornos.jpg" width="50%" />

Se detectaron los contornos principales de la imagen binarizada utilizando `cv2.findContours()` y luego se dibujaron sobre una copia de la imagen original en color, usando `cv2.drawContours()`.

#### Calcular datos de los contornos

Para cada contorno detectado, se calcularon tres propiedades principales:
- Área mediante `cv2.contourArea()`.
- Perímetro mediante `cv2.arcLength()`.
- Centroide utilizando los momentos de imagen (`cv2.moments()`).

#### Visualizar datos de los contornos
<img src="python\taller7\img\contornosetiquetados.jpg" width="50%" />

Se etiquetó cada figura dibujada con sus métricas principales (área, perímetro y coordenadas del centroide) usando `cv2.putText()`, lo que permitió una rápida interpretación visual de los resultados.

### Descripción de los prompts
A lo largo de la implementación, se recurrió al apoyo de herramientas LLM, realizando consultas sobre:
* Cómo adaptar una función de visualización para imágenes binarizadas.
* Cómo calcular el área, perímetro y centroide de contornos en OpenCV.
* Cómo etiquetar y visualizar los datos sobre las figuras detectadas.

### Dificultades presentadas
* Entender la diferencia en el tratamiento de imágenes a color y binarizadas para la correcta visualización.
* Recordar el manejo de momentos (`cv2.moments`) y evitar divisiones por cero al calcular los centroides.

### Aprendizajes obtenidos
* Refuerzo en el uso de `cv2.findContours`, `cv2.drawContours`, `cv2.contourArea`, `cv2.arcLength` y `cv2.moments`.
* Aprendizaje de buenas prácticas para visualizar imágenes binarizadas correctamente en Matplotlib.
* Mejora en la organización del flujo de procesamiento de imágenes: carga, binarización, procesamiento de contornos y visualización de resultados.
