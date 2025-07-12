import cv2
import mediapipe as mp
import numpy as np
import time
import math
from collections import deque

# Inicializar MediaPipe
mp_face_mesh = mp.solutions.face_mesh
mp_hands = mp.solutions.hands
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False)
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2)

# Constantes y estados
CENTER_POINT_INDEX = 168
LEFT_EYE = 33
RIGHT_EYE = 263
rotation_angle = 0
angle_history = deque(maxlen=5)
last_tilt_time = 0
tilt_cooldown = 0.8
x_history = deque(maxlen=20)
y_history = deque(maxlen=20)
timestamps = deque(maxlen=20)

mode = "inicio"
captured_photo = None
photo_taken = False
ask_continue = False
last_nod_time = 0
last_thumbs_up_time = 0
thumbs_cooldown = 2
photo_with_rect = None
rect = None

take_photo_cooldown = 3  # segundos de espera antes de capturar
photo_taken_time = 0

def get_rectangle_from_two_hands(hand_landmarks_list, image_width, image_height):
    """
    Dado landmarks de dos manos, retorna un rectángulo que encierra
    los puntos clave: índice y pulgar de ambas manos.
    """
    if len(hand_landmarks_list) != 2:
        return None

    keypoints = []

    for hand_landmarks in hand_landmarks_list:
        # Punta del índice (8) y pulgar (4)
        index_tip = hand_landmarks.landmark[8]
        thumb_tip = hand_landmarks.landmark[4]

        x1 = int(index_tip.x * image_width)
        y1 = int(index_tip.y * image_height)
        x2 = int(thumb_tip.x * image_width)
        y2 = int(thumb_tip.y * image_height)

        keypoints.append((x1, y1))
        keypoints.append((x2, y2))

    # Coordenadas del rectángulo que encierra los 4 puntos
    xs = [p[0] for p in keypoints]
    ys = [p[1] for p in keypoints]

    return min(xs), min(ys), max(xs), max(ys)

def detect_nod(x_hist, y_hist):
    if len(x_hist) < 10:
        return False

    y = np.array(y_hist, dtype=np.float32)
    y -= np.mean(y)
    y_diff = np.diff(y)
    y_zeros = np.sum(y_diff[1:] * y_diff[:-1] < 0)
    return y_zeros >= 2 and np.max(np.abs(y)) > 10

def detect_head_tilt(face_landmarks, w, h):
    left_eye = face_landmarks.landmark[LEFT_EYE]
    right_eye = face_landmarks.landmark[RIGHT_EYE]
    x1, y1 = int(left_eye.x * w), int(left_eye.y * h)
    x2, y2 = int(right_eye.x * w), int(right_eye.y * h)
    angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
    return angle

def apply_rotation(image, angle):
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(image, matrix, (w, h), flags=cv2.INTER_LINEAR)

# Función auxiliar para calcular distancia, si no la tienes ya
def calculate_distance(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2 + (point1.z - point2.z)**2)

def detect_thumb_gesture(hand_landmarks):
    landmarks = hand_landmarks.landmark

    # Puntos clave para el pulgar
    thumb_tip = landmarks[4]
    thumb_ip = landmarks[3]  # Articulación intermedia del pulgar
    thumb_mcp = landmarks[2] # Nudillo del pulgar
    wrist = landmarks[0]     # Muñeca

    # Puntos clave para otros dedos (necesarios para la flexión)
    index_tip = landmarks[8]
    index_pip = landmarks[7]
    index_mcp = landmarks[5]

    middle_tip = landmarks[12]
    middle_pip = landmarks[11]
    middle_mcp = landmarks[9]

    ring_tip = landmarks[16]
    ring_pip = landmarks[15]
    ring_mcp = landmarks[13]

    pinky_tip = landmarks[20]
    pinky_pip = landmarks[19]
    pinky_mcp = landmarks[17]

    # --- Lógica para Pulgar Arriba ("up") ---
    thumb_extended = calculate_distance(thumb_tip, thumb_mcp) > calculate_distance(thumb_ip, thumb_mcp) * 1.5
    thumb_above_reference = thumb_tip.y < index_mcp.y

    other_fingers_flexed_for_up = True # Renombramos para claridad
    finger_tips = [index_tip, middle_tip, ring_tip, pinky_tip]
    finger_mcps = [index_mcp, middle_mcp, ring_mcp, pinky_mcp]
    finger_pips = [index_pip, middle_pip, ring_pip, pinky_pip]

    for i in range(4):
        # La punta debe estar cerca de su nudillo (flexionado) Y por debajo de este.
        # Si la distancia de la punta al nudillo es "grande" O la punta está "arriba" del nudillo, no está flexionado
        if calculate_distance(finger_tips[i], finger_mcps[i]) > calculate_distance(finger_pips[i], finger_mcps[i]) * 1.2 or \
           finger_tips[i].y < finger_mcps[i].y: # Simplificado: punta.y debe ser MAYOR que nudillo.y para estar "abajo"
            other_fingers_flexed_for_up = False
            break

    if thumb_extended and thumb_above_reference and other_fingers_flexed_for_up:
        return "up"

    
    # --- Lógica para Pulgar Hacia Abajo ("down") ---
    thumb_close_to_palm_x = calculate_distance(thumb_tip, index_mcp) < calculate_distance(thumb_mcp, index_mcp) * 0.6
    thumb_y_is_low = thumb_tip.y > wrist.y

    is_thumb_down_oriented = thumb_close_to_palm_x

    other_fingers_flexed_for_down = True
    for i in range(4):
        if calculate_distance(finger_tips[i], finger_mcps[i]) > calculate_distance(finger_pips[i], finger_mcps[i]) * 1:
            other_fingers_flexed_for_down = False
            break

    if thumb_y_is_low and other_fingers_flexed_for_down:
        return "down"

    return None

def draw_rectangle_on_image_pixels(image, x1, y1, x2, y2, color=(0, 255, 0), thickness=3):
    """
    Dibuja un rectángulo directamente sobre la imagen, modificando los píxeles.
    No usa funciones de alto nivel como cv2.rectangle.
    """
    # Bordes horizontales
    image[y1:y1+thickness, x1:x2] = color  # Línea superior
    image[y2-thickness:y2, x1:x2] = color  # Línea inferior

    # Bordes verticales
    image[y1:y2, x1:x1+thickness] = color  # Línea izquierda
    image[y1:y2, x2-thickness:x2] = color  # Línea derecha

# Cámara
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results_face = face_mesh.process(frame_rgb)
    results_hands = hands.process(frame_rgb)

    if results_face.multi_face_landmarks:
        face = results_face.multi_face_landmarks[0]
        cx = int(face.landmark[CENTER_POINT_INDEX].x * w)
        cy = int(face.landmark[CENTER_POINT_INDEX].y * h)

        x_history.append(cx)
        y_history.append(cy)
        timestamps.append(time.time())

        angle = detect_head_tilt(face, w, h)
        angle_history.append(angle)

        now = time.time()

        if mode == "inicio":
            cv2.putText(frame, "Pulgar arriba para tomar foto", (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
            # Dibuja la(s) mano(s) detectada(s)
            if results_hands.multi_hand_landmarks:
                for hand_landmarks in results_hands.multi_hand_landmarks:
                    thumb_gesture = detect_thumb_gesture(hand_landmarks)
                    if thumb_gesture == "up":
                        last_thumbs_up_time = time.time()
                        photo_taken_time = time.time()
                        mode = "tomando"
                        break
                    
            cv2.imshow("Interacción Visual", frame)
        # --- Modo TOMANDO FOTO ---
        elif mode == "tomando":
            elapsed = time.time() - photo_taken_time
            countdown = take_photo_cooldown - int(elapsed)
            if countdown > 0:
                cv2.putText(frame, f"Tomando foto en {countdown}s", (50, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 200, 255), 3)
                cv2.imshow("Interacción Visual", frame)
            else:
                captured_photo = frame.copy()
                cv2.destroyWindow("Interacción Visual")
                mode = "confirmar"
        elif mode == "confirmar" and captured_photo is not None:
            combined = np.hstack((frame, captured_photo))
            cv2.putText(combined, "¿Confirmar foto? Pulgar arriba", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)
            cv2.putText(combined, "Camara", (w // 2 - 50, h - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (100, 255, 100), 2)
            cv2.putText(combined, "Foto", (w + w // 2 - 50, h - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (100, 255, 100), 2)

            cv2.imshow("Confirmar", combined)

            if results_hands.multi_hand_landmarks:
                for hand_landmarks in results_hands.multi_hand_landmarks:
                    if time.time() - last_thumbs_up_time < thumbs_cooldown:
                        break
                    if detect_thumb_gesture(hand_landmarks) == "up":
                        mode = "recortar_foto"
                        ask_continue = False
                        time.sleep(0.5)
                        last_thumbs_up_time = time.time()
                        cv2.destroyWindow("Confirmar")
                    elif detect_thumb_gesture(hand_landmarks) == "down":
                        mode = "inicio"
                        captured_photo = None
                        time.sleep(0.5)
                        last_thumbs_down_time = time.time()
                        cv2.destroyWindow("Confirmar")

        elif mode == "rotar_foto" and captured_photo is not None:
            if len(angle_history) == 5:
                delta = angle_history[-1] - angle_history[0]
                if abs(delta) > 20 and (now - last_tilt_time) > tilt_cooldown:
                    if delta > 0:
                        rotation_angle += 90
                    else:
                        rotation_angle -= 90
                    last_tilt_time = now
                else:
                    if results_hands.multi_hand_landmarks:
                        for hand_landmarks in results_hands.multi_hand_landmarks:
                            if time.time() - last_thumbs_up_time < thumbs_cooldown:
                                break

                            thumb_gesture = detect_thumb_gesture(hand_landmarks)
                            if thumb_gesture == "up":
                                photo_taken_time = time.time()
                                last_thumbs_up_time = photo_taken_time  # prevenir múltiples capturas

                                # Aplicar rotación final
                                final_image = apply_rotation(captured_photo, rotation_angle)

                                # Crear carpeta resultados/ si no existe
                                import os
                                output_dir = "resultados"
                                os.makedirs(output_dir, exist_ok=True)

                                # Guardar imagen como PNG con timestamp
                                filename = os.path.join(output_dir, f"foto_{int(photo_taken_time)}.png")
                                cv2.imwrite(filename, final_image)
                                print(f"Foto guardada en: {filename}")

                                # Cerrar todas las ventanas anteriores
                                cv2.destroyAllWindows()

                                # Mostrar imagen en una nueva ventana sin texto
                                cv2.imshow("Foto Final", final_image)

                                # Esperar hasta que el usuario cierre la ventana
                                while True:
                                    if cv2.getWindowProperty("Foto Final", cv2.WND_PROP_VISIBLE) < 1:
                                        break
                                    if cv2.waitKey(100) & 0xFF == 27:  # permitir cerrar también con ESC
                                        break

                                cv2.destroyAllWindows()
                                exit()

            rotated_photo = apply_rotation(captured_photo, rotation_angle)

            if rotated_photo.shape[0] != frame.shape[0]:
                h_frame = frame.shape[0]
                h_photo = rotated_photo.shape[0]
                diff = h_frame - h_photo

                # Calcular cuánto rellenar arriba y abajo
                top_pad = diff // 2
                bottom_pad = diff - top_pad

                # Rellenar solo en alto (vertical)
                rotated_photo = cv2.copyMakeBorder(rotated_photo, top_pad, bottom_pad, 0, 0,
                                       cv2.BORDER_CONSTANT, value=(0, 0, 0))
            combined = np.hstack((frame, rotated_photo))
            cv2.putText(combined, "Inclina cabeza para rotar foto", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)
            cv2.putText(combined, "Pulgar arriba para continuar", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)
            cv2.imshow("Interacción Visual", combined)
            key = cv2.waitKey(1) & 0xFF
            if key == 27:
                break
            continue
        elif mode == "recortar_foto" and captured_photo is not None:
            # Hacer una copia de la foto rotada para dibujar sobre ella
            # rotated_photo = apply_rotation(captured_photo, rotation_angle)
            if detect_nod(x_history, y_history) and now - last_nod_time > 1:
                x1, y1, x2, y2 = rect

                # Recortar el área dentro del rectángulo (en color)
                captured_photo = captured_photo[y1:y2, x1:x2]

                last_nod_time = now
                time.sleep(1)
                photo_taken = True
                ask_continue = True
                mode = "rotar_foto"
                continue
            rotated_photo = captured_photo
            photo_with_rect = rotated_photo.copy()
            h, w = frame.shape[:2]
            # Verificar si hay dos manos detectadas
            if results_hands.multi_hand_landmarks:

                rect = get_rectangle_from_two_hands(results_hands.multi_hand_landmarks, w, h)
                
            if rect:
                x1, y1, x2, y2 = rect

                # 1. Convertir la foto a escala de grises y luego a BGR (para poder combinarla)
                gray = cv2.cvtColor(rotated_photo, cv2.COLOR_BGR2GRAY)
                gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

                # 2. Crear máscara donde el rectángulo es blanco (color) y lo demás es negro (blanco y negro)
                mask = np.zeros_like(gray, dtype=np.uint8)
                mask[y1:y2, x1:x2] = 255  # Dentro del rectángulo

                # 3. Aplicar la máscara para mantener color en esa zona
                color_part = cv2.bitwise_and(rotated_photo, rotated_photo, mask=mask)

                # 4. Invertir la máscara y aplicar a la imagen en blanco y negro
                inv_mask = cv2.bitwise_not(mask)
                gray_part = cv2.bitwise_and(gray_bgr, gray_bgr, mask=inv_mask)

                # 5. Combinar ambas partes
                photo_with_rect = cv2.add(color_part, gray_part)



                # x1, y1, x2, y2 = rect
                # Dibujar rectángulo directamente sobre la foto
                cv2.rectangle(photo_with_rect, (x1, y1), (x2, y2), (0, 255, 0), 3)
                
                # También dibujar en la cámara como referencia
                # cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                
                # Mostrar las coordenadas
                cv2.putText(frame, f"Rect: ({x1},{y1}) - ({x2},{y2})", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
                

                # Dibujar directamente sobre la foto con píxeles
                # draw_rectangle_on_image_pixels(frame, x1, y1, x2, y2, color=(0, 255, 0), thickness=3)

                # También dibujar en la cámara como referencia
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)




            # Crear imagen combinada DESPUÉS de dibujar los rectángulos
            combined = np.hstack((frame, photo_with_rect))
            cv2.putText(combined, "Haz marco con ambas manos - Asiente con la cabeza para confirmar", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
            
            cv2.imshow("Interacción Visual", combined)
            key = cv2.waitKey(1) & 0xFF
            if key == 27:
                break
            continue

    cv2.putText(frame, f"Modo: {mode}", (30, 460), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('r'):
        mode = "inicio"
        rotation_angle = 0
        captured_photo = None
        photo_taken = False
        ask_continue = False
    elif key == 27:
        break

cap.release()
cv2.destroyAllWindows()