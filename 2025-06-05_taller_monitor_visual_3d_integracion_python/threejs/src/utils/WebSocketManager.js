/**
 * Clase para manejar la conexión WebSocket y sus eventos
 */
class WebSocketManager {
    constructor(url = 'ws://localhost:8080/ws') {
        this.url = url;
        this.ws = null;
        this.isConnected = false;
        this.callbacks = {
            onPeopleCount: null,
            onConnectionChange: null
        };

        // Vincular métodos al contexto de la clase
        this.connect = this.connect.bind(this);
        this.disconnect = this.disconnect.bind(this);
        this.handleMessage = this.handleMessage.bind(this);
    }

    /**
     * Inicia la conexión WebSocket
     * @returns {boolean} - true si se inició la conexión, false si ya existe una
     */
    connect() {
        // Si ya hay una conexión activa, no hacer nada
        if (this.ws && (this.ws.readyState === WebSocket.CONNECTING || this.ws.readyState === WebSocket.OPEN)) {
            console.log('Ya existe una conexión WebSocket activa');
            return false;
        }

        try {
            console.log('Iniciando conexión WebSocket...');
            this.ws = new WebSocket(this.url);

            this.ws.onopen = () => {
                console.log('Conexión WebSocket establecida');
                this.isConnected = true;
                if (this.callbacks.onConnectionChange) {
                    this.callbacks.onConnectionChange(true);
                }
            };

            this.ws.onclose = () => {
                console.log('Conexión WebSocket cerrada');
                this.isConnected = false;
                if (this.callbacks.onConnectionChange) {
                    this.callbacks.onConnectionChange(false);
                }
            };

            this.ws.onerror = (error) => {
                console.error('Error en WebSocket:', error);
                this.isConnected = false;
                if (this.callbacks.onConnectionChange) {
                    this.callbacks.onConnectionChange(false);
                }
            };

            this.ws.onmessage = this.handleMessage;
            return true;

        } catch (error) {
            console.error('Error al crear WebSocket:', error);
            this.isConnected = false;
            if (this.callbacks.onConnectionChange) {
                this.callbacks.onConnectionChange(false);
            }
            return false;
        }
    }

    /**
     * Maneja los mensajes recibidos del servidor
     */
    handleMessage(event) {
        try {
            const data = JSON.parse(event.data);
            
            // Si recibimos el conteo de personas y hay un callback registrado
            if ('people_count' in data && this.callbacks.onPeopleCount) {
                this.callbacks.onPeopleCount(data.people_count);
            }
        } catch (error) {
            console.error('Error al procesar mensaje:', error);
        }
    }

    /**
     * Cierra la conexión WebSocket de forma limpia
     */
    disconnect() {
        if (this.ws) {
            console.log('Cerrando conexión WebSocket...');
            this.ws.close();
            this.ws = null;
            this.isConnected = false;
            if (this.callbacks.onConnectionChange) {
                this.callbacks.onConnectionChange(false);
            }
        }
    }

    /**
     * Registra un callback para recibir actualizaciones del conteo de personas
     */
    onPeopleCount(callback) {
        this.callbacks.onPeopleCount = callback;
    }

    /**
     * Registra un callback para recibir cambios en el estado de la conexión
     */
    onConnectionChange(callback) {
        this.callbacks.onConnectionChange = callback;
    }
}

export default WebSocketManager; 