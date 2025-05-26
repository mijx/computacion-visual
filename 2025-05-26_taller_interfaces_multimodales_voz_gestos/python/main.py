import cv2
import pygame
import numpy as np
import threading
import speech_recognition as sr
import pyttsx3
import time

# Inicializar pygame
pygame.init()
pantalla = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Control de Cuadro con Voz y Gestos")

# Sintetizador de voz
voz = pyttsx3.init()
def hablar(texto):
    voz.say(texto)
    voz.runAndWait()

# Variables del cuadro
cuadro_visible = True
color = (255, 255, 255)
angulo = 0

# Gesto actual detectado
gesto_actual = None

# Comandos reconocidos
ultimo_comando = None

# Lock para sincronización
estado_lock = threading.Lock()

# Función para detectar voz
def escuchar():
    global ultimo_comando
    reconocedor = sr.Recognizer()
    microfono = sr.Microphone()
    with microfono as source:
        reconocedor.adjust_for_ambient_noise(source)
    while True:
        with microfono as source:
            print("Escuchando...")
            try:
                audio = reconocedor.listen(source, timeout=5)
                comando = reconocedor.recognize_google(audio, language="es-ES").lower()
                print("Comando detectado:", comando)
                with estado_lock:
                    ultimo_comando = comando
            except Exception as e:
                print("No se entendió el comando:", e)

# Función para procesar cámara y detectar movimientos
zona_actual = None
def detectar_movimiento():
    global gesto_actual, zona_actual
    camara = cv2.VideoCapture(0)
    _, frame_anterior = camara.read()
    frame_anterior = cv2.cvtColor(frame_anterior, cv2.COLOR_BGR2GRAY)
    frame_anterior = cv2.GaussianBlur(frame_anterior, (21, 21), 0)

    tiempo_ultimo_gesto = 0
    intervalo_gesto = 2  # segundos

    while True:
        _, frame = camara.read()
        gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gris = cv2.GaussianBlur(gris, (21, 21), 0)

        frame_diff = cv2.absdiff(frame_anterior, gris)
        _, thresh = cv2.threshold(frame_diff, 15, 255, cv2.THRESH_BINARY)

        height, width = thresh.shape
        zona_ancho = width // 3

        zonas = {
            'izquierda': (0, zona_ancho),
            'centro': (zona_ancho, 2 * zona_ancho),
            'derecha': (2 * zona_ancho, width)
        }

        gesto_detectado = None
        tiempo_actual = time.time()

        for zona, (x1, x2) in zonas.items():
            sub_frame = thresh[:, x1:x2]
            movimiento = np.sum(sub_frame)
            if movimiento > 1000000 and (tiempo_actual - tiempo_ultimo_gesto) > intervalo_gesto:
                print(f"Movimiento detectado en la zona: {zona}")
                if zona == 'centro':
                    gesto_detectado = 'mano_abierta'
                elif zona == 'izquierda':
                    gesto_detectado = 'puno'
                elif zona == 'derecha':
                    gesto_detectado = 'v'
                tiempo_ultimo_gesto = tiempo_actual
                break

        with estado_lock:
            if gesto_detectado:
                gesto_actual = gesto_detectado

        frame_anterior = gris
        cv2.imshow("Camara", thresh)
        if cv2.waitKey(1) == 27:
            break
    camara.release()
    cv2.destroyAllWindows()

# Hilos de detección de voz y movimiento
threading.Thread(target=escuchar, daemon=True).start()
threading.Thread(target=detectar_movimiento, daemon=True).start()

# Bucle principal visual
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont(None, 36)

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()

    pantalla.fill((0, 0, 0))

    with estado_lock:
        comando = ultimo_comando
        gesto = gesto_actual
        ultimo_comando = None  # Limpiar después de usar

    if comando and gesto:
        if gesto == 'mano_abierta':
            if comando in ['rojo', 'azul', 'verde', 'amarillo']:
                colores = {
                    'rojo': (255, 0, 0),
                    'azul': (0, 0, 255),
                    'verde': (0, 255, 0),
                    'amarillo': (255, 255, 0)
                }
                color = colores[comando]
                hablar(f"Color cambiado a {comando}")
        elif gesto == 'puno':
            if comando == 'rotar':
                angulo = (angulo + 30) % 360
                hablar("Rotando 30 grados")
        elif gesto == 'v':
            if comando == 'ocultar':
                cuadro_visible = False
                hablar("Ocultando figura")
            elif comando == 'mostrar':
                cuadro_visible = True
                hablar("Mostrando figura")

    if cuadro_visible:
        superficie = pygame.Surface((100, 100), pygame.SRCALPHA)
        pygame.draw.rect(superficie, color, (0, 0, 100, 100))
        superficie_rotada = pygame.transform.rotate(superficie, angulo)
        rect = superficie_rotada.get_rect(center=(300, 300))
        pantalla.blit(superficie_rotada, rect)

    # Mostrar el gesto en pantalla
    texto_gesto = fuente.render(f"Gesto: {gesto if gesto else 'Ninguno'}", True, (255, 255, 255))
    pantalla.blit(texto_gesto, (10, 10))

    pygame.display.flip()
    reloj.tick(30)
