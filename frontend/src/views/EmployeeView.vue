<template>
  <div class="min-h-screen bg-primary text-primary">
    <!-- Шапка -->
    <header class="bg-secondary border-b border-border">
      <div class="container mx-auto px-4 py-4 flex justify-between items-center">
        <h1 class="text-xl font-semibold">IT Support</h1>
        <div class="flex items-center space-x-4">
          <ThemeToggle />
          <button 
            @click="handleLogout" 
            class="text-button-primary hover:text-button-hover transition-colors"
          >
            Выйти
          </button>
        </div>
      </div>
    </header>

    <!-- Основной контент -->
    <main class="container mx-auto px-4 py-8">
      <!-- Форма создания заявки -->
      <div class="bg-card rounded-lg shadow-lg p-6 mb-8">
        <h2 class="text-lg font-semibold mb-4">Создать заявку</h2>
        <form @submit.prevent="submitRequest" class="space-y-4">
          <div>
            <label class="block text-secondary mb-1">Тема</label>
            <input
              v-model="requestForm.title"
              type="text"
              required
              class="w-full px-4 py-2 rounded-lg bg-input text-primary border border-input-border focus:border-button-primary transition-colors"
              placeholder="Введите тему заявки"
            >
          </div>
          <div>
            <label class="block text-secondary mb-1">Описание</label>
            <textarea
              v-model="requestForm.description"
              required
              rows="4"
              class="w-full px-4 py-2 rounded-lg bg-input text-primary border border-input-border focus:border-button-primary transition-colors"
              placeholder="Опишите вашу проблему"
            ></textarea>
          </div>
          <div>
            <label class="block text-secondary mb-1">Приоритет</label>
            <select
              v-model="requestForm.priority"
              required
              class="w-full px-4 py-2 rounded-lg bg-input text-primary border border-input-border focus:border-button-primary transition-colors"
            >
              <option value="low">Низкий</option>
              <option value="medium">Средний</option>
              <option value="high">Высокий</option>
            </select>
          </div>
          <button
            type="submit"
            class="w-full bg-button-primary hover:bg-button-hover text-white font-medium py-2 px-4 rounded-lg transition-colors"
            :disabled="isSubmitting"
          >
            {{ isSubmitting ? 'Отправка...' : 'Отправить заявку' }}
          </button>
        </form>
      </div>

      <!-- Список заявок -->
      <div class="bg-card rounded-lg shadow-lg p-6">
        <h2 class="text-lg font-semibold mb-4">Мои заявки</h2>
        <div class="space-y-4">
          <div
            v-for="request in requests"
            :key="request.id"
            class="border border-border rounded-lg p-4"
          >
            <div class="flex justify-between items-start">
              <div>
                <h3 class="font-medium">{{ request.title }}</h3>
                <p class="text-secondary mt-1">{{ request.description }}</p>
              </div>
              <span 
                class="px-2 py-1 rounded-full text-sm"
                :class="getStatusClass(request.status)"
              >
                {{ getStatusLabel(request.status) }}
              </span>
            </div>
            <div class="mt-2 text-sm text-secondary">
              {{ new Date(request.created_at).toLocaleString() }}
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import ThemeToggle from '@/components/ThemeToggle.vue'

const router = useRouter()
const requests = ref([])
const isSubmitting = ref(false)

const requestForm = ref({
  title: '',
  description: '',
  priority: 'low'
})

// Получение заявок
const fetchRequests = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch('/api/requests/', {
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
    
    if (!response.ok) throw new Error('Failed to create request')
    
    // Очищаем форму
    requestForm.value = {
      title: '',
      description: '',
      priority: 'low'
    }
    
    // Обновляем список заявок
    await fetchRequests()
  } catch (error) {
    console.error('Error creating request:', error)
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

onMounted(() => {
  fetchRequests()
})
</script>

<style>
/* Используем CSS переменные для цветов */
.bg-primary {
  background-color: var(--color-bg-primary);
}

.bg-secondary {
  background-color: var(--color-bg-secondary);
}

.bg-card {
  background-color: var(--color-card-bg);
}

.bg-input {
  background-color: var(--color-input-bg);
}

.text-primary {
  color: var(--color-text-primary);
}

.text-secondary {
  color: var(--color-text-secondary);
}

.border-border {
  border-color: var(--color-border);
}

.border-input-border {
  border-color: var(--color-input-border);
}

.bg-button-primary {
  background-color: var(--color-button-primary);
}

.hover\:bg-button-hover:hover {
  background-color: var(--color-button-hover);
}

.text-button-primary {
  color: var(--color-button-primary);
}

.hover\:text-button-hover:hover {
  color: var(--color-button-hover);
}
</style> 