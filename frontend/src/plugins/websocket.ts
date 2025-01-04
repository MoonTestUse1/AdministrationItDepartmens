import { ref } from 'vue'

class WebSocketClient {
  private socket: WebSocket | null = null
  private reconnectAttempts = 0
  private maxReconnectAttempts = 5
  private reconnectTimeout = 3000
  private messageHandlers: ((data: any) => void)[] = []
  private currentType: 'admin' | 'employee' | null = null
  private currentId: number | undefined = undefined
  private pingInterval: number | null = null

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

    console.log('WebSocket: Connecting to', url)
    
    if (this.socket) {
      console.log('WebSocket: Closing existing connection')
      this.socket.close()
      this.socket = null
      if (this.pingInterval) {
        clearInterval(this.pingInterval)
        this.pingInterval = null
      }
    }

    try {
      this.socket = new WebSocket(url)

      this.socket.onopen = () => {
        console.log('WebSocket: Connected successfully')
        this.isConnected.value = true
        this.reconnectAttempts = 0
        
        // Устанавливаем ping интервал для поддержания соединения
        this.pingInterval = window.setInterval(() => {
          if (this.socket?.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify({ type: 'ping' }))
          }
        }, 30000) // Пинг каждые 30 секунд
      }

      this.socket.onmessage = (event) => {
        console.log('WebSocket: Message received:', event.data)
        try {
          const data = JSON.parse(event.data)
          if (data.type !== 'pong') {
            console.log('WebSocket: Broadcasting message to handlers:', data)
            this.messageHandlers.forEach(handler => {
              try {
                handler(data)
              } catch (error) {
                console.error('WebSocket: Error in message handler:', error)
              }
            })
          }
        } catch (error) {
          console.error('WebSocket: Error parsing message:', error)
        }
      }

      this.socket.onclose = (event) => {
        console.log('WebSocket: Connection closed', event.code, event.reason)
        this.isConnected.value = false
        if (this.pingInterval) {
          clearInterval(this.pingInterval)
          this.pingInterval = null
        }
        this.tryReconnect()
      }

      this.socket.onerror = (error) => {
        console.error('WebSocket: Error occurred:', error)
        this.isConnected.value = false
      }
    } catch (error) {
      console.error('WebSocket: Error creating connection:', error)
      this.isConnected.value = false
      this.tryReconnect()
    }
  }

  private tryReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts && this.currentType) {
      this.reconnectAttempts++
      const delay = this.reconnectTimeout * Math.min(this.reconnectAttempts, 3)
      console.log(`WebSocket: Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts}) in ${delay}ms`)
      
      setTimeout(() => {
        console.log('WebSocket: Reconnecting...')
        this.connect(this.currentType!, this.currentId)
      }, delay)
    } else {
      console.log('WebSocket: Max reconnection attempts reached')
    }
  }

  addMessageHandler(handler: (data: any) => void) {
    console.log('WebSocket: Adding message handler')
    this.messageHandlers.push(handler)
    console.log('WebSocket: Total handlers:', this.messageHandlers.length)
  }

  removeMessageHandler(handler: (data: any) => void) {
    console.log('WebSocket: Removing message handler')
    const index = this.messageHandlers.indexOf(handler)
    if (index > -1) {
      this.messageHandlers.splice(index, 1)
      console.log('WebSocket: Handler removed, remaining handlers:', this.messageHandlers.length)
    }
  }

  disconnect() {
    console.log('WebSocket: Disconnecting...')
    if (this.socket) {
      this.socket.close()
      this.socket = null
    }
    if (this.pingInterval) {
      clearInterval(this.pingInterval)
      this.pingInterval = null
    }
    this.currentType = null
    this.currentId = undefined
    this.isConnected.value = false
    console.log('WebSocket: Disconnected')
  }
}

export const wsClient = new WebSocketClient() 