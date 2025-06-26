from ultralytics import YOLO
import cv2
import asyncio
import json
from aiohttp import web
import threading
import sys

# --- Estado Compartido y Control de Apagado ---
ws_connections = []
loop = None
server_ready = threading.Event()
# Evento central para coordinar un apagado limpio desde cualquier hilo
shutdown_event = threading.Event()

# --- Configuración de la Ventana de Video ---
WINDOW_NAME = "Detección de Personas - Presiona 'q' para salir"
INITIAL_WINDOW_WIDTH = 1280  # Ancho inicial de la ventana

def create_resizable_window():
    """Crea una ventana redimensionable con propiedades personalizadas."""
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    # Permitir que la ventana sea redimensionable
    cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_ASPECT_RATIO, cv2.WINDOW_KEEPRATIO)
    cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_TOPMOST, 1)

def resize_frame(frame, target_width):
    """Redimensiona el frame manteniendo la proporción de aspecto."""
    height, width = frame.shape[:2]
    aspect_ratio = width / height
    target_height = int(target_width / aspect_ratio)
    return cv2.resize(frame, (target_width, target_height))

# --- Lógica de aiohttp y WebSocket ---

async def websocket_handler(request):
    """Maneja las conexiones WebSocket entrantes."""
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    ws_connections.append(ws)
    print("Cliente WebSocket conectado.")
    
    try:
        # Mantenemos la conexión abierta, revisando periódicamente si debemos apagar.
        while not shutdown_event.is_set():
            try:
                # Esperamos mensajes con un timeout para no bloquear el bucle.
                await ws.receive(timeout=1.0)
            except asyncio.TimeoutError:
                continue
    finally:
        if ws in ws_connections:
            ws_connections.remove(ws)
        print("Cliente WebSocket desconectado.")
    return ws

async def broadcast_people_count(count):
    """Envía el conteo de personas a todos los clientes WebSocket conectados."""
    if ws_connections and not shutdown_event.is_set():
        data = json.dumps({"people_count": count})
        # Preparamos tareas para enviar a todos los clientes concurrentemente.
        tasks = [ws.send_str(data) for ws in ws_connections]
        await asyncio.gather(*tasks, return_exceptions=True)

async def shutdown_handler(request):
    """Maneja la petición HTTP para apagar el servidor y el procesamiento."""
    print("Petición de apagado recibida por HTTP. Iniciando cierre...")
    shutdown_event.set()
    # Programamos la detención del loop para que esta respuesta pueda ser enviada.
    asyncio.create_task(stop_server_loop_soon())
    return web.Response(text="El servidor se está apagando...")

async def stop_server_loop_soon():
    """Espera un segundo y luego detiene el event loop del servidor."""
    await asyncio.sleep(1)
    if loop and loop.is_running():
        loop.stop()

def run_web_server():
    """Configura y ejecuta el servidor web aiohttp."""
    global loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    app = web.Application()
    app.router.add_get('/ws', websocket_handler)
    app.router.add_get('/shutdown', shutdown_handler)  # Nueva ruta para apagar
    
    runner = web.AppRunner(app)
    loop.run_until_complete(runner.setup())
    site = web.TCPSite(runner, 'localhost', 8080)
    loop.run_until_complete(site.start())
    
    print("\n" + "="*50)
    print("Servidor WebSocket iniciado en ws://localhost:8080/ws")
    print("FORMAS DE APAGAR LA APLICACIÓN:")
    print("1. Visita http://localhost:8080/shutdown en tu navegador.")
    print("2. Presiona la tecla 'q' en la ventana de video.")
    print("3. Presiona Ctrl+C en esta terminal.")
    print("="*50 + "\n")
    server_ready.set()
    
    # El loop se ejecuta hasta que loop.stop() es llamado
    loop.run_forever()
    
    print("Limpiando y deteniendo el servidor web...")
    loop.run_until_complete(runner.cleanup())
    loop.close()
    print("Servidor web detenido.")

# --- Lógica de OpenCV y YOLO ---

def process_video():
    """Procesa el video, detecta personas y se comunica con el servidor."""
    server_ready.wait()
    model = YOLO("yolov8n.pt")
    video = cv2.VideoCapture("people_walking.mp4")

    if not video.isOpened():
        print("Error: No se pudo abrir el archivo de video.")
        shutdown_event.set()
        return

    
    try:
        while not shutdown_event.is_set():
            ret, frame = video.read()
            if not ret:
                print("Fin del video.")
                break
            
            results = model.predict(frame, classes=0, conf=0.5, verbose=False)
            amnt_people = len(results[0].boxes)
            print(f"Personas detectadas: {amnt_people}", end='\r')

            if loop and not loop.is_closed():
                asyncio.run_coroutine_threadsafe(broadcast_people_count(amnt_people), loop)
            
            annotated_frame = results[0].plot()
            resized_frame = resize_frame(annotated_frame, INITIAL_WINDOW_WIDTH)
            
            cv2.imshow(WINDOW_NAME, resized_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("\nSe presionó 'q'. Iniciando apagado.")
                break
    finally:
        print("\nDeteniendo procesamiento de video...")
        video.release()
        cv2.destroyAllWindows()
        # Aseguramos que el evento de apagado se active para notificar al otro hilo.
        shutdown_event.set()
        # Detenemos el loop del servidor de forma segura desde este hilo.
        if loop and loop.is_running():
            loop.call_soon_threadsafe(loop.stop)

# --- Ejecución Principal ---

if __name__ == "__main__":
    server_thread = threading.Thread(target=run_web_server, daemon=True)
    server_thread.start()

    try:
        process_video()
    except KeyboardInterrupt:
        print("\nProcesamiento interrumpido por el usuario (Ctrl+C).")
    finally:
        shutdown_event.set()
        if server_thread.is_alive():
            server_thread.join(timeout=5)
        print("Aplicación finalizada.")
        # Limpieza final para asegurar que la terminal quede limpia.
        sys.stdout.write("\n")
        sys.stdout.flush()