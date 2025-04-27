# Taller 6
## Python
[Enlace a la implementación en el repositorio](https://github.com/mijx/computacion-visual/tree/main/2025-04-23_taller_algoritmos_rasterizacion_basica/python)

### Resumen de la implementación

Se implementaron tres algoritmos clásicos de rasterización en Python: el algoritmo de Bresenham para líneas, el algoritmo de punto medio para círculos y el algoritmo de rasterización por scanline para triángulos. Cada algoritmo fue graficado utilizando matplotlib.

#### Algoritmo de Bresenham
<img src="resultados\linea.png" width="50%" />

El algoritmo de Bresenham permite dibujar líneas rectas en una cuadrícula de píxeles de manera eficiente, utilizando únicamente operaciones enteras. Se basa en calcular la diferencia entre las coordenadas de los extremos y decidir, en cada paso, cuál es el píxel siguiente que mejor aproxima la línea teórica.

#### Algoritmo de punto medio
<img src="resultados\circulo.png" width="50%" />

El algoritmo de punto medio para círculos permite rasterizar un círculo calculando puntos en un octante y reflejándolos para completar el dibujo. Utiliza una función de decisión para elegir el siguiente píxel y aprovechar la simetría del círculo, optimizando el rendimiento.

#### Rasterización por scanline
<img src="resultados\triangulo.png" width="50%" />

La rasterización por scanline dibuja triángulos recorriendo línea por línea (scanlines) de arriba hacia abajo, llenando los píxeles entre los bordes del triángulo. Se organiza la información de los vértices y se interpolan los extremos de cada línea a medida que se avanza en el eje y.


### Descripción de los prompts
Se hizo uso de herramientas LLM para mejorar la redacción del informe.

### Dificultades presentadas
* Cómo guardar las imágenes creadas con plt.

### Aprendizajes obtenidos
* Cómo implementar rasterización básica de primitivas geométricas en píxeles.
* Cómo manejar la simetría en algoritmos como el de punto medio para optimizar el dibujo de círculos.
* Cómo interpolar posiciones en la rasterización de polígonos mediante el método de scanline.
