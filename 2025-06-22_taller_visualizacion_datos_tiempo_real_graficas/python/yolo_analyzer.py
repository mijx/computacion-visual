import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
from ultralytics import YOLO
from typing import List, Dict
from img_stream import ImageStreamer
from collections import Counter

class YoloAnalyzer:
    def __init__(self, 
                 model_path: str = "yolov8n.pt",
                 images_dir: str = "imgs",
                 max_images: int = 15,
                 interval_seconds: float = 1.0,
                 confidence_threshold: float = 0.5):
        """
        Inicializa el analizador YOLO con streaming de imágenes.
        
        Args:
            model_path: Ruta al modelo YOLO (se descarga automáticamente si no existe)
            images_dir: Directorio con las imágenes
            max_images: Número máximo de imágenes a procesar
            interval_seconds: Intervalo entre imágenes
            confidence_threshold: Umbral de confianza para detecciones
        """
        self.model_path = model_path
        self.confidence_threshold = confidence_threshold
        self.model = None
        self.current_detections = []
        self.detection_log = []
        self.display_image = None
        self.is_running = False
        self.class_counts = Counter()  # Contador para las clases detectadas
        
        # Configurar el streamer de imágenes
        self.image_streamer = ImageStreamer(
            images_dir=images_dir,
            max_images=max_images,
            interval_seconds=interval_seconds
        )
        
        # Configurar callback del streamer
        self.image_streamer.set_image_callback(self._process_image_callback)
        
        # Configurar la ventana de visualización
        self.window_name = "YOLO Animal Detection - Real Time Analysis"
        
        # Dimensiones de la ventana
        self.window_width = 1920
        self.window_height = 1080
        self.left_column_width = self.window_width // 2
        self.right_column_width = self.window_width // 2
        
        # Cargar modelo YOLO
        self._load_yolo_model()
    
    def _load_yolo_model(self):
        """Carga el modelo YOLO."""
        try:
            print(f"Cargando modelo YOLO: {self.model_path}")
            self.model = YOLO(self.model_path)
            print("Modelo YOLO cargado exitosamente")
        except Exception as e:
            print(f"Error al cargar el modelo YOLO: {e}")
            raise
    
    def _process_image_callback(self, image: np.ndarray, animal_name: str):
        """
        Callback que procesa cada imagen con YOLO.
        
        Args:
            image: Imagen a procesar
            animal_name: Nombre real del animal en la imagen
        """
        # Realizar detección con YOLO
        if self.model is None:
            return
        results = self.model(image, conf=self.confidence_threshold, verbose=False)
        
        # Procesar resultados
        detections = self._extract_detections(results[0], animal_name)
        self.current_detections = detections
        
        # Crear imagen con overlay
        display_img = self._create_display_image(image.copy(), detections, animal_name)
        self.display_image = display_img
        
        # Actualizar log
        self._update_detection_log(detections, animal_name)
    
    def _extract_detections(self, result, true_animal: str) -> List[Dict]:
        """
        Extrae las detecciones del resultado de YOLO, limitando a una sola detección por imagen.
        Se selecciona la detección con mayor confianza.
        
        Args:
            result: Resultado de YOLO
            true_animal: Nombre real del animal
            
        Returns:
            Lista con máximo una detección (la de mayor confianza)
        """
        detections = []
        
        if result.boxes is not None:
            boxes = result.boxes
            best_detection = None
            best_confidence = 0.0
            
            # Encontrar la detección con mayor confianza
            for i in range(len(boxes)):
                confidence = float(boxes.conf[i].cpu().numpy())
                
                if confidence > best_confidence:
                    x1, y1, x2, y2 = boxes.xyxy[i].cpu().numpy()
                    class_id = int(boxes.cls[i].cpu().numpy())
                    class_name = self.model.names[class_id] if self.model else "unknown"
                    
                    best_detection = {
                        'bbox': (int(x1), int(y1), int(x2), int(y2)),
                        'confidence': confidence,
                        'class_name': class_name,
                        'class_id': class_id,
                        'true_animal': true_animal,
                        'is_correct': self._is_detection_correct(class_name, true_animal)
                    }
                    best_confidence = confidence
            
            # Agregar solo la mejor detección si existe
            if best_detection is not None:
                detections.append(best_detection)
                # Actualizar contador de clases
                self.class_counts[best_detection['class_name']] += 1
        
        return detections
    
    def _is_detection_correct(self, detected_class: str, true_animal: str) -> bool:
        """
        Verifica si la detección es correcta comparando con el animal real.
        
        Args:
            detected_class: Clase detectada por YOLO
            true_animal: Animal real en la imagen
            
        Returns:
            True si la detección es correcta
        """
        # Mapeo de nombres de archivos a clases de YOLO
        animal_mapping = {
            'dog': ['dog'],
            'cat': ['cat'],
            'bird': ['bird'],
            'cow': ['cow'],
            'sheep': ['sheep'],
            'elephant': ['elephant']
        }
        
        true_classes = animal_mapping.get(true_animal.lower(), [])
        return detected_class.lower() in [cls.lower() for cls in true_classes]
    
    def _create_display_image(self, image: np.ndarray, detections: List[Dict], true_animal: str) -> np.ndarray:
        """
        Crea la imagen de visualización con layout de dos columnas: 
        Izquierda (imagen completa), Derecha (gráfico de pastel).
        
        Args:
            image: Imagen base
            detections: Lista de detecciones
            true_animal: Animal real
            
        Returns:
            Imagen combinada con layout de dos columnas
        """
        # Redimensionar imagen para la columna izquierda (mantener toda la altura)
        image_resized = cv2.resize(image, (self.left_column_width, self.window_height))
        
        # Dibujar detecciones en la imagen
        image_with_detections = self._draw_detections_on_image(
            image_resized, detections, true_animal, image.shape
        )
        
        # Crear gráfico de pastel (columna derecha)
        pie_chart = self._create_pie_chart(self.right_column_width, self.window_height)
        
        # Combinar ambas columnas horizontalmente
        final_image = np.hstack([image_with_detections, pie_chart])
        
        return final_image
    
    def _draw_detections_on_image(self, image: np.ndarray, detections: List[Dict], 
                                true_animal: str, original_shape: tuple) -> np.ndarray:
        """
        Dibuja las detecciones y información en la imagen.
        
        Args:
            image: Imagen redimensionada donde dibujar
            detections: Lista de detecciones
            true_animal: Nombre del animal real
            original_shape: Forma original de la imagen (height, width, channels)
        """
        # Obtener dimensiones
        display_height, display_width = image.shape[:2]
        original_height, original_width = original_shape[:2]
        
        # Calcular factores de escala
        scale_x = display_width / original_width
        scale_y = display_height / original_height
        
        # Dibujar bounding boxes y etiquetas
        for detection in detections:
            x1, y1, x2, y2 = detection['bbox']
            confidence = detection['confidence']
            class_name = detection['class_name']
            is_correct = detection['is_correct']
            
            # Escalar coordenadas a las dimensiones de la imagen de visualización
            x1_scaled = int(x1 * scale_x)
            y1_scaled = int(y1 * scale_y)
            x2_scaled = int(x2 * scale_x)
            y2_scaled = int(y2 * scale_y)
            
            # Asegurar que las coordenadas estén dentro de los límites
            x1_scaled = max(0, min(x1_scaled, display_width - 1))
            y1_scaled = max(0, min(y1_scaled, display_height - 1))
            x2_scaled = max(0, min(x2_scaled, display_width - 1))
            y2_scaled = max(0, min(y2_scaled, display_height - 1))
            
            # Color verde para detecciones correctas, rojo para incorrectas
            color = (0, 255, 0) if is_correct else (0, 0, 255)
            
            # Dibujar bounding box
            cv2.rectangle(image, (x1_scaled, y1_scaled), (x2_scaled, y2_scaled), color, 3)
            
            # Preparar texto de la etiqueta
            label = f"{class_name}: {confidence:.2f}"
            if is_correct:
                label += " ✓"
            else:
                label += " ✗"
            
            # Dibujar fondo del texto
            font_scale = 0.7
            thickness = 2
            (text_width, text_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
            cv2.rectangle(image, (x1_scaled, y1_scaled - text_height - 10), 
                         (x1_scaled + text_width, y1_scaled), color, -1)
            
            # Dibujar texto
            cv2.putText(image, label, (x1_scaled, y1_scaled - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), thickness)
        
        # Agregar información del animal real
        info_text = f"Animal Real: {true_animal.upper()}"
        cv2.putText(image, info_text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 3)
        cv2.putText(image, info_text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)
        
        # Agregar progreso
        current, total = self.image_streamer.get_progress()
        progress_text = f"Progreso: {current}/{total}"
        cv2.putText(image, progress_text, (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 3)
        cv2.putText(image, progress_text, (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        
        return image
    

    
    def _create_pie_chart(self, width: int, height: int) -> np.ndarray:
        """
        Crea un gráfico de pastel dinámico con matplotlib.
        
        Args:
            width: Ancho del gráfico
            height: Alto del gráfico
            
        Returns:
            Imagen del gráfico de pastel como array de NumPy
        """
        # Configurar matplotlib para no mostrar ventanas
        plt.ioff()
        
        # Crear figura con fondo negro
        fig, ax = plt.subplots(figsize=(width/100, height/100), facecolor='black')
        ax.set_facecolor('black')
        
        if not self.class_counts:
            # Si no hay datos, mostrar mensaje
            ax.text(0.5, 0.5, 'Esperando\ndetecciones...', 
                   horizontalalignment='center', verticalalignment='center',
                   transform=ax.transAxes, fontsize=14, color='white')
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
        else:
            # Datos para el gráfico de pastel
            labels = list(self.class_counts.keys())
            sizes = list(self.class_counts.values())
            total_detections = sum(sizes)
            
            # Colores vibrantes para cada clase
            colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF99CC', '#C2C2F0', '#FFB3E6', '#C4E17F']
            colors = colors[:len(labels)]  # Usar solo los colores necesarios
            
            # Crear gráfico de pastel
            # labels va dentro del segmento (nombres de clase)
            # autopct va fuera del segmento (porcentajes)
            pie_result = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                              colors=colors, startangle=90,
                              textprops={'color': 'white', 'fontsize': 9},
                              pctdistance=1.1,  # Porcentajes fuera del círculo
                              labeldistance=0.6)  # Nombres dentro del segmento
            
            # Título
            ax.set_title(f'Detecciones por Clase\n(Total: {total_detections})', 
                        color='white', fontsize=12, pad=20)
            
            # Mejorar la apariencia del texto si hay elementos suficientes
            if len(pie_result) >= 3:
                wedges, texts, autotexts = pie_result
                
                # Configurar texto de las etiquetas (nombres de clase, dentro)
                for text in texts:
                    text.set_color('white')
                    text.set_fontweight('bold')
                    text.set_fontsize(10)
                
                # Configurar texto de los porcentajes (fuera)
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontweight('bold')
                    autotext.set_fontsize(9)
        
        # Convertir la figura a imagen usando PIL
        from PIL import Image
        import io
        
        # Guardar la figura en un buffer
        buf = io.BytesIO()
        fig.savefig(buf, format='png', facecolor='black', bbox_inches='tight', dpi=100)
        buf.seek(0)
        
        # Cargar la imagen con PIL y convertir a array NumPy
        pil_image = Image.open(buf)
        image_array = np.array(pil_image)
        
        # Convertir RGBA a BGR si es necesario
        if image_array.shape[2] == 4:  # RGBA
            image_array = cv2.cvtColor(image_array, cv2.COLOR_RGBA2BGR)
        elif image_array.shape[2] == 3:  # RGB
            image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
        
        # Redimensionar si es necesario
        if image_array.shape[1] != width or image_array.shape[0] != height:
            image_array = cv2.resize(image_array, (width, height))
        
        plt.close(fig)
        buf.close()
        return image_array
    
    def _update_detection_log(self, detections: List[Dict], true_animal: str):
        """
        Actualiza el log de detecciones.
        
        Args:
            detections: Lista de detecciones actuales
            true_animal: Animal real
        """
        timestamp = time.strftime("%H:%M:%S")
        correct_detections = sum(1 for d in detections if d['is_correct'])
        
        log_entry = {
            'timestamp': timestamp,
            'true_animal': true_animal,
            'detections': detections,
            'correct_detections': correct_detections,
            'total_detections': len(detections)
        }
        
        self.detection_log.append(log_entry)
        
        # Mantener solo las últimas 50 entradas para evitar uso excesivo de memoria
        if len(self.detection_log) > 50:
            self.detection_log = self.detection_log[-50:]
    
    def start_analysis(self):
        """Inicia el análisis con YOLO y streaming de imágenes."""
        if self.is_running:
            print("El análisis ya está en curso")
            return
        
        self.is_running = True
        
        # Crear ventana
        cv2.namedWindow(self.window_name, cv2.WINDOW_AUTOSIZE)
        
        # Iniciar streaming de imágenes
        self.image_streamer.start_streaming()
        
        print("Análisis YOLO iniciado.")
        print("CONTROLES:")
        print("- Presiona 'q' en la ventana para salir")
        print("- También puedes usar Ctrl+C en la consola")
        print("-" * 40)
        
        # Loop principal de visualización
        while self.is_running and self.image_streamer.is_active():
            if self.display_image is not None:
                cv2.imshow(self.window_name, self.display_image)
            
            # Verificar tecla presionada (waitKey con timeout corto)
            key = cv2.waitKey(30) & 0xFF  # 30ms timeout para mejor responsividad
            
            # Salir si se presiona 'q' o 'Q' o Escape
            if key == ord('q') or key == ord('Q') or key == 27:  # 27 es ESC
                print("\nSaliendo del programa por solicitud del usuario...")
                break
            
            # Verificar si la ventana fue cerrada
            try:
                # Intentar obtener propiedades de la ventana
                if cv2.getWindowProperty(self.window_name, cv2.WND_PROP_VISIBLE) < 1:
                    print("\nVentana cerrada, terminando programa...")
                    break
            except cv2.error:
                # La ventana fue cerrada
                print("\nVentana cerrada, terminando programa...")
                break
                
            time.sleep(0.01)  # Pequeña pausa para evitar uso excesivo de CPU
        
        # Asegurar que se detenga el streaming
        self.stop_analysis()
        
    
    def stop_analysis(self):
        """Detiene el análisis y limpia recursos."""
        if not self.is_running:
            return  # Ya está detenido
            
        print("Deteniendo análisis...")
        self.is_running = False
        
        # Detener el streaming de imágenes
        if hasattr(self, 'image_streamer'):
            self.image_streamer.stop_streaming()
        
        # Cerrar todas las ventanas de OpenCV
        try:
            cv2.destroyAllWindows()
            # Dar tiempo para que las ventanas se cierren
            cv2.waitKey(1)
        except:
            pass
            
        print("Análisis detenido exitosamente")
    
    def get_statistics(self) -> Dict:
        """
        Retorna estadísticas del análisis.
        
        Returns:
            Diccionario con estadísticas
        """
        if not self.detection_log:
            return {}
        
        total_images = len(self.detection_log)
        total_correct = sum(entry['correct_detections'] > 0 for entry in self.detection_log)
        total_detections = sum(entry['total_detections'] for entry in self.detection_log)
        
        return {
            'total_images_processed': total_images,
            'images_with_correct_detection': total_correct,
            'accuracy': (total_correct / total_images * 100) if total_images > 0 else 0,
            'total_detections': total_detections,
            'average_detections_per_image': (total_detections / total_images) if total_images > 0 else 0
        }


if __name__ == "__main__":
    try:
        # Crear analizador YOLO
        analyzer = YoloAnalyzer(
            model_path="yolov8n.pt",  # Modelo nano (más rápido)
            images_dir="imgs",
            max_images=15,
            interval_seconds=1.0,
            confidence_threshold=0.3
        )
        
        # Iniciar análisis
        analyzer.start_analysis()
        
        # Mostrar estadísticas finales
        stats = analyzer.get_statistics()
        if stats:
            print("\n=== ESTADÍSTICAS FINALES ===")
            print(f"Imágenes procesadas: {stats['total_images_processed']}")
            print(f"Detecciones correctas: {stats['images_with_correct_detection']}")
            print(f"Precisión: {stats['accuracy']:.1f}%")
            print(f"Total detecciones: {stats['total_detections']}")
            print(f"Promedio detecciones/imagen: {stats['average_detections_per_image']:.1f}")
        
    except KeyboardInterrupt:
        print("\nDeteniendo análisis...")
        if 'analyzer' in locals():
            analyzer.stop_analysis()
    except Exception as e:
        print(f"Error: {e}")
