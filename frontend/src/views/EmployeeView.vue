<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
    <!-- Шапка -->
    <header class="bg-white shadow-md">
      <div class="container mx-auto px-6 py-4 flex justify-between items-center">
        <h1 class="text-2xl font-bold text-gray-800">IT Support</h1>
        <div class="flex items-center space-x-4">
          <button
            @click="handleLogout"
            class="px-4 py-2 rounded-lg text-gray-600 hover:text-gray-800 hover:bg-gray-100 transition-all duration-300 flex items-center space-x-2"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M3 3a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V4a1 1 0 0 0-1-1H3zm11 4.414l-4.293 4.293a1 1 0 0 1-1.414 0L4 7.414 5.414 6l3.293 3.293L12 6l2 1.414z" clip-rule="evenodd" />
            </svg>
            <span>Выйти</span>
          </button>
        </div>
      </div>
    </header>

    <!-- Основной контент -->
    <main class="container mx-auto px-6 py-8">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <!-- Блок 1: Создать заявку -->
        <div class="group bg-white rounded-2xl shadow-lg hover:shadow-2xl transform hover:-translate-y-1 transition-all duration-300">
          <div class="p-8">
            <div class="flex items-center justify-between mb-6">
              <h2 class="text-xl font-bold text-gray-800 group-hover:text-blue-600 transition-colors">Создать заявку</h2>
              <button
                @click="showRequestModal = true"
                class="bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white px-6 py-3 rounded-xl transition-all duration-300 flex items-center space-x-2 transform hover:scale-105"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
                </svg>
                <span>Создать</span>
              </button>
            </div>
            <p class="text-gray-600 leading-relaxed">
              Создайте новую заявку в службу поддержки для решения технических проблем. Мы поможем вам с любыми вопросами.
            </p>
          </div>
        </div>

        <!-- Блок 2: Перейти в чат -->
        <div class="group bg-white rounded-2xl shadow-lg hover:shadow-2xl transform hover:-translate-y-1 transition-all duration-300">
          <div class="p-8">
            <div class="flex items-center justify-between mb-6">
              <h2 class="text-xl font-bold text-gray-800 group-hover:text-green-600 transition-colors">Чат поддержки</h2>
              <button
                class="bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white px-6 py-3 rounded-xl transition-all duration-300 flex items-center space-x-2 transform hover:scale-105"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clip-rule="evenodd" />
                </svg>
                <span>Открыть чат</span>
              </button>
            </div>
            <p class="text-gray-600 leading-relaxed">
              Общайтесь с технической поддержкой в реальном времени для быстрого решения проблем. Мы всегда на связи.
            </p>
          </div>
        </div>

        <!-- Блок 3: Мои заявки -->
        <div class="group bg-white rounded-2xl shadow-lg hover:shadow-2xl transform hover:-translate-y-1 transition-all duration-300">
          <div class="p-8">
            <div class="flex items-center justify-between mb-6">
              <h2 class="text-xl font-bold text-gray-800 group-hover:text-purple-600 transition-colors">Мои заявки</h2>
              <span class="bg-purple-100 text-purple-800 px-4 py-2 rounded-xl text-sm font-semibold">
                {{ requests.length }} заявок
              </span>
            </div>
            <div class="space-y-4">
              <div
                v-for="request in requests"
                :key="request.id"
                class="bg-gray-50 rounded-xl p-4 hover:bg-gray-100 transition-colors group-hover:border-purple-200 border-2 border-transparent"
              >
                <div class="flex justify-between items-start">
                  <div>
                    <h3 class="font-semibold text-gray-800">{{ getRequestTypeLabel(request.request_type) }}</h3>
                    <p class="text-gray-600 mt-1 text-sm">{{ request.description }}</p>
                  </div>
                  <span 
                    class="px-4 py-1 rounded-lg text-sm font-semibold shadow-sm"
                    :class="getStatusClass(request.status)"
                  >
                    {{ getStatusLabel(request.status) }}
                  </span>
                </div>
                <div class="mt-3 text-sm text-gray-500 flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd" />
                  </svg>
                  {{ new Date(request.created_at).toLocaleString() }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>

  <!-- Модальное окно создания заявки -->
  <div v-if="showRequestModal" class="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
    <div class="bg-white rounded-2xl max-w-md w-full shadow-2xl transform transition-all">
      <div class="flex justify-between items-center p-6 border-b border-gray-100">
        <h3 class="text-xl font-bold text-gray-800">Создать заявку</h3>
        <button 
          @click="showRequestModal = false"
          class="text-gray-400 hover:text-gray-600 transition-colors"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      <form @submit.prevent="submitRequest" class="p-6 space-y-6">
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">Тип заявки</label>
          <select
            v-model="requestForm.request_type"
            required
            class="w-full rounded-xl border-gray-200 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-gray-700"
          >
            <option value="">Выберите тип</option>
            <option value="hardware">Проблема с оборудованием</option>
            <option value="software">Проблема с ПО</option>
            <option value="network">Проблема с сетью</option>
            <option value="access">Доступ к системам</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">Описание</label>
          <textarea
            v-model="requestForm.description"
            required
            rows="4"
            class="w-full rounded-xl border-gray-200 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-gray-700"
            placeholder="Опишите вашу проблему подробно..."
          ></textarea>
        </div>
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">Приоритет</label>
          <select
            v-model="requestForm.priority"
            required
            class="w-full rounded-xl border-gray-200 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-gray-700"
          >
            <option value="low">Низкий</option>
            <option value="medium">Средний</option>
            <option value="high">Высокий</option>
          </select>
        </div>
        <button
          type="submit"
          class="w-full bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-semibold py-3 px-6 rounded-xl transition-all duration-300 transform hover:scale-105 flex items-center justify-center space-x-2"
          :disabled="isSubmitting"
        >
          <svg v-if="isSubmitting" class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>{{ isSubmitting ? 'Отправка...' : 'Отправить заявку' }}</span>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const requests = ref([])
const isSubmitting = ref(false)
const showRequestModal = ref(false)

const requestForm = ref({
  request_type: '',
  description: '',
  priority: 'low'
})

// Получение заявок
const fetchRequests = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch('/api/requests/my', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    if (!response.ok) throw new Error('Failed to fetch requests')
    requests.value = await response.json()
  } catch (error) {
    console.error('Error fetching requests:', error)
  }
}

// Отправка заявки
const submitRequest = async () => {
  try {
    isSubmitting.value = true
    const token = localStorage.getItem('token')
    const response = await fetch('/api/requests/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(requestForm.value)
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Failed to create request')
    }

    // Очищаем форму и закрываем модальное окно
    requestForm.value = {
      request_type: '',
      description: '',
      priority: 'low'
    }
    showRequestModal.value = false

    // Обновляем список заявок
    await fetchRequests()
  } catch (error) {
    console.error('Error creating request:', error)
    alert(error.message)
  } finally {
    isSubmitting.value = false
  }
}

// Выход из системы
const handleLogout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}

// Получение класса для статуса
const getStatusClass = (status) => {
  const classes = {
    new: 'bg-blue-100 text-blue-800',
    in_progress: 'bg-yellow-100 text-yellow-800',
    completed: 'bg-green-100 text-green-800',
    rejected: 'bg-red-100 text-red-800'
  }
  return classes[status] || classes.new
}

// Получение метки для статуса
const getStatusLabel = (status) => {
  const labels = {
    new: 'Новая',
    in_progress: 'В работе',
    completed: 'Завершена',
    rejected: 'Отклонена'
  }
  return labels[status] || 'Новая'
}

// Получение метки для типа заявки
const getRequestTypeLabel = (type) => {
  const labels = {
    hardware: 'Проблема с оборудованием',
    software: 'Проблема с ПО',
    network: 'Проблема с сетью',
    access: 'Доступ к системам'
  }
  return labels[type] || type
}

onMounted(() => {
  fetchRequests()
})
</script> 