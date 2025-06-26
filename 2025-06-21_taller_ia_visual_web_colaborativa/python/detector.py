import cv2
import json
import requests
import os
from ultralytics import YOLO

# --- Configuración ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(SCRIPT_DIR, "input_image.jpg")
MODEL_DIR = os.path.join(SCRIPT_DIR, "..", "modelo")
MODEL_PATH = os.path.join(MODEL_DIR, "yolov8n.pt")
MODEL_URL = "https://github.com/ultralytics/assets/releases/download/v8.1.0/yolov8n.pt"

# El taller pide que los resultados esten en una carpeta 'resultados' en la raiz del taller.
# Desde 'python/' el path relativo es '../resultados/'
OUTPUT_IMAGE_PATH = os.path.join(SCRIPT_DIR, "..", "resultados", "deteccion.png")
OUTPUT_JSON_PATH = os.path.join(SCRIPT_DIR, "..", "resultados", "results.json")

# --- 1. Detección de objetos con YOLO ---
def detect_objects():
    print("Preparando entorno...")
    # Crear el directorio para el modelo si no existe
    os.makedirs(MODEL_DIR, exist_ok=True)

    # Si el modelo está en el directorio principal, moverlo a la carpeta 'modelo'
    original_model_path_in_root = os.path.join(SCRIPT_DIR, "yolov8n.pt")
    if os.path.exists(original_model_path_in_root) and not os.path.exists(MODEL_PATH):
        print(f"Moviendo modelo a '{MODEL_DIR}'...")
        os.rename(original_model_path_in_root, MODEL_PATH)

    # --- Descargar el modelo si no existe ---
    if not os.path.exists(MODEL_PATH):
        print(f"Modelo no encontrado en '{MODEL_PATH}'. Descargando...")
        try:
            response = requests.get(MODEL_URL, stream=True)
            response.raise_for_status()  # Lanza una excepción para respuestas con error (4xx o 5xx)
            with open(MODEL_PATH, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print("Descarga del modelo completada.")
        except requests.exceptions.RequestException as e:
            print(f"Error al descargar el modelo: {e}")
            exit()

    print("Cargando modelo YOLOv8...")
    model = YOLO(MODEL_PATH)  # Cargar el modelo desde la carpeta 'modelo'

    print(f"Cargando imagen desde {IMAGE_PATH}...")
    img = cv2.imread(IMAGE_PATH)
    if img is None:
        print(f"Error al cargar la imagen en '{IMAGE_PATH}'.")
        print("Asegúrate de que el archivo 'input_image.jpg' existe en la misma carpeta que el script.")
        exit()

    print("Realizando detección de objetos...")
    results = model(img)[0]  # Obtener resultados de la detección

    detections = []
    # Iterar sobre las detecciones
    for box in results.boxes:
        # Extraer coordenadas del bounding box
        x1, y1, x2, y2 = [int(coord) for coord in box.xyxy[0]]
        confidence = float(box.conf[0])
        class_id = int(box.cls[0])
        class_name = results.names[class_id]

        # Filtrar por confianza para mejores resultados
        if confidence > 0.5:
            # Dibujar caja y etiqueta en la imagen
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f"{class_name}: {confidence:.2f}"
            cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Guardar datos para el JSON
            detections.append({
                "class": class_name,
                "confidence": confidence,
                "box": [x1, y1, x2-x1, y2-y1] # formato [x, y, w, h]
            })

    # --- 2. Guardar resultados ---
    print(f"Guardando imagen anotada en {OUTPUT_IMAGE_PATH}...")
    # Asegurarse que el directorio de salida exista
    os.makedirs(os.path.dirname(OUTPUT_IMAGE_PATH), exist_ok=True)
    cv2.imwrite(OUTPUT_IMAGE_PATH, img)

    print(f"Guardando detecciones en {OUTPUT_JSON_PATH}...")
    with open(OUTPUT_JSON_PATH, 'w') as f:
        json.dump({"objects": detections}, f, indent=2)

    print("Proceso completado.")

if __name__ == "__main__":
    detect_objects() 