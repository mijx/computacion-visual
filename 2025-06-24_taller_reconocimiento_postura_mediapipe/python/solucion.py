import cv2
import mediapipe as mp
import numpy as np

# Inicializar MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Inicializar captura de video
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    
    if not ret:
        print("No se pudo leer el frame.")
        break
    
    # Convertir el frame a RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Realizar detección de postura
    results = pose.process(frame_rgb)
    
    # Dibujar los puntos clave del cuerpo
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
        # Obtener coordenadas de puntos clave importantes (por ejemplo, hombros, muñecas)
        landmarks = results.pose_landmarks.landmark
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
        left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE]
        right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE]
        
        # Condiciones lógicas para detectar acciones
        if left_wrist.y < left_shoulder.y and right_wrist.y < right_shoulder.y:
            action = "Levantando brazos"
        elif left_hip.y > left_knee.y and right_hip.y > right_knee.y:
            action = "Sentado"
        elif abs(left_hip.y - right_hip.y) < 0.05 and abs(left_knee.y - right_knee.y) < 0.05:
            action = "Caminando"
        else:
            action = "Accion no reconocida"
        
        # Mostrar el nombre de la acción en la pantalla
        cv2.putText(frame, f"Acción: {action}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    
    # Mostrar la imagen con la detección de postura
    cv2.imshow("Reconocimiento de Postura", frame)
    
    if cv2.waitKey(1) & 0xFF == 27:  # Salir con la tecla ESC
        break

cap.release()
cv2.destroyAllWindows()
