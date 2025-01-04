import { ref } from 'vue'

class WebSocketClient {
  private socket: WebSocket | null = null
  private reconnectAttempts = 0
  private maxReconnectAttempts = 5
  private reconnectTimeout = 3000
  private messageHandlers: ((data: any) => void)[] = []

  // Состояние подключения
  isConnected = ref(false)

  connect(type: 'admin' | 'employee', id?: number) {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const baseUrl = `${protocol}//${window.location.host}`
    const url = type === 'admin' ? 
      `${baseUrl}/api/requests/ws/admin` : 
      `${baseUrl}/api/requests/ws/employee/${id}`

    this.socket = new WebSocket(url)

    this.socket.onopen = () => {
      console.log('WebSocket connected')
      this.isConnected.value = true
      this.reconnectAttempts = 0
    }

    this.socket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      this.messageHandlers.forEach(handler => handler(data))
    }

    this.socket.onclose = () => {
      console.log('WebSocket disconnected')
      this.isConnected.value = false
      this.tryReconnect()
    }

    this.socket.onerror = (error) => {
      console.error('WebSocket error:', error)
      this.isConnected.value = false
    }
  }

  private tryReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++
      setTimeout(() => {
        console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})`)
        this.connect('admin')
      }, this.reconnectTimeout)
    }
  }

  addMessageHandler(handler: (data: any) => void) {
    this.messageHandlers.push(handler)
  }

  removeMessageHandler(handler: (data: any) => void) {
    const index = this.messageHandlers.indexOf(handler)
    if (index > -1) {
      this.messageHandlers.splice(index, 1)
    }
  }

  disconnect() {
    if (this.socket) {
      this.socket.close()
      this.socket = null
    }
  }
}

export const wsClient = new WebSocketClient() 