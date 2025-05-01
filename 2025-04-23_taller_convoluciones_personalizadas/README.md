# Taller 9
## Python
[Enlace a la implementación en el repositorio](https://github.com/mijx/computacion-visual/tree/main/2025-04-23_taller_convoluciones_personalizadas/python/taller9)

### Resumen de la implementación

En este taller, se implementó una convolución 2D desde cero utilizando **NumPy**. La imagen base se procesó con diferentes filtros utilizando kernels personalizados para realizar tareas de **enfoque (sharpening)**, **suavizado (blur)** y **detección de bordes (Sobel)**. Se compararon los resultados obtenidos con la función implementada manualmente y los de la función `cv2.filter2D()` de OpenCV.

La imagen base para la práctica fue:
<img src="python\taller9\img\blackwhite.png" width="50%" />

### Implementar una convolución 2D
Se implementó una función manual de convolución 2D que aplica un kernel a cada píxel de la imagen:

    def convolucionar_imagen(imagen, kernel):
        alto, ancho = imagen.shape
        k_alto, k_ancho = kernel.shape
        pad_alto = k_alto // 2
        pad_ancho = k_ancho // 2

        # Crear una imagen de salida del mismo tamaño, inicializada en ceros
        imagen_filtrada = np.zeros_like(imagen)

        # Rellenar la imagen original con ceros en los bordes (padding)
        imagen_padded = np.pad(imagen, ((pad_alto, pad_alto), (pad_ancho, pad_ancho)), mode='constant')

        # Recorrer cada píxel de la imagen original
        for i in range(alto):
            for j in range(ancho):
                # Extraer la región de interés
                region = imagen_padded[i:i + k_alto, j:j + k_ancho]
                # Aplicar el producto punto entre el kernel y la región
                valor = np.sum(region * kernel)
                # Asignar el valor al píxel correspondiente (recortando entre 0-255)
                imagen_filtrada[i, j] = np.clip(valor, 0, 255)

        return imagen_filtrada.astype(np.uint8)

Posteriormente, se ejecutó la función usando cuatro kernels diferentes, para generar filtros sobre la imagen.

#### Kernel de Sharpening (enfoque)
<img src="python\taller9\img\enfocada.png" width="50%" />

El kernel de **sharpening** resalta los detalles de la imagen, aumentando el contraste entre píxeles cercanos y mejorando la definición de bordes.

#### Kernel de Blur
<img src="python\taller9\img\blur.png" width="30%" />

El kernel de **blur** (desenfoque) suaviza la imagen al promediar los valores de los píxeles vecinos, eliminando detalles finos y creando un efecto de suavizado.

#### Kernel de Sobel (derivadas cruzadas)
<img src="python\taller9\img\sobel_derivadas_cruzadas.png" width="30%" />

El kernel de **Sobel** se usa para detectar bordes en la imagen, calculando las derivadas en las direcciones horizontal y vertical. Al combinar estas derivadas, se pueden resaltar las esquinas y los bordes en la imagen.

#### Kernel de Sobel Horizontal
<img src="python\taller9\img\sobel_horizontal.png" width="30%" />

El kernel de **Sobel Horizontal** resalta los bordes en la dirección horizontal. Se utiliza junto con el kernel de Sobel vertical para obtener un gradiente completo y detectar las esquinas en la imagen.

#### Comparación: manual vs filtro cv2

Se compararon los resultados obtenidos con la implementación manual de la convolución y los de OpenCV utilizando la función `cv2.filter2D()`.

<img src="python\taller9\img\comparacion_enfoque.png" width="100%" />

<img src="python\taller9\img\comparacion_blur.png" width="100%" />

<img src="python\taller9\img\comparacion_sobel.png" width="100%" />

### Descripción de los prompts
A lo largo de la implementación, se recurrió al apoyo de herramientas LLM, realizando consultas sobre:
* Cómo implementar una convolución 2D desde cero usando **NumPy**.
* Qué kernels se pueden usar para **enfoque**, **suavizado** y **detección de bordes**.
* Comparación entre la implementación manual y las funciones de OpenCV.

### Dificultades presentadas
* Implementar la convolución manualmente sin perder eficiencia fue un reto, ya que hubo que manejar bordes y definir correctamente el padding.
* Al aplicar varios kernels, asegurarse de que los resultados coincidieran entre la implementación manual y la de OpenCV fue un desafío.

### Aprendizajes obtenidos
* Aprendí cómo implementar la convolución 2D desde cero utilizando **NumPy** y cómo aplicar diferentes filtros personalizados a imágenes.
* Mejoré mi comprensión de los **kernels** y su impacto en el procesamiento de imágenes, especialmente en la detección de bordes y el suavizado.
* Me familiaricé con la comparación de métodos, tanto manuales como de bibliotecas como OpenCV, para validar resultados.
