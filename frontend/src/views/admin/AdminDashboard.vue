<template>
  <div class="p-6">
    <div class="mb-6">
      <h1 class="text-2xl font-bold mb-4">Панель администратора</h1>
      <div class="mb-4">
        <span :class="wsClient.isConnected ? 'text-green-600' : 'text-red-600'">
          {{ wsClient.isConnected ? 'WebSocket подключен' : 'WebSocket отключен' }}
        </span>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="bg-white p-4 rounded-lg shadow">
          <h3 class="text-lg font-semibold mb-2">Новые заявки</h3>
          <p class="text-3xl font-bold text-blue-600">{{ statistics.by_status?.NEW || 0 }}</p>
        </div>
        <div class="bg-white p-4 rounded-lg shadow">
          <h3 class="text-lg font-semibold mb-2">В работе</h3>
          <p class="text-3xl font-bold text-yellow-600">{{ statistics.by_status?.IN_PROGRESS || 0 }}</p>
        </div>
        <div class="bg-white p-4 rounded-lg shadow">
          <h3 class="text-lg font-semibold mb-2">Завершено</h3>
          <p class="text-3xl font-bold text-green-600">{{ statistics.by_status?.COMPLETED || 0 }}</p>
        </div>
        <div class="bg-white p-4 rounded-lg shadow">
          <h3 class="text-lg font-semibold mb-2">Отклонено</h3>
          <p class="text-3xl font-bold text-red-600">{{ statistics.by_status?.REJECTED || 0 }}</p>
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

const requests = ref([])
const statistics = ref({
  total: 0,
  by_status: {}
})

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
    statistics.value = statsResponse.data
  } catch (error) {
    console.error('Error fetching data:', error)
  }
}

// Обработчик WebSocket сообщений
const handleWebSocketMessage = (data: any) => {
  console.log('AdminDashboard: Received WebSocket message:', data)
  
  // Обновляем статистику, если она пришла в сообщении
  if (data.statistics) {
    console.log('AdminDashboard: Old statistics:', statistics.value)
    console.log('AdminDashboard: Updating statistics:', data.statistics)
    statistics.value = {
      total: data.statistics.total,
      by_status: { ...data.statistics.by_status }
    }
    console.log('AdminDashboard: New statistics:', statistics.value)
  }
  
  if (data.type === 'new_request' && data.data) {
    console.log('AdminDashboard: Adding new request:', data.data)
    // Добавляем новую заявку в начало списка
    requests.value = [data.data, ...requests.value]
  } else if (data.type === 'status_update' && data.data) {
    console.log('AdminDashboard: Updating request status:', data.data)
    // Обновляем статус заявки в списке
    const request = requests.value.find(r => r.id === data.data.id)
    if (request) {
      request.status = data.data.status
    }
  }
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

const getPriorityClass = (priority: string) => {
  const classes = {
    HIGH: 'text-red-600',
    MEDIUM: 'text-yellow-600',
    LOW: 'text-green-600'
  }
  return classes[priority] || ''
}

const getStatusClass = (status: string) => {
  const classes = {
    NEW: 'text-blue-600',
    IN_PROGRESS: 'text-yellow-600',
    COMPLETED: 'text-green-600',
    REJECTED: 'text-red-600'
  }
  return classes[status] || ''
}

const openRequestDetails = (request: any) => {
  // Здесь можно добавить логику открытия модального окна с деталями заявки
  console.log('Opening request details:', request)
}
</script> 