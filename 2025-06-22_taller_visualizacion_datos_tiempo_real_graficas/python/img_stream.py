import random
import time
import threading
from pathlib import Path
from typing import Optional, Callable
import cv2
import numpy as np

class ImageStreamer:
    def __init__(self, 
                 images_dir: str = "imgs", 
                 max_images: int = 15, 
                 interval_seconds: float = 1.0):
        """
        Inicializa el streamer de imágenes.
        
        Args:
            images_dir: Directorio que contiene las imágenes
            max_images: Número máximo de imágenes a mostrar
            interval_seconds: Intervalo en segundos entre imágenes
        """
        self.images_dir = Path(images_dir)
        self.max_images = max_images
        self.interval_seconds = interval_seconds
        self.current_image_count = 0
        self.is_streaming = False
        self.current_image = None
        self.current_image_path = None
        self.streaming_thread = None
        self.image_callback = None
        
        # Cargar lista de imágenes disponibles
        self._load_available_images()
    
    def _load_available_images(self):
        """Carga la lista de imágenes disponibles desde el directorio."""
        if not self.images_dir.exists():
            raise FileNotFoundError(f"El directorio {self.images_dir} no existe")
        
        # Buscar archivos de imagen comunes
        image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif'}
        self.available_images = []
        
        for file_path in self.images_dir.iterdir():
            if file_path.suffix.lower() in image_extensions:
                self.available_images.append(file_path)
        
        if not self.available_images:
            raise ValueError(f"No se encontraron imágenes en {self.images_dir}")
        
        print(f"Imágenes disponibles: {[img.name for img in self.available_images]}")
    
    def _select_random_image(self) -> Path:
        """Selecciona una imagen aleatoria de la lista disponible."""
        return random.choice(self.available_images)
    
    def _load_image(self, image_path: Path) -> np.ndarray:
        """Carga una imagen usando OpenCV."""
        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError(f"No se pudo cargar la imagen: {image_path}")
        return image
    
    def get_current_image(self) -> Optional[np.ndarray]:
        """Retorna la imagen actual cargada."""
        return self.current_image
    
    def get_current_image_path(self) -> Optional[Path]:
        """Retorna la ruta de la imagen actual."""
        return self.current_image_path
    
    def get_current_animal_name(self) -> Optional[str]:
        """Extrae el nombre del animal de la imagen actual."""
        if self.current_image_path:
            return self.current_image_path.stem
        return None
    
    def set_image_callback(self, callback: Callable[[np.ndarray, str], None]):
        """
        Establece un callback que se ejecutará cada vez que se seleccione una nueva imagen.
        
        Args:
            callback: Función que recibe (imagen, nombre_animal)
        """
        self.image_callback = callback
    
    def _streaming_loop(self):
        """Loop principal del streaming de imágenes."""
        while self.is_streaming and self.current_image_count < self.max_images:
            # Seleccionar imagen aleatoria
            selected_image_path = self._select_random_image()
            
            try:
                # Cargar la imagen
                image = self._load_image(selected_image_path)
                
                # Actualizar estado
                self.current_image = image
                self.current_image_path = selected_image_path
                self.current_image_count += 1
                
                animal_name = self.get_current_animal_name() or "unknown"
                
                print(f"Imagen {self.current_image_count}/{self.max_images}: {animal_name}")
                
                # Ejecutar callback si está definido
                if self.image_callback:
                    self.image_callback(image, animal_name)
                
                # Esperar el intervalo especificado
                time.sleep(self.interval_seconds)
                
            except Exception as e:
                print(f"Error al procesar imagen {selected_image_path}: {e}")
                continue
        
        self.is_streaming = False
        print("Streaming finalizado")
    
    def start_streaming(self):
        """Inicia el streaming de imágenes en un hilo separado."""
        if self.is_streaming:
            print("El streaming ya está en curso")
            return
        
        self.is_streaming = True
        self.current_image_count = 0
        self.streaming_thread = threading.Thread(target=self._streaming_loop)
        self.streaming_thread.daemon = True
        self.streaming_thread.start()
        print(f"Streaming iniciado: {self.max_images} imágenes cada {self.interval_seconds}s")
    
    def stop_streaming(self):
        """Detiene el streaming de imágenes."""
        self.is_streaming = False
        if self.streaming_thread and self.streaming_thread.is_alive():
            self.streaming_thread.join()
        print("Streaming detenido")
    
    def is_active(self) -> bool:
        """Retorna True si el streaming está activo."""
        return self.is_streaming
    
    def get_progress(self) -> tuple:
        """Retorna el progreso actual (imagen_actual, total_imágenes)."""
        return (self.current_image_count, self.max_images)


# Ejemplo de uso y función de callback para mostrar imágenes
def display_image_callback(image: np.ndarray, animal_name: str):
    """Callback de ejemplo para mostrar la imagen con OpenCV."""
    # Redimensionar para mejor visualización
    height, width = image.shape[:2]
    if width > 800:
        scale = 800 / width
        new_width = int(width * scale)
        new_height = int(height * scale)
        image = cv2.resize(image, (new_width, new_height))
    
    # Mostrar la imagen
    cv2.imshow(f'Animal Detection - {animal_name}', image)
    cv2.waitKey(1)  # Necesario para actualizar la ventana


if __name__ == "__main__":
    # Ejemplo de uso básico
    try:
        streamer = ImageStreamer(
            images_dir="imgs",
            max_images=15,
            interval_seconds=1.0
        )
        
        # Configurar callback para mostrar imágenes
        streamer.set_image_callback(display_image_callback)
        
        # Iniciar streaming
        streamer.start_streaming()
        
        # Mantener el programa corriendo hasta que termine el streaming
        while streamer.is_active():
            time.sleep(0.1)
        
        # Cerrar ventanas de OpenCV
        cv2.destroyAllWindows()
        
    except KeyboardInterrupt:
        print("\nDeteniendo streaming...")
        if 'streamer' in locals():
            streamer.stop_streaming()
        cv2.destroyAllWindows()
    except Exception as e:
        print(f"Error: {e}")
