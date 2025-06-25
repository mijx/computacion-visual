import asyncio
import websockets
import json
import random

async def handler(websocket):
    """
    Maneja la conexión WebSocket, enviando datos aleatorios al cliente
    cada 0.5 segundos.
    """
    print(f"Cliente conectado: {websocket.remote_address}")
    try:
        while True:
            data = {
                "x": random.uniform(-5, 5),
                "y": random.uniform(-5, 5),
                "color": random.choice(["red", "green", "blue"])
            }
            await websocket.send(json.dumps(data))
            await asyncio.sleep(0.5)
    except websockets.exceptions.ConnectionClosedOK:
        print(f"Cliente desconectado: {websocket.remote_address}")
    except Exception as e:
        print(f"Error en el handler: {e}")

async def main():
    """
    Inicializa el servidor WebSocket.
    """
    print("Servidor WebSocket iniciado en ws://localhost:8765")
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future() # Mantener el servidor corriendo indefinidamente

if __name__ == "__main__":
    asyncio.run(main())