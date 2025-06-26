import cv2
import numpy as np
import os
import csv
from datetime import datetime
import time
from ultralytics import YOLO, settings

# --- Directorios de trabajo ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
CAPTURES_DIR = os.path.join(BASE_DIR, 'capturas')
MODEL_DIR = os.path.join(BASE_DIR, 'modelo')
LOG_FILE_PATH = os.path.join(LOGS_DIR, 'events_log.csv')
DETECTION_COOLDOWN = 5.0 # Segundos de espera para registrar un nuevo evento

# --- Inicialización ---
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(CAPTURES_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

def draw_bounding_boxes(frame, bboxes, labels, confidences):
    """
    Dibuja los cuadros delimitadores, etiquetas y confianzas en el frame.
    """
    for bbox, label, conf in zip(bboxes, labels, confidences):
        x1, y1, x2, y2 = bbox
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        text = f"{label}: {conf:.2f}"
        
        (text_width, text_height), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.rectangle(frame, (x1, y1 - text_height - 10), (x1 + text_width + 10, y1), (0, 255, 0), -1)
        cv2.putText(frame, text, (x1 + 5, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        
    return frame

# --- Aplicación Principal ---
def main():
    """
    Función principal que ejecuta el sistema de monitoreo.
    """
    # Actualizar la configuración de ultralytics para usar el directorio local de modelos
    # Esto asegura que el modelo se descargue en la carpeta correcta
    settings.update({'weights_dir': MODEL_DIR})
    
    # Cargar el modelo YOLOv8. Se descargará en MODEL_DIR si no existe.
    model = YOLO('yolov8n.pt') 
    print("Modelo cargado.")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara web.")
        return

    last_detection_time = 0
    system_status = "Iniciando..."
    
    print("Sistema de monitoreo iniciado. Presione 'q' para salir.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: No se pudo capturar el frame de la cámara.")
            break

        # Detección de objetos con YOLOv8
        results = model(frame, verbose=False)
        
        bboxes = []
        labels = []
        confs = []

        # Procesar resultados
        for result in results:
            for box in result.boxes:
                confidence = box.conf[0]
                if confidence > 0.5:
                    class_id = int(box.cls[0])
                    label = model.names[class_id]
                    
                    coords = box.xyxy[0].cpu().numpy().astype(int)
                    x1, y1, x2, y2 = coords
                    
                    bboxes.append([x1, y1, x2, y2])
                    labels.append(label)
                    confs.append(float(confidence))

        person_detected = 'person' in labels

        if person_detected:
            system_status = "¡Alerta! Persona detectada"
            current_time = time.time()
            
            # Lógica para registrar evento solo después del cooldown
            if current_time - last_detection_time > DETECTION_COOLDOWN:
                last_detection_time = current_time
                
                timestamp_dt = datetime.now()
                timestamp_str = timestamp_dt.strftime("%Y%m%d_%H%M%S")
                log_timestamp = timestamp_dt.strftime("%Y-%m-%d %H:%M:%S")

                # 1. Guardar captura de imagen
                image_filename = f'captura_{timestamp_str}.jpg'
                image_path = os.path.join(CAPTURES_DIR, image_filename)
                cv2.imwrite(image_path, frame)

                # 2. Escribir en el log
                person_conf_index = labels.index('person')
                person_conf = confs[person_conf_index]
                with open(LOG_FILE_PATH, 'a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([log_timestamp, 'Persona detectada', 'person', f"{person_conf:.2f}"])
                    writer.writerow([log_timestamp, 'Captura guardada', 'system', 'N/A'])
                
                print(f"[{log_timestamp}] Evento: Persona detectada. 'person', {person_conf:.2f}")
        else:
            system_status = "Monitoreando..."

        # Dibujar cajas delimitadoras sobre la imagen
        output_frame = draw_bounding_boxes(frame.copy(), bboxes, labels, confs)

        # --- Crear el panel de información ---
        dashboard_height = output_frame.shape[0]
        dashboard_width = 350
        dashboard = np.zeros((dashboard_height, dashboard_width, 3), dtype="uint8")
        
        # Título y estado del sistema
        cv2.putText(dashboard, "Panel de Monitoreo", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.line(dashboard, (10, 45), (340, 45), (255, 255, 255), 1)
        
        status_color = (0, 0, 255) if person_detected else (0, 255, 0)
        cv2.putText(dashboard, "Estado:", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.putText(dashboard, system_status, (70, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)

        # Contador de objetos detectados
        cv2.putText(dashboard, "Conteo de Objetos:", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        y_pos = 140
        object_counts = {l: labels.count(l) for l in set(labels)}
        if not object_counts:
            cv2.putText(dashboard, " - Ninguno", (15, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
        else:
            for obj, count in object_counts.items():
                text = f" - {obj.capitalize()}: {count}"
                cv2.putText(dashboard, text, (15, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
                y_pos += 25

        # Instrucciones
        cv2.putText(dashboard, "Presione 'q' para salir", (10, dashboard_height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)

        # Combinar la vista de la cámara y el panel
        combined_view = np.hstack((output_frame, dashboard))
        cv2.imshow('Sistema de Monitoreo Inteligente', combined_view)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()
    print("Sistema detenido.")

if __name__ == '__main__':
    # Nota: ultralytics descargará el modelo YOLOv8n en la carpeta 'modelo'
    # la primera vez que se ejecute.
    # Se requiere una conexión a internet para la descarga inicial.
    # También necesitarás instalar ultralytics y torch: pip install ultralytics torch
    main() 