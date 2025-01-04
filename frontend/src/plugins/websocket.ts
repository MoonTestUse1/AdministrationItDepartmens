import { ref } from 'vue'

class WebSocketClient {
  private socket: WebSocket | null = null
  private reconnectAttempts = 0
  private maxReconnectAttempts = 5
  private reconnectTimeout = 3000
  private messageHandlers: ((data: any) => void)[] = []
  private currentType: 'admin' | 'employee' | null = null
  private currentId: number | undefined = undefined

  // Состояние подключения
  isConnected = ref(false)

  connect(type: 'admin' | 'employee', id?: number) {
    this.currentType = type
    this.currentId = id
    
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const baseUrl = `${protocol}//${window.location.host}`
    const url = type === 'admin' ? 
      `${baseUrl}/api/requests/ws/admin` : 
      `${baseUrl}/api/requests/ws/employee/${id}`

    console.log('Connecting to WebSocket:', url)
    
    if (this.socket) {
      console.log('Closing existing connection')
      this.socket.close()
    }

    this.socket = new WebSocket(url)

    this.socket.onopen = () => {
      console.log('WebSocket connected')
      this.isConnected.value = true
      this.reconnectAttempts = 0
    }

    this.socket.onmessage = (event) => {
      console.log('WebSocket message received:', event.data)
      try {
        const data = JSON.parse(event.data)
        this.messageHandlers.forEach(handler => handler(data))
      } catch (error) {
        console.error('Error parsing WebSocket message:', error)
      }
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
    if (this.reconnectAttempts < this.maxReconnectAttempts && this.currentType) {
      this.reconnectAttempts++
      console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})`)
      setTimeout(() => {
        this.connect(this.currentType!, this.currentId)
      }, this.reconnectTimeout * this.reconnectAttempts)
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
    this.currentType = null
    this.currentId = undefined
    this.isConnected.value = false
  }
}

export const wsClient = new WebSocketClient() 