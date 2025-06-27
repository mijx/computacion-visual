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
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class YOLODetectorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎯 YOLO Real-Time Object Detection - Webcam")
        self.root.geometry("1400x900")
        self.root.resizable(True, True)
        
        # Variables principales
        self.cap = None
        self.model = None
        self.is_running = False
        self.is_paused = False
        
        # Configuración de detección
        self.confidence_threshold = 0.5
        self.selected_classes = set()
        self.all_classes = []
        
        # Estadísticas
        self.frame_count = 0
        self.fps_history = []
        self.detection_stats = defaultdict(int)
        self.total_detections = 0
        
        # Threading
        self.log_queue = Queue()
        self.video_thread = None
        
        self.setup_gui()
        self.setup_camera()
        self.setup_yolo()
        
    def configure_dark_theme(self):
        """Configurar tema oscuro moderno"""
        self.colors = {
            'bg_primary': '#1e1e1e',      # Fondo principal
            'bg_secondary': '#2d2d2d',    # Fondo secundario
            'bg_accent': '#3d3d3d',       # Acentos
            'bg_card': '#2d2d2d',         # Tarjetas (igual que bg_secondary)
            'text_primary': '#ffffff',    # Texto principal
            'text_secondary': '#b0b0b0',  # Texto secundario
            'accent_green': '#00ff41',    # Verde neón
            'accent_blue': '#00b4d8',     # Azul moderno
            'accent_orange': '#ff6b35',   # Naranja vibrante
            'accent_red': '#da3633',      # Rojo
            'border': '#30363d',          # Bordes
            'button_hover': '#404040'     # Hover de botones
        }
        
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Configurar estilo TTK
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Estilos personalizados usando el patrón del taller anterior
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
        
        self.style.configure('DarkCheckbutton.TCheckbutton',
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['text_secondary'],
                           font=('Arial', 8),
                           focuscolor='none')
        
        self.style.map('DarkCheckbutton.TCheckbutton',
                      foreground=[('active', self.colors['text_primary'])])
        
        # Configurar Scale con el estilo por defecto
        self.style.configure('TScale',
                           background=self.colors['bg_secondary'],
                           troughcolor=self.colors['bg_accent'],
                           borderwidth=0)
    
    def setup_gui(self):
        """Configurar interfaz gráfica moderna"""
        self.configure_dark_theme()
        
        # Frame principal con padding
        main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Título principal
        title_frame = tk.Frame(main_frame, bg=self.colors['bg_primary'])
        title_frame.pack(fill=tk.X, pady=(0, 15))
        
        title_label = tk.Label(title_frame, 
                              text="🎯 YOLO Real-Time Object Detection",
                              font=('Segoe UI', 18, 'bold'),
                              bg=self.colors['bg_primary'], 
                              fg=self.colors['text_primary'])
        title_label.pack()
        
        # Layout principal: video + controles
        content_frame = tk.Frame(main_frame, bg=self.colors['bg_primary'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Panel izquierdo: Video
        video_panel = ttk.LabelFrame(content_frame, text="📹 Live Detection Feed", 
                                   padding=10, style='DarkLabelFrame.TLabelframe')
        video_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.video_label = tk.Label(video_panel, 
                                  bg=self.colors['bg_card'], 
                                  text="Cámara no iniciada\nPresiona 'Iniciar Detección'",
                                  fg=self.colors['text_secondary'],
                                  font=('Segoe UI', 14))
        self.video_label.pack(expand=True, fill=tk.BOTH)
        
        # Panel derecho: Controles y estadísticas
        control_panel = tk.Frame(content_frame, bg=self.colors['bg_primary'], width=400)
        control_panel.pack(side=tk.RIGHT, fill=tk.Y)
        control_panel.pack_propagate(False)
        
        # Controles principales
        self.setup_main_controls(control_panel)
        
        # Configuración de detección
        self.setup_detection_config(control_panel)
        
        # Estadísticas
        self.setup_statistics_panel(control_panel)
        
        # Consola de logs
        self.setup_console(main_frame)
        
        # Eventos de teclado
        self.root.bind('<Key>', self.on_key_press)
        self.root.focus_set()
        
        self.log("🚀 Interfaz YOLO inicializada")
        
    def setup_main_controls(self, parent):
        """Configurar controles principales"""
        controls_frame = ttk.LabelFrame(parent, text="🎮 Controles Principales", 
                                      padding=10, style='DarkLabelFrame.TLabelframe')
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Estado actual
        self.status_label = tk.Label(controls_frame, 
                                   text="Estado: Listo para iniciar",
                                   bg=self.colors['bg_secondary'], 
                                   fg=self.colors['text_primary'],
                                   font=('Segoe UI', 10, 'bold'))
        self.status_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Botones principales
        buttons_frame = tk.Frame(controls_frame, bg=self.colors['bg_secondary'])
        buttons_frame.pack(fill=tk.X)
        
        self.start_btn = ttk.Button(buttons_frame, text="▶️ Iniciar Detección", 
                                  command=self.start_detection, style='DarkButton.TButton')
        self.start_btn.pack(fill=tk.X, pady=2)
        
        self.pause_btn = ttk.Button(buttons_frame, text="⏸️ Pausar", 
                                  command=self.toggle_pause, style='DarkButton.TButton')
        self.pause_btn.pack(fill=tk.X, pady=2)
        
        self.capture_btn = ttk.Button(buttons_frame, text="📷 Capturar Frame", 
                                    command=self.capture_frame, style='DarkButton.TButton')
        self.capture_btn.pack(fill=tk.X, pady=2)
        
        # Métricas en tiempo real
        metrics_frame = tk.Frame(controls_frame, bg=self.colors['bg_secondary'])
        metrics_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.fps_label = tk.Label(metrics_frame, text="FPS: 0.0", 
                                bg=self.colors['bg_secondary'], 
                                fg=self.colors['accent_green'],
                                font=('Segoe UI', 12, 'bold'))
        self.fps_label.pack(anchor=tk.W)
        
        self.detections_label = tk.Label(metrics_frame, text="Detecciones: 0", 
                                       bg=self.colors['bg_secondary'], 
                                       fg=self.colors['accent_blue'],
                                       font=('Segoe UI', 10))
        self.detections_label.pack(anchor=tk.W)
        
    def setup_detection_config(self, parent):
        """Configurar parámetros de detección"""
        config_frame = ttk.LabelFrame(parent, text="⚙️ Configuración de Detección", 
                                    padding=10, style='DarkLabelFrame.TLabelframe')
        config_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Umbral de confianza
        conf_frame = tk.Frame(config_frame, bg=self.colors['bg_secondary'])
        conf_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(conf_frame, text="Umbral de Confianza:", 
                bg=self.colors['bg_secondary'], fg=self.colors['text_secondary'],
                font=('Segoe UI', 9)).pack(anchor=tk.W)
        
        self.confidence_var = tk.DoubleVar(value=0.5)
        self.confidence_scale = ttk.Scale(conf_frame, from_=0.1, to=0.9, 
                                        variable=self.confidence_var,
                                        orient=tk.HORIZONTAL,
                                        command=self.update_confidence)
        self.confidence_scale.pack(fill=tk.X, pady=2)
        
        self.confidence_label = tk.Label(conf_frame, text="50%", 
                                       bg=self.colors['bg_secondary'], 
                                       fg=self.colors['accent_orange'],
                                       font=('Segoe UI', 9, 'bold'))
        self.confidence_label.pack(anchor=tk.W)
        
        # Filtro de clases
        classes_frame = tk.Frame(config_frame, bg=self.colors['bg_secondary'])
        classes_frame.pack(fill=tk.X)
        
        tk.Label(classes_frame, text="Filtrar por Clases:", 
                bg=self.colors['bg_secondary'], fg=self.colors['text_secondary'],
                font=('Segoe UI', 9)).pack(anchor=tk.W, pady=(0, 5))
        
        # Frame scrollable para checkboxes
        self.classes_canvas = tk.Canvas(classes_frame, height=120, 
                                      bg=self.colors['bg_card'], 
                                      highlightthickness=0)
        self.classes_scrollbar = ttk.Scrollbar(classes_frame, orient="vertical", 
                                             command=self.classes_canvas.yview)
        self.classes_scrollable = tk.Frame(self.classes_canvas, bg=self.colors['bg_card'])
        
        self.classes_canvas.configure(yscrollcommand=self.classes_scrollbar.set)
        self.classes_canvas.pack(side="left", fill="both", expand=True)
        self.classes_scrollbar.pack(side="right", fill="y")
        
        self.classes_canvas.create_window((0, 0), window=self.classes_scrollable, anchor="nw")
        
    def setup_statistics_panel(self, parent):
        """Configurar panel de estadísticas"""
        stats_frame = ttk.LabelFrame(parent, text="📊 Estadísticas de Detección", 
                                   padding=10, style='DarkLabelFrame.TLabelframe')
        stats_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Gráfica de FPS
        self.fig = Figure(figsize=(4, 2), dpi=80, facecolor=self.colors['bg_secondary'])
        self.ax = self.fig.add_subplot(111, facecolor=self.colors['bg_card'])
        self.ax.set_title("FPS en Tiempo Real", color=self.colors['text_primary'], fontsize=10)
        self.ax.set_xlabel("Frames", color=self.colors['text_secondary'], fontsize=8)
        self.ax.set_ylabel("FPS", color=self.colors['text_secondary'], fontsize=8)
        self.ax.tick_params(colors=self.colors['text_secondary'], labelsize=8)
        
        self.canvas = FigureCanvasTkAgg(self.fig, stats_frame)
        self.canvas.get_tk_widget().pack(fill=tk.X, pady=(0, 10))
        
        # Lista de objetos detectados
        self.stats_text = scrolledtext.ScrolledText(stats_frame, height=8, 
                                                  bg=self.colors['bg_card'], 
                                                  fg=self.colors['text_primary'], 
                                                  font=("Consolas", 9),
                                                  insertbackground=self.colors['text_primary'])
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        
    def setup_console(self, parent):
        """Configurar consola de logs"""
        console_frame = ttk.LabelFrame(parent, text="💻 Consola de Sistema", 
                                     padding=10, style='DarkLabelFrame.TLabelframe')
        console_frame.pack(fill=tk.X, pady=(15, 0))
        
        self.console = scrolledtext.ScrolledText(console_frame, height=6, 
                                               bg=self.colors['bg_card'], 
                                               fg=self.colors['accent_green'], 
                                               font=("Consolas", 9),
                                               insertbackground=self.colors['accent_green'],
                                               selectbackground=self.colors['accent_blue'])
        self.console.pack(fill=tk.BOTH)
        
    def setup_camera(self):
        """Configurar cámara"""
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                raise RuntimeError("No se pudo acceder a la cámara")
            
            # Configurar resolución
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            self.log("✅ Cámara inicializada correctamente")
            
        except Exception as e:
            self.log(f"❌ Error al inicializar cámara: {str(e)}")
            
    def setup_yolo(self):
        """Configurar modelo YOLO"""
        try:
            self.log("🔄 Cargando modelo YOLOv8...")
            self.model = YOLO('yolov8n.pt')
            self.all_classes = list(self.model.names.values())
            self.setup_class_checkboxes()
            self.log("✅ Modelo YOLO cargado exitosamente")
            
        except Exception as e:
            self.log(f"❌ Error al cargar YOLO: {str(e)}")
            
    def setup_class_checkboxes(self):
        """Crear checkboxes para filtro de clases"""
        if not self.all_classes:
            return
            
        # Limpiar frame anterior
        for widget in self.classes_scrollable.winfo_children():
            widget.destroy()
            
        # Variables para checkboxes
        self.class_vars = {}
        
        # Clases populares al inicio
        popular_classes = ['person', 'car', 'truck', 'bus', 'bicycle', 'motorcycle', 
                          'cell phone', 'laptop', 'book', 'bottle', 'cup', 'chair']
        
        # Crear checkboxes
        for i, class_name in enumerate(self.all_classes):
            var = tk.BooleanVar(value=class_name in popular_classes)
            self.class_vars[class_name] = var
            
            if var.get():
                self.selected_classes.add(class_name)
            
            cb = ttk.Checkbutton(self.classes_scrollable, text=class_name, 
                               variable=var, command=self.update_class_filter,
                               style='DarkCheckbutton.TCheckbutton')
            cb.pack(anchor=tk.W, padx=5, pady=1)
            
        # Actualizar scroll region
        self.classes_scrollable.update_idletasks()
        self.classes_canvas.configure(scrollregion=self.classes_canvas.bbox("all"))
        
    def update_confidence(self, value):
        """Actualizar umbral de confianza"""
        self.confidence_threshold = float(value)
        self.confidence_label.config(text=f"{int(self.confidence_threshold * 100)}%")
        
    def update_class_filter(self):
        """Actualizar filtro de clases"""
        self.selected_classes.clear()
        for class_name, var in self.class_vars.items():
            if var.get():
                self.selected_classes.add(class_name)
        
        self.log(f"🔍 Filtro actualizado: {len(self.selected_classes)} clases seleccionadas")
        
    def start_detection(self):
        """Iniciar detección"""
        if not self.is_running and self.cap and self.model:
            self.is_running = True
            self.is_paused = False
            self.video_thread = threading.Thread(target=self.detection_loop)
            self.video_thread.daemon = True
            self.video_thread.start()
            
            self.start_btn.config(text="🔄 Detectando...", state='disabled')
            self.status_label.config(text="Estado: Detectando objetos...")
            self.log("▶️ Detección iniciada")
            
    def toggle_pause(self):
        """Alternar pausa"""
        if self.is_running:
            self.is_paused = not self.is_paused
            status = "pausado" if self.is_paused else "detectando"
            self.pause_btn.config(text="▶️ Continuar" if self.is_paused else "⏸️ Pausar")
            self.status_label.config(text=f"Estado: {status.capitalize()}")
            self.log(f"⏸️ Detección {'pausada' if self.is_paused else 'reanudada'}")
            
    def capture_frame(self):
        """Capturar frame actual"""
        if hasattr(self, 'current_frame') and self.current_frame is not None:
            timestamp = int(time.time())
            filename = f"capture_yolo_{timestamp}.jpg"
            cv2.imwrite(filename, self.current_frame)
            self.log(f"📷 Frame capturado: {filename}")
            
    def on_key_press(self, event):
        """Manejar eventos de teclado"""
        key = event.keysym.lower()
        
        if key == 's':
            self.start_detection()
        elif key == 'p':
            self.toggle_pause()
        elif key == 'c':
            self.capture_frame()
        elif key == 'q':
            self.cleanup()
            self.root.quit()
            
    def detect_objects(self, frame):
        """Detectar objetos con YOLO"""
        if self.model is None:
            return frame, {}
            
        try:
            start_time = time.time()
            results = self.model(frame, verbose=False, conf=self.confidence_threshold)
            inference_time = time.time() - start_time
            
            annotated_frame = frame.copy()
            current_detections = defaultdict(int)
            
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        confidence = float(box.conf[0])
                        class_id = int(box.cls[0])
                        class_name = self.model.names[class_id]
                        
                        # Filtrar por clases seleccionadas
                        if self.selected_classes and class_name not in self.selected_classes:
                            continue
                            
                        current_detections[class_name] += 1
                        
                        # Dibujar bounding box
                        color = self.get_class_color(class_name)
                        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
                        
                        # Etiqueta con fondo
                        label = f"{class_name}: {confidence:.2f}"
                        label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
                        cv2.rectangle(annotated_frame, (x1, y1 - label_size[1] - 10), 
                                    (x1 + label_size[0], y1), color, -1)
                        cv2.putText(annotated_frame, label, (x1, y1 - 5), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Calcular FPS
            fps = 1.0 / inference_time if inference_time > 0 else 0
            
            # Mostrar información en el frame
            info_text = f"FPS: {fps:.1f} | Objetos: {sum(current_detections.values())}"
            cv2.putText(annotated_frame, info_text, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            return annotated_frame, current_detections
            
        except Exception as e:
            self.log(f"❌ Error en detección: {str(e)}")
            return frame, {}
            
    def get_class_color(self, class_name):
        """Obtener color único para cada clase"""
        colors = [
            (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
            (255, 0, 255), (0, 255, 255), (128, 0, 128), (255, 165, 0),
            (255, 192, 203), (128, 128, 128), (0, 128, 0), (128, 0, 0)
        ]
        return colors[hash(class_name) % len(colors)]
        
    def detection_loop(self):
        """Loop principal de detección"""
        fps_counter = 0
        fps_start_time = time.time()
        
        while self.is_running:
            if self.is_paused:
                time.sleep(0.1)
                continue
                
            ret, frame = self.cap.read()
            if not ret:
                continue
                
            self.current_frame = frame.copy()
            
            # Procesar frame
            processed_frame, detections = self.detect_objects(frame)
            
            # Actualizar estadísticas
            self.update_detection_stats(detections)
            
            # Calcular FPS promedio
            fps_counter += 1
            if fps_counter >= 10:  # Cada 10 frames
                elapsed = time.time() - fps_start_time
                avg_fps = fps_counter / elapsed
                self.fps_history.append(avg_fps)
                if len(self.fps_history) > 50:
                    self.fps_history.pop(0)
                    
                fps_counter = 0
                fps_start_time = time.time()
                
                # Actualizar GUI
                self.root.after(0, self.update_gui_stats, avg_fps, detections)
            
            # Mostrar frame
            try:
                tk_image = self.cv2_to_tkinter(processed_frame)
                self.root.after(0, self.update_video_display, tk_image)
            except Exception as e:
                self.log(f"❌ Error actualizando display: {str(e)}")
                
            self.frame_count += 1
            
    def update_detection_stats(self, current_detections):
        """Actualizar estadísticas de detección"""
        for class_name, count in current_detections.items():
            self.detection_stats[class_name] += count
            self.total_detections += count
            
    def update_gui_stats(self, fps, current_detections):
        """Actualizar estadísticas en GUI"""
        # Actualizar labels
        self.fps_label.config(text=f"FPS: {fps:.1f}")
        self.detections_label.config(text=f"Detecciones: {sum(current_detections.values())}")
        
        # Actualizar gráfica de FPS
        if self.fps_history:
            self.ax.clear()
            self.ax.plot(self.fps_history, color=self.colors['accent_green'], linewidth=2)
            self.ax.set_title("FPS en Tiempo Real", color=self.colors['text_primary'], fontsize=10)
            self.ax.set_facecolor(self.colors['bg_card'])
            self.ax.tick_params(colors=self.colors['text_secondary'], labelsize=8)
            self.canvas.draw()
            
        # Actualizar texto de estadísticas
        stats_text = "Objetos detectados por clase:\n" + "-" * 30 + "\n"
        sorted_stats = sorted(self.detection_stats.items(), key=lambda x: x[1], reverse=True)
        
        for class_name, count in sorted_stats[:10]:  # Top 10
            stats_text += f"{class_name:15}: {count:4d}\n"
            
        stats_text += "-" * 30 + f"\nTotal detecciones: {self.total_detections}"
        
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats_text)
        
    def cv2_to_tkinter(self, cv_img):
        """Convertir imagen OpenCV a Tkinter"""
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        # Redimensionar para ajustar al espacio disponible
        height, width = cv_img.shape[:2]
        max_width, max_height = 800, 600
        
        if width > max_width or height > max_height:
            scale = min(max_width/width, max_height/height)
            new_width = int(width * scale)
            new_height = int(height * scale)
            cv_img = cv2.resize(cv_img, (new_width, new_height))
            
        img_pil = Image.fromarray(cv_img)
        return ImageTk.PhotoImage(img_pil)
        
    def update_video_display(self, tk_image):
        """Actualizar display de video"""
        self.video_label.config(image=tk_image, text="")
        self.video_label.image = tk_image
        
    def log(self, message):
        """Agregar mensaje a consola"""
        timestamp = time.strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        self.log_queue.put(log_message)
        
        def update_console():
            try:
                while not self.log_queue.empty():
                    message = self.log_queue.get_nowait()
                    self.console.insert(tk.END, message)
                    self.console.see(tk.END)
            except:
                pass
            self.root.after(100, update_console)
            
        self.root.after(0, update_console)
        
    def cleanup(self):
        """Limpiar recursos"""
        self.is_running = False
        if self.cap:
            self.cap.release()
        self.log("🧹 Recursos liberados")
        
    def run(self):
        """Ejecutar aplicación"""
        self.root.protocol("WM_DELETE_WINDOW", lambda: (self.cleanup(), self.root.quit()))
        self.root.mainloop()

def main():
    """Función principal"""
    try:
        app = YOLODetectorGUI()
        app.run()
    except Exception as e:
        print(f"Error fatal: {str(e)}")
        
if __name__ == "__main__":
    main() 