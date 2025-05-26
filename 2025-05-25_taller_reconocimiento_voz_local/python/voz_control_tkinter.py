import speech_recognition as sr
import pyttsx3
import tkinter as tk
from threading import Thread

# Diccionario de comandos
comandos = {
    "rojo": "#ff0000",
    "verde": "#00ff00",
    "azul": "#0000ff",
    "amarillo": "#ffff00",
    "blanco": "#ffffff",
    "negro": "#000000",
    "detener": "detener",
    "iniciar": "iniciar"
}

# Inicializar reconocimiento y motor de voz
r = sr.Recognizer()
mic = sr.Microphone()
voz = pyttsx3.init()
voz.setProperty('rate', 150)
voz.setProperty('voice', 'spanish')  # Puede que no funcione si no hay una voz en español instalada

# Crear ventana
ventana = tk.Tk()
ventana.title("Control por voz")
ventana.geometry("400x300")
ventana.configure(bg="white")

estado_lbl = tk.Label(ventana, text="Presiona el botón y habla", font=("Arial", 14))
estado_lbl.pack(pady=20)

def hablar(texto):
    voz.say(texto)
    voz.runAndWait()

def procesar_comando(texto):
    texto = texto.lower()
    print("Comando detectado:", texto)
    if texto in comandos:
        accion = comandos[texto]
        if accion.startswith("#"):
            ventana.configure(bg=accion)
            estado_lbl.config(text=f"Color: {texto}")
            hablar(f"Cambiando a color {texto}")
        elif accion == "detener":
            estado_lbl.config(text="Comando: detener")
            hablar("Deteniendo")
        elif accion == "iniciar":
            estado_lbl.config(text="Comando: iniciar")
            hablar("Iniciando")
    else:
        estado_lbl.config(text="Comando no reconocido")
        hablar("No entendí el comando")

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
    hilo = Thread(target=escuchar)
    hilo.start()

btn = tk.Button(ventana, text="Hablar", font=("Arial", 12), command=escuchar_en_hilo)
btn.pack(pady=10)

ventana.mainloop()
