<template>
  <div class="p-6">
    <div class="mb-6">
      <h1 class="text-2xl font-bold mb-4">Панель администратора</h1>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="bg-white p-4 rounded-lg shadow">
          <h3 class="text-lg font-semibold mb-2">Новые заявки</h3>
          <p class="text-3xl font-bold text-blue-600">{{ statistics.by_status?.new || 0 }}</p>
        </div>
        <div class="bg-white p-4 rounded-lg shadow">
          <h3 class="text-lg font-semibold mb-2">В работе</h3>
          <p class="text-3xl font-bold text-yellow-600">{{ statistics.by_status?.in_progress || 0 }}</p>
        </div>
        <div class="bg-white p-4 rounded-lg shadow">
          <h3 class="text-lg font-semibold mb-2">Завершено</h3>
          <p class="text-3xl font-bold text-green-600">{{ statistics.by_status?.completed || 0 }}</p>
        </div>
        <div class="bg-white p-4 rounded-lg shadow">
          <h3 class="text-lg font-semibold mb-2">Отклонено1</h3>
          <p class="text-3xl font-bold text-red-600">{{ statistics.by_status?.rejected || 0 }}</p>
        </div>
      </div>
    </div>

    <div class="bg-white rounded-lg shadow p-6">
      <h2 class="text-xl font-bold mb-4">Последние заявки</h2>
      <div class="overflow-x-auto">
        <table class="min-w-full table-auto">
          <thead>
            <tr class="bg-gray-100">
              <th class="px-4 py-2 text-left">ID</th>
              <th class="px-4 py-2 text-left">Сотрудник</th>
              <th class="px-4 py-2 text-left">Тип</th>
              <th class="px-4 py-2 text-left">Приоритет</th>
              <th class="px-4 py-2 text-left">Статус</th>
              <th class="px-4 py-2 text-left">Дата создания</th>
              <th class="px-4 py-2 text-left">Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in requests" :key="request.id" class="border-b">
              <td class="px-4 py-2">#{{ request.id }}</td>
              <td class="px-4 py-2">{{ request.employee_name }}</td>
              <td class="px-4 py-2">{{ request.request_type }}</td>
              <td class="px-4 py-2">
                <span :class="getPriorityClass(request.priority)">
                  {{ request.priority }}
                </span>
              </td>
              <td class="px-4 py-2">
                <span :class="getStatusClass(request.status)">
                  {{ request.status }}
                </span>
              </td>
              <td class="px-4 py-2">{{ formatDate(request.created_at) }}</td>
              <td class="px-4 py-2">
                <button @click="openRequestDetails(request)" class="text-blue-600 hover:text-blue-800">
                  Подробнее
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import axios from '@/plugins/axios'
import { wsClient } from '@/plugins/websocket'
import { formatDate } from '@/utils/date'

interface Request {
  id: number;
  employee_name: string;
  request_type: string;
  priority: 'high' | 'medium' | 'low';
  status: 'new' | 'in_progress' | 'completed' | 'rejected';
  created_at: string;
}

interface Statistics {
  total: number;
  by_status: {
    new: number;
    in_progress: number;
    completed: number;
    rejected: number;
  };
}

interface WebSocketMessage {
  type: 'new_request' | 'status_update';
  data?: Request;
  statistics?: {
    total: number;
    by_status: {
      new: number;
      in_progress: number;
      completed: number;
      rejected: number;
    };
  };
}

const requests = ref<Request[]>([])
const statistics = ref<Statistics>({
  total: 0,
  by_status: {
    new: 0,
    in_progress: 0,
    completed: 0,
    rejected: 0
  }
})

// Обработчик WebSocket сообщений
const handleWebSocketMessage = (data: WebSocketMessage) => {
  console.log('AdminDashboard: Received WebSocket message:', data)
  
  if (data.type === 'new_request' || data.type === 'status_update') {
    if (data.statistics) {
      console.log('AdminDashboard: Old statistics:', statistics.value)
      console.log('AdminDashboard: Updating statistics:', data.statistics)
      
      // Обновляем статистику
      statistics.value = {
        total: data.statistics.total,
        by_status: {
          new: data.statistics.by_status?.new || 0,
          in_progress: data.statistics.by_status?.in_progress || 0,
          completed: data.statistics.by_status?.completed || 0,
          rejected: data.statistics.by_status?.rejected || 0
        }
      }
      
      console.log('AdminDashboard: New statistics:', statistics.value)
    }
    
    if (data.type === 'new_request' && data.data) {
      console.log('AdminDashboard: Adding new request:', data.data)
      // Добавляем новую заявку в начало списка
      const newRequest = data.data as Request
      requests.value = [newRequest, ...requests.value]
    } else if (data.type === 'status_update' && data.data) {
      console.log('AdminDashboard: Updating request status:', data.data)
      // Обновляем статус заявки в списке
      const updatedRequest = data.data as Request
      const request = requests.value.find(r => r.id === updatedRequest.id)
      if (request) {
        request.status = updatedRequest.status
      }
    }
  }
}

// Загрузка данных
const fetchData = async () => {
  try {
    console.log('AdminDashboard: Fetching data')
    const [requestsResponse, statsResponse] = await Promise.all([
      axios.get('/api/requests/admin'),
      axios.get('/api/requests/statistics')
    ])
    requests.value = requestsResponse.data
    console.log('AdminDashboard: Received statistics:', statsResponse.data)
    
    // Обновляем статистику
    statistics.value = {
      total: statsResponse.data.total,
      by_status: {
        new: statsResponse.data.by_status?.new || 0,
        in_progress: statsResponse.data.by_status?.in_progress || 0,
        completed: statsResponse.data.by_status?.completed || 0,
        rejected: statsResponse.data.by_status?.rejected || 0
      }
    }
  } catch (error) {
    console.error('Error fetching data:', error)
  }
}

const getPriorityClass = (priority: 'high' | 'medium' | 'low'): string => {
  const classes: Record<'high' | 'medium' | 'low', string> = {
    high: 'text-red-600',
    medium: 'text-yellow-600',
    low: 'text-green-600'
  }
  return classes[priority]
}

const getStatusClass = (status: 'new' | 'in_progress' | 'completed' | 'rejected'): string => {
  const classes: Record<'new' | 'in_progress' | 'completed' | 'rejected', string> = {
    new: 'text-blue-600',
    in_progress: 'text-yellow-600',
    completed: 'text-green-600',
    rejected: 'text-red-600'
  }
  return classes[status]
}

const openRequestDetails = (request: Request) => {
  console.log('Opening request details:', request)
}

// Подключение к WebSocket при монтировании компонента
onMounted(() => {
  console.log('AdminDashboard: Component mounted')
  fetchData()
  
  // Добавляем небольшую задержку перед подключением WebSocket
  setTimeout(() => {
    console.log('AdminDashboard: Connecting to WebSocket')
    wsClient.connect('admin')
    wsClient.addMessageHandler(handleWebSocketMessage)
  }, 1000)
})

// Переподключение WebSocket при потере соединения
watch(() => wsClient.isConnected, (isConnected) => {
  console.log('AdminDashboard: WebSocket connection status changed:', isConnected)
  if (!isConnected) {
    console.log('AdminDashboard: Attempting to reconnect')
    setTimeout(() => {
      wsClient.connect('admin')
    }, 3000)
  }
})

// Отключение от WebSocket при размонтировании компонента
onUnmounted(() => {
  console.log('AdminDashboard: Component unmounting')
  wsClient.removeMessageHandler(handleWebSocketMessage)
  wsClient.disconnect()
})
</script> 