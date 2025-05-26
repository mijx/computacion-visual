import speech_recognition as sr
import pyttsx3
import tkinter as tk
from threading import Thread
import math

# --- Configuración de voz ---
voz = pyttsx3.init()
voz.setProperty('rate', 150)
voz.setProperty('voice', 'spanish')

# --- Reconocimiento de voz ---
r = sr.Recognizer()
mic = sr.Microphone()

# --- Diccionario de colores y comandos ---
colores = {
    "rojo": "red",
    "verde": "green",
    "azul": "blue",
    "amarillo": "yellow",
    "negro": "black",
    "blanco": "white"
}

# --- Variables del triángulo ---
color_actual = "blue"
angulo_actual = 0  # en grados

# --- Interfaz ---
ventana = tk.Tk()
ventana.title("Control por Voz - Triángulo")
ventana.geometry("500x500")

canvas = tk.Canvas(ventana, width=400, height=400, bg="white")
canvas.pack(pady=10)

estado_lbl = tk.Label(ventana, text="Presiona el botón y habla", font=("Arial", 14))
estado_lbl.pack(pady=10)

# --- Dibujo del triángulo ---
def calcular_puntos_triangulo(cx, cy, size, angulo):
    # Calcula los tres puntos del triángulo rotado
    puntos_base = [
        (0, -size),
        (-size * math.sin(math.radians(60)), size * math.cos(math.radians(60))),
        (size * math.sin(math.radians(60)), size * math.cos(math.radians(60)))
    ]
    puntos_rotados = []
    for x, y in puntos_base:
        xr = x * math.cos(math.radians(angulo)) - y * math.sin(math.radians(angulo))
        yr = x * math.sin(math.radians(angulo)) + y * math.cos(math.radians(angulo))
        puntos_rotados.append((cx + xr, cy + yr))
    return puntos_rotados

def dibujar_triangulo():
    canvas.delete("all")
    puntos = calcular_puntos_triangulo(200, 200, 80, angulo_actual)
    canvas.create_polygon(puntos, fill=color_actual, outline="black", width=2)

dibujar_triangulo()

# --- Respuesta hablada ---
def hablar(texto):
    voz.say(texto)
    voz.runAndWait()

# --- Procesamiento del comando ---
def procesar_comando(texto):
    global color_actual, angulo_actual
    texto = texto.lower()
    print("Comando detectado:", texto)

    if texto in colores:
        color_actual = colores[texto]
        estado_lbl.config(text=f"Color cambiado a {texto}")
        hablar(f"Cambiando a color {texto}")
    elif texto == "derecha":
        angulo_actual = (angulo_actual + 30) % 360
        estado_lbl.config(text="Girando a la derecha")
        hablar("Girando a la derecha")
    elif texto == "izquierda":
        angulo_actual = (angulo_actual - 30) % 360
        estado_lbl.config(text="Girando a la izquierda")
        hablar("Girando a la izquierda")
    else:
        estado_lbl.config(text="Comando no reconocido")
        hablar("No entendí el comando")

    dibujar_triangulo()

# --- Función para escuchar en hilo ---
def escuchar():
    with mic as source:
        estado_lbl.config(text="Escuchando...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        texto = r.recognize_google(audio, language="es-ES")
        procesar_comando(texto)
    except sr.UnknownValueError:
        estado_lbl.config(text="No entendí lo que dijiste")
        hablar("No entendí lo que dijiste")
    except sr.RequestError:
        estado_lbl.config(text="Error de conexión")
        hablar("Hay un error de conexión")

def escuchar_en_hilo():
    Thread(target=escuchar).start()

# --- Botón de hablar ---
btn = tk.Button(ventana, text="Hablar", font=("Arial", 12), command=escuchar_en_hilo)
btn.pack(pady=5)

ventana.mainloop()
