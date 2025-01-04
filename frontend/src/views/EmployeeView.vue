<template>
  <div :class="{'dark': isDarkMode}" class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-900">
    <!-- Шапка -->
    <header class="bg-white shadow-md dark:bg-gray-800 transition-colors duration-200">
      <div class="container mx-auto px-6 py-4 flex justify-between items-center">
        <h1 class="text-2xl font-bold text-gray-800 dark:text-white">IT Support</h1>
        <div class="flex items-center space-x-4">
          <!-- Переключатель темы -->
          <button
            @click="toggleDarkMode"
            class="p-2 rounded-lg text-gray-600 hover:text-gray-800 hover:bg-gray-100 dark:text-gray-300 dark:hover:text-white dark:hover:bg-gray-700 transition-all duration-200"
            :title="isDarkMode ? 'Включить светлую тему' : 'Включить темную тему'"
          >
            <svg v-if="isDarkMode" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
            </svg>
          </button>
          <button
            @click="handleLogout"
            class="px-4 py-2 rounded-lg text-gray-600 hover:text-gray-800 hover:bg-gray-100 dark:text-gray-300 dark:hover:text-white dark:hover:bg-gray-700 transition-all duration-200 flex items-center space-x-2"
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
                v-for="request in displayedRequests"
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
            <div class="mt-6 flex justify-center">
              <button
                @click="showRequestsModal = true"
                class="text-purple-600 hover:text-purple-700 font-semibold flex items-center space-x-2 group"
              >
                <span>Показать все заявки</span>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 transform group-hover:translate-x-1 transition-transform" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>

  <!-- Модальное окно всех заявок -->
  <div v-if="showRequestsModal" class="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
    <div class="bg-white rounded-2xl max-w-4xl w-full shadow-2xl transform transition-all max-h-[90vh] flex flex-col">
      <div class="flex justify-between items-center p-6 border-b border-gray-100">
        <h3 class="text-xl font-bold text-gray-800">Все заявки</h3>
        <button 
          @click="showRequestsModal = false"
          class="text-gray-400 hover:text-gray-600 transition-colors"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      <div class="overflow-y-auto flex-1 p-6">
        <div class="space-y-4">
          <div
            v-for="request in paginatedRequests"
            :key="request.id"
            class="bg-gray-50 rounded-xl p-4 hover:bg-gray-100 transition-colors border-2 border-transparent hover:border-purple-200"
          >
            <div class="flex justify-between items-start">
              <div>
                <h3 class="font-semibold text-gray-800">{{ getRequestTypeLabel(request.request_type) }}</h3>
                <p class="text-gray-600 mt-1">{{ request.description }}</p>
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
      <div class="p-6 border-t border-gray-100">
        <div class="flex justify-between items-center">
          <div class="text-sm text-gray-600">
            Показано {{ startIndex + 1 }}-{{ Math.min(endIndex, requests.length) }} из {{ requests.length }} заявок
          </div>
          <div class="flex space-x-2">
            <button
              @click="currentPage--"
              :disabled="currentPage === 1"
              class="px-4 py-2 rounded-lg bg-gray-100 text-gray-700 hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              Назад
            </button>
            <button
              @click="currentPage++"
              :disabled="currentPage >= totalPages"
              class="px-4 py-2 rounded-lg bg-purple-100 text-purple-700 hover:bg-purple-200 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              Вперед
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Модальное окно создания заявки -->
  <div v-if="showRequestModal" class="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
    <div class="bg-white dark:bg-gray-800 rounded-2xl max-w-xl w-full shadow-2xl transform transition-all">
      <div class="flex justify-between items-center p-6 border-b border-gray-100 dark:border-gray-700">
        <h3 class="text-xl font-bold text-gray-800 dark:text-white">Создать заявку</h3>
        <button 
          @click="showRequestModal = false"
          class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      <form @submit.prevent="submitRequest" class="p-6 space-y-6">
        <!-- Тип заявки -->
        <div class="space-y-2">
          <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300">Тип заявки</label>
          <div class="grid grid-cols-2 gap-4">
            <label 
              v-for="type in requestTypes" 
              :key="type.value"
              class="relative flex cursor-pointer rounded-lg border border-gray-200 dark:border-gray-700 p-4 focus:outline-none"
              :class="{'bg-blue-50 border-blue-200 dark:bg-blue-900/30 dark:border-blue-700': requestForm.request_type === type.value}"
            >
              <input 
                type="radio" 
                :value="type.value" 
                v-model="requestForm.request_type"
                class="sr-only"
                required
              >
              <span class="flex flex-1">
                <span class="flex flex-col">
                  <span class="block text-sm font-medium text-gray-900 dark:text-white">
                    {{ type.label }}
                  </span>
                  <span class="mt-1 flex items-center text-sm text-gray-500 dark:text-gray-400">
                    {{ type.description }}
                  </span>
                </span>
              </span>
              <svg 
                class="h-5 w-5 text-blue-600 dark:text-blue-400"
                :class="{'hidden': requestForm.request_type !== type.value}"
                xmlns="http://www.w3.org/2000/svg" 
                viewBox="0 0 20 20" 
                fill="currentColor"
              >
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
              </svg>
            </label>
          </div>
        </div>

        <!-- Описание -->
        <div class="space-y-2">
          <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300">Описание проблемы</label>
          <div class="relative">
            <textarea
              v-model="requestForm.description"
              required
              rows="4"
              class="w-full rounded-xl border-gray-200 dark:border-gray-700 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:text-white resize-none"
              placeholder="Опишите вашу проблему подробно..."
            ></textarea>
            <div class="absolute bottom-3 right-3 text-sm text-gray-400 dark:text-gray-500">
              {{ requestForm.description.length }}/500
            </div>
          </div>
        </div>

        <!-- Приоритет -->
        <div class="space-y-2">
          <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300">Приоритет</label>
          <div class="flex space-x-4">
            <label 
              v-for="priority in priorities" 
              :key="priority.value"
              class="flex-1 relative"
            >
              <input 
                type="radio" 
                :value="priority.value" 
                v-model="requestForm.priority"
                class="sr-only"
                required
              >
              <div 
                class="w-full p-4 text-center rounded-xl cursor-pointer transition-all"
                :class="{
                  'bg-green-50 text-green-700 border-green-200 dark:bg-green-900/30 dark:text-green-400 dark:border-green-700': priority.value === 'low' && requestForm.priority === 'low',
                  'bg-yellow-50 text-yellow-700 border-yellow-200 dark:bg-yellow-900/30 dark:text-yellow-400 dark:border-yellow-700': priority.value === 'medium' && requestForm.priority === 'medium',
                  'bg-red-50 text-red-700 border-red-200 dark:bg-red-900/30 dark:text-red-400 dark:border-red-700': priority.value === 'high' && requestForm.priority === 'high',
                  'bg-gray-50 text-gray-700 border-gray-200 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-700': requestForm.priority !== priority.value
                }"
              >
                <span class="block font-medium">{{ priority.label }}</span>
                <span class="mt-1 text-sm opacity-75">{{ priority.description }}</span>
              </div>
            </label>
          </div>
        </div>

        <button
          type="submit"
          class="w-full bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-semibold py-3 px-6 rounded-xl transition-all duration-300 transform hover:scale-105 flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
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
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const requests = ref([])
const isSubmitting = ref(false)
const showRequestModal = ref(false)
const showRequestsModal = ref(false)
const isDarkMode = ref(false)

// Типы заявок
const requestTypes = [
  {
    value: 'hardware',
    label: 'Проблема с оборудованием',
    description: 'Неполадки с компьютером, принтером или другим оборудованием'
  },
  {
    value: 'software',
    label: 'Проблема с ПО',
    description: 'Проблемы с программным обеспечением'
  },
  {
    value: 'network',
    label: 'Проблема с сетью',
    description: 'Проблемы с интернетом или локальной сетью'
  },
  {
    value: 'access',
    label: 'Доступ к системам',
    description: 'Запрос доступа к системам или сервисам'
  }
]

// Приоритеты
const priorities = [
  {
    value: 'low',
    label: 'Низкий',
    description: 'Не срочно'
  },
  {
    value: 'medium',
    label: 'Средний',
    description: 'Важно'
  },
  {
    value: 'high',
    label: 'Высокий',
    description: 'Срочно'
  }
]

// Переключение темы
const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value
  if (isDarkMode.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}

// Проверяем предпочтения пользователя при загрузке
onMounted(() => {
  // Проверяем сохраненные настройки темы
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    isDarkMode.value = true
    document.documentElement.classList.add('dark')
  }
  
  fetchRequests()
})

// Пагинация
const currentPage = ref(1)
const itemsPerPage = 5
const displayedRequestsCount = 3 // Количество заявок для отображения в блоке

// Вычисляемые свойства для пагинации
const startIndex = computed(() => (currentPage.value - 1) * itemsPerPage)
const endIndex = computed(() => startIndex.value + itemsPerPage)
const totalPages = computed(() => Math.ceil(requests.value.length / itemsPerPage))

// Заявки для текущей страницы
const paginatedRequests = computed(() => {
  return requests.value.slice(startIndex.value, endIndex.value)
})

// Заявки для отображения в блоке
const displayedRequests = computed(() => {
  return requests.value.slice(0, displayedRequestsCount)
})

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
</script>

<style>
/* Добавляем плавные переходы для смены темы */
.dark {
  color-scheme: dark;
}

* {
  transition-property: color, background-color, border-color;
  transition-duration: 200ms;
}
</style> 