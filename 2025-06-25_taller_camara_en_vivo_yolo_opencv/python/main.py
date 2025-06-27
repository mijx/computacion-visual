import cv2
import numpy as np
from ultralytics import YOLO
import time
import os
import tkinter as tk
from tkinter import ttk, scrolledtext
from PIL import Image, ImageTk
import threading
from queue import Queue

class VideoProcessorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🧪 Taller: Cámara en Vivo - YOLO y OpenCV")
        self.root.geometry("1280x720")
        self.root.resizable(False, False)
        
        self.cap = None
        self.model = None
        self.current_filter = 'original'
        self.is_paused = False
        self.object_count = {}
        self.frame_count = 0
        self.is_running = False
        
        self.log_queue = Queue()
        self.setup_gui()
        self.setup_camera()
        self.setup_yolo()
    
    def configure_dark_theme(self):
        # Configurar colores del tema oscuro
        self.colors = {
            'bg_primary': '#1e1e1e',      # Fondo principal
            'bg_secondary': '#2d2d2d',    # Fondo secundario
            'bg_accent': '#3d3d3d',       # Acentos
            'text_primary': '#ffffff',    # Texto principal
            'text_secondary': '#b0b0b0',  # Texto secundario
            'accent_green': '#00ff41',    # Verde neón
            'accent_blue': '#00b4d8',     # Azul moderno
            'accent_orange': '#ff6b35',   # Naranja vibrante
            'button_hover': '#404040'     # Hover de botones
        }
        
        # Configurar el root con tema oscuro
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Configurar estilo para ttk widgets
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configurar estilos personalizados con nombres correctos
        self.style.configure('DarkLabelFrame.TLabelframe', 
                           background=self.colors['bg_secondary'], 
                           bordercolor=self.colors['accent_green'],
                           darkcolor=self.colors['bg_accent'],
                           lightcolor=self.colors['bg_accent'],
                           borderwidth=2)
        
        self.style.configure('DarkLabelFrame.TLabelframe.Label', 
                           background=self.colors['bg_secondary'], 
                           foreground=self.colors['accent_green'], 
                           font=('Arial', 10, 'bold'))
        
        self.style.configure('DarkButton.TButton', 
                           background=self.colors['bg_accent'],
                           foreground=self.colors['text_primary'],
                           borderwidth=1,
                           focuscolor='none',
                           font=('Arial', 9, 'bold'))
        
        self.style.map('DarkButton.TButton',
                      background=[('active', self.colors['button_hover']),
                                ('pressed', self.colors['accent_blue'])])
        
        self.style.configure('DarkRadio.TRadiobutton',
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['text_secondary'],
                           font=('Arial', 8),
                           focuscolor='none')
        
        self.style.map('DarkRadio.TRadiobutton',
                      foreground=[('selected', self.colors['accent_blue']),
                                ('active', self.colors['text_primary'])])
    
    def setup_gui(self):
        # Configurar tema oscuro
        self.configure_dark_theme()
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#1e1e1e')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Fila 1: Videos (2 columnas)
        video_frame = tk.Frame(main_frame, bg=self.colors['bg_primary'])
        video_frame.pack(fill=tk.BOTH, expand=True)
        
        # Video Original
        self.original_frame = ttk.LabelFrame(video_frame, text="📹 Video Original", 
                                           padding=5, style='DarkLabelFrame.TLabelframe')
        self.original_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.original_label = tk.Label(self.original_frame, bg=self.colors['bg_secondary'], 
                                     text="Cámara no iniciada", fg=self.colors['text_secondary'],
                                     font=('Arial', 12))
        self.original_label.pack(expand=True)
        
        # Video Procesado
        self.processed_frame = ttk.LabelFrame(video_frame, text="🎨 Video Procesado", 
                                            padding=5, style='DarkLabelFrame.TLabelframe')
        self.processed_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.processed_label = tk.Label(self.processed_frame, bg=self.colors['bg_secondary'], 
                                      text="Procesamiento inactivo", fg=self.colors['text_secondary'],
                                      font=('Arial', 12))
        self.processed_label.pack(expand=True)
        
        # Fila 2: Consola y controles
        console_frame = ttk.LabelFrame(main_frame, text="💻 Consola y Controles", 
                                     padding=5, style='DarkLabelFrame.TLabelframe')
        console_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Panel de controles
        controls_frame = tk.Frame(console_frame, bg=self.colors['bg_secondary'])
        controls_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Información de estado
        status_frame = tk.Frame(controls_frame, bg=self.colors['bg_secondary'])
        status_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.status_label = tk.Label(status_frame, text="Filtro: original | Frame: 0 | Estado: Iniciando...",
                                   bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                                   font=('Arial', 10, 'bold'))
        self.status_label.pack(anchor=tk.W, pady=2)
        
        self.objects_label = tk.Label(status_frame, text="Objetos detectados: Ninguno",
                                    bg=self.colors['bg_secondary'], fg=self.colors['accent_green'],
                                    font=('Arial', 9))
        self.objects_label.pack(anchor=tk.W)
        
        # Botones de control
        buttons_frame = tk.Frame(controls_frame, bg=self.colors['bg_secondary'])
        buttons_frame.pack(side=tk.RIGHT)
        
        ttk.Button(buttons_frame, text="▶️ Iniciar", command=self.start_video, 
                  style='DarkButton.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(buttons_frame, text="⏸️ Pausar", command=self.toggle_pause, 
                  style='DarkButton.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(buttons_frame, text="📷 Capturar", command=self.capture_frame, 
                  style='DarkButton.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(buttons_frame, text="❓ Ayuda", command=self.show_help, 
                  style='DarkButton.TButton').pack(side=tk.LEFT, padx=2)
        
        # Filtros disponibles
        filters_frame = tk.Frame(controls_frame, bg=self.colors['bg_secondary'])
        filters_frame.pack(side=tk.RIGHT, padx=(10, 0))
        
        tk.Label(filters_frame, text="Filtros:", bg=self.colors['bg_secondary'], 
                fg=self.colors['accent_blue'], font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=(0, 5))
        
        self.filter_var = tk.StringVar(value="original")
        filters = [
            ("Original", "original"),
            ("Grises", "grayscale"),
            ("Binario", "binary"),
            ("Bordes", "edges"),
            ("Blur", "blur"),
            ("YOLO", "yolo")
        ]
        
        for text, value in filters:
            ttk.Radiobutton(filters_frame, text=text, variable=self.filter_var, 
                          value=value, command=self.change_filter, 
                          style='DarkRadio.TRadiobutton').pack(side=tk.LEFT, padx=2)
        
        # Área de consola mejorada
        self.console = scrolledtext.ScrolledText(console_frame, height=8, width=80, 
                                               bg=self.colors['bg_accent'], 
                                               fg=self.colors['accent_green'], 
                                               font=("Consolas", 10),
                                               insertbackground=self.colors['accent_green'],
                                               selectbackground=self.colors['accent_blue'],
                                               selectforeground=self.colors['text_primary'],
                                               wrap=tk.WORD)
        self.console.pack(fill=tk.BOTH, expand=True)
        
        # Configurar eventos de teclado
        self.root.bind('<Key>', self.on_key_press)
        self.root.focus_set()
        
        self.log("🚀 Interfaz gráfica inicializada")
        self.log("📝 Usa los botones o las teclas para controlar la aplicación")
        
    def setup_camera(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("No se pudo acceder a la cámara")
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
    def setup_yolo(self):
        try:
            self.model = YOLO('yolov8n.pt')
            self.log("✅ Modelo YOLOv8 cargado exitosamente")
        except Exception as e:
            self.log(f"❌ Error cargando modelo YOLO: {e}")
            self.log("📥 Descargando modelo YOLOv8...")
            self.model = YOLO('yolov8n.pt')
    
    def log(self, message):
        timestamp = time.strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        def update_console():
            self.console.insert(tk.END, log_message)
            self.console.see(tk.END)
        
        if hasattr(self, 'console'):
            self.root.after(0, update_console)
        else:
            print(log_message.strip())
    
    def start_video(self):
        if not self.is_running:
            self.is_running = True
            self.video_thread = threading.Thread(target=self.video_loop, daemon=True)
            self.video_thread.start()
            self.log("▶️ Video iniciado")
    
    def toggle_pause(self):
        self.is_paused = not self.is_paused
        status = "pausado" if self.is_paused else "reanudado"
        self.log(f"⏸️ Video {status}")
    
    def change_filter(self):
        self.current_filter = self.filter_var.get()
        self.log(f"🎨 Filtro cambiado a: {self.current_filter}")
    
    def capture_frame(self):
        if hasattr(self, 'current_frame') and self.current_frame is not None:
            processed = self.process_frame(self.current_frame)
            timestamp = int(time.time())
            filename = f"capture_{self.current_filter}_{timestamp}.jpg"
            cv2.imwrite(filename, processed)
            self.log(f"📷 Imagen guardada: {filename}")
    
    def on_key_press(self, event):
        key = event.char.lower()
        
        if key == 'g':
            self.filter_var.set('grayscale')
            self.change_filter()
        elif key == 'b':
            self.filter_var.set('binary')
            self.change_filter()
        elif key == 'e':
            self.filter_var.set('edges')
            self.change_filter()
        elif key == 'l':
            self.filter_var.set('blur')
            self.change_filter()
        elif key == 'o':
            self.filter_var.set('original')
            self.change_filter()
        elif key == 'y':
            self.filter_var.set('yolo')
            self.change_filter()
        elif key == 'p':
            self.toggle_pause()
        elif key == 's':
            self.capture_frame()
        elif key == 'h':
            self.show_help()
        elif key == 'q':
            self.cleanup()
    
    def apply_grayscale_filter(self, frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    def apply_binary_filter(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        return binary
    
    def apply_edge_detection(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        return edges
    
    def apply_blur_filter(self, frame):
        return cv2.GaussianBlur(frame, (15, 15), 0)
    
    def detect_objects(self, frame):
        if self.model is None:
            return frame
            
        results = self.model(frame, verbose=False)
        annotated_frame = frame.copy()
        current_objects = {}
        
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    confidence = float(box.conf[0])
                    class_id = int(box.cls[0])
                    class_name = self.model.names[class_id]
                    
                    if confidence > 0.5:
                        current_objects[class_name] = current_objects.get(class_name, 0) + 1
                        
                        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        
                        label = f"{class_name}: {confidence:.2f}"
                        label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
                        cv2.rectangle(annotated_frame, (x1, y1 - label_size[1] - 10), 
                                    (x1 + label_size[0], y1), (0, 255, 0), -1)
                        cv2.putText(annotated_frame, label, (x1, y1 - 5), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        
        self.object_count = current_objects
        return annotated_frame
    
    def update_status_labels(self):
        # Actualizar etiqueta de estado
        status_text = f"Filtro: {self.current_filter} | Frame: {self.frame_count} | Estado: {'Pausado' if self.is_paused else 'Ejecutando'}"
        self.status_label.config(text=status_text)
        
        # Actualizar etiqueta de objetos
        if self.object_count:
            objects_text = "Objetos detectados: " + ", ".join([f"{obj}: {count}" for obj, count in self.object_count.items()])
        else:
            objects_text = "Objetos detectados: Ninguno"
        self.objects_label.config(text=objects_text)
    
    def show_help(self):
        self.log("═══════════════════════════════════════")
        self.log("📖 CONTROLES DISPONIBLES:")
        self.log("═══════════════════════════════════════")
        self.log("🎨 FILTROS:")
        self.log("  'g' - Filtro escala de grises")
        self.log("  'b' - Filtro binario")
        self.log("  'e' - Detección de bordes")
        self.log("  'l' - Filtro blur")
        self.log("  'o' - Frame original")
        self.log("  'y' - Detección YOLO")
        self.log("🎮 CONTROLES:")
        self.log("  'p' - Pausar/Reanudar")
        self.log("  's' - Capturar imagen")
        self.log("  'h' - Mostrar ayuda")
        self.log("  'q' - Salir")
        self.log("💡 También puedes usar los botones y controles de la interfaz")
        self.log("═══════════════════════════════════════")
    
    def save_frame(self, frame, filter_name):
        timestamp = int(time.time())
        filename = f"capture_{filter_name}_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Imagen guardada como: {filename}")
    
    def process_frame(self, frame):
        if self.current_filter == 'grayscale':
            processed = self.apply_grayscale_filter(frame)
            processed = cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR)
        elif self.current_filter == 'binary':
            processed = self.apply_binary_filter(frame)
            processed = cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR)
        elif self.current_filter == 'edges':
            processed = self.apply_edge_detection(frame)
            processed = cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR)
        elif self.current_filter == 'blur':
            processed = self.apply_blur_filter(frame)
        elif self.current_filter == 'yolo':
            processed = self.detect_objects(frame)
        else:
            processed = frame.copy()
        
        return processed
    
    def video_loop(self):
        self.log("🎥 Bucle de video iniciado")
        
        while self.is_running:
            if not self.is_paused:
                if self.cap is None:
                    self.log("❌ Error: Cámara no inicializada")
                    break
                    
                ret, frame = self.cap.read()
                if not ret:
                    self.log("❌ Error: No se pudo leer el frame")
                    break
                
                self.frame_count += 1
                frame = cv2.flip(frame, 1)  # Efecto espejo
                self.current_frame = frame
                
                processed_frame = self.process_frame(frame)
                
                # Convertir frames para tkinter
                original_image = self.cv2_to_tkinter(frame)
                processed_image = self.cv2_to_tkinter(processed_frame)
                
                # Actualizar GUI en thread principal
                self.root.after(0, self.update_video_display, original_image, processed_image)
                
            time.sleep(0.03)  # ~30 FPS
    
    def cv2_to_tkinter(self, cv_img):
        # Redimensionar para ajustarse a la interfaz
        height, width = cv_img.shape[:2]
        max_width, max_height = 600, 350
        
        scale = min(max_width/width, max_height/height)
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        resized = cv2.resize(cv_img, (new_width, new_height))
        
        # Convertir de BGR a RGB si es necesario
        if len(resized.shape) == 3:
            resized = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        
        # Convertir a PIL y luego a ImageTk
        pil_image = Image.fromarray(resized)
        return ImageTk.PhotoImage(pil_image)
    
    def update_video_display(self, original_image, processed_image):
        self.original_label.config(image=original_image)
        self.original_label.image = original_image  # Mantener referencia
        
        self.processed_label.config(image=processed_image)
        self.processed_label.image = processed_image  # Mantener referencia
        
        self.update_status_labels()
    
    def run(self):
        self.log("🚀 Iniciando aplicación...")
        self.log("📝 Presiona '▶️ Iniciar' o usa las teclas para controlar")
        
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.log("⚠️ Interrupción del usuario detectada")
        finally:
            self.cleanup()
    
    def cleanup(self):
        self.is_running = False
        if self.cap:
            self.cap.release()
        self.log("🔧 Recursos liberados")
        self.root.quit()
        self.root.destroy()

def main():
    try:
        processor = VideoProcessorGUI()
        processor.run()
    except KeyboardInterrupt:
        print("\nInterrupción del usuario detectada")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main() 