class WebSocketClient {
  private ws: WebSocket | null = null;
  private messageHandlers: ((data: any) => void)[] = [];
  private reconnectTimeout: number | null = null;
  public isConnected: boolean = false;

  connect(role: string) {
    if (this.ws) {
      this.ws.close();
    }

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/api/ws/${role}`;
    
    this.ws = new WebSocket(wsUrl);

    this.ws.onopen = () => {
      console.log('WebSocket connected');
      this.isConnected = true;
    };

    this.ws.onclose = () => {
      console.log('WebSocket disconnected');
      this.isConnected = false;
      
      // Попытка переподключения через 3 секунды
      if (this.reconnectTimeout === null) {
        this.reconnectTimeout = window.setTimeout(() => {
          this.reconnectTimeout = null;
          this.connect(role);
        }, 3000);
      }
    };

    this.ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        this.messageHandlers.forEach(handler => handler(data));
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    if (this.reconnectTimeout !== null) {
      clearTimeout(this.reconnectTimeout);
      this.reconnectTimeout = null;
    }
  }

  addMessageHandler(handler: (data: any) => void) {
    this.messageHandlers.push(handler);
  }

  removeMessageHandler(handler: (data: any) => void) {
    this.messageHandlers = this.messageHandlers.filter(h => h !== handler);
  }
}

export const wsClient = new WebSocketClient(); 