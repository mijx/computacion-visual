import cv2
import numpy as np
import mediapipe as mp
import speech_recognition as sr
import threading
import time
import os

# --- Configuración Inicial ---

# Colores (BGR)
COLOR_PALETTE = {
    "rojo": (0, 0, 255),
    "verde": (0, 255, 0),
    "azul": (255, 0, 0),
    "amarillo": (0, 255, 255),
    "blanco": (255, 255, 255)
}
DEFAULT_COLOR = COLOR_PALETTE["blanco"]
current_color = DEFAULT_COLOR
brush_size = 15
is_drawing_mode = True 

# Lienzo
canvas = np.zeros((720, 1280, 3), dtype=np.uint8)

# Creación de la carpeta 'obras' si no existe
if not os.path.exists("../obras"):
    os.makedirs("../obras")

# --- Reconocimiento de Voz (en un hilo separado) ---
def voice_recognizer():
    global current_color, is_drawing_mode, canvas
    r = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        r.adjust_for_ambient_noise(source)

    print("🎤 Escuchando comandos de voz...")

    while True:
        try:
            with mic as source:
                audio = r.listen(source, timeout=5, phrase_time_limit=3)
            
            command = r.recognize_google(audio, language="es-ES").lower()
            print(f"Comando reconocido: '{command}'")

            if "limpiar" in command:
                canvas = np.zeros((720, 1280, 3), dtype=np.uint8)
                print("Lienzo limpiado.")
            
            elif "guardar" in command:
                filename = f"../obras/obra_{time.strftime('%Y%m%d_%H%M%S')}.png"
                cv2.imwrite(filename, canvas)
                print(f"Obra guardada como {filename}")

            elif "pincel" in command:
                is_drawing_mode = True
                print("Modo: Pincel activado")

            elif "borrador" in command:
                is_drawing_mode = False
                print("Modo: Borrador activado")

            else:
                for color_name, color_val in COLOR_PALETTE.items():
                    if color_name in command:
                        current_color = color_val
                        print(f"Color cambiado a {color_name}")
                        break

        except sr.UnknownValueError:
            pass # Ignorar si no se entiende el audio
        except sr.RequestError as e:
            print(f"Error en el servicio de reconocimiento; {e}")
        except sr.WaitTimeoutError:
            pass # No pasa nada si no se detecta voz


# --- Detección de Manos y Dibujo ---
def hand_drawing():
    global canvas

    # Inicializar MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    )
    mp_draw = mp.solutions.drawing_utils

    # Iniciar captura de video
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: No se puede abrir la cámara.")
        return

    cap.set(3, 1280)
    cap.set(4, 720)

    prev_pos = None

    print("✍️  Mueve tu dedo índice para dibujar. Cierra el puño para pausar.")
    print("Presiona 'q' para salir.")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            continue

        # Voltear la imagen para efecto espejo
        frame = cv2.flip(frame, 1)
        
        # Procesar con MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]

            # Dibujar esqueleto de la mano
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Obtener coordenadas del dedo índice (landmark 8)
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            h, w, _ = frame.shape
            cx, cy = int(index_finger_tip.x * w), int(index_finger_tip.y * h)

            # Usar el gesto de "dedos juntos" (índice y corazón) para activar/desactivar
            middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            dist_x = abs(index_finger_tip.x - middle_finger_tip.x)
            dist_y = abs(index_finger_tip.y - middle_finger_tip.y)
            is_active = (dist_x < 0.05 and dist_y < 0.05)

            if is_active:
                draw_color = current_color if is_drawing_mode else (0, 0, 0)
                
                if prev_pos is None:
                    prev_pos = (cx, cy)

                cv2.line(canvas, prev_pos, (cx, cy), draw_color, brush_size)
                prev_pos = (cx, cy)
            else:
                prev_pos = None
        else:
            prev_pos = None

        # Combinar el lienzo con la imagen de la cámara
        # Se usa una máscara para que el negro del lienzo sea transparente
        gray_canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
        _, inv_mask = cv2.threshold(gray_canvas, 1, 255, cv2.THRESH_BINARY_INV)
        frame_bg = cv2.bitwise_and(frame, frame, mask=inv_mask)
        canvas_fg = cv2.bitwise_and(canvas, canvas, mask=~inv_mask)
        combined_view = cv2.add(frame_bg, canvas)

        cv2.imshow("Pintura Interactiva con Voz y Gestos", combined_view)

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    os._exit(0) # Forzar la salida para detener el hilo de voz

if __name__ == "__main__":
    # Iniciar el hilo de reconocimiento de voz
    voice_thread = threading.Thread(target=voice_recognizer, daemon=True)
    voice_thread.start()

    # Iniciar la detección de manos y el bucle principal de dibujo
    hand_drawing() 