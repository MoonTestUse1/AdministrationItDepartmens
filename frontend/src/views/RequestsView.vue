<template>
  <div class="min-h-screen bg-primary text-primary">
    <!-- Шапка -->
    <header class="bg-secondary border-b border-border mb-6">
      <div class="max-w-4xl mx-auto px-4 py-4 flex justify-between items-center">
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

    <div class="max-w-4xl mx-auto p-6">
      <h1 class="text-2xl font-bold mb-6">Создание заявки</h1>

      <form @submit.prevent="handleSubmit" class="space-y-6 bg-card rounded-lg shadow-lg p-6">
        <div>
          <label for="request_type" class="block text-sm font-medium text-secondary mb-1">Тип заявки</label>
          <select
            id="request_type"
            v-model="formData.request_type"
            class="w-full px-4 py-2 rounded-lg bg-input text-primary border border-input-border focus:border-button-primary transition-colors"
            required
          >
            <option value="">Выберите тип</option>
            <option value="access">Доступ к системе</option>
            <option value="software">Установка ПО</option>
            <option value="hardware">Проблема с оборудованием</option>
            <option value="other">Другое</option>
          </select>
        </div>

        <div>
          <label for="priority" class="block text-sm font-medium text-secondary mb-1">Приоритет</label>
          <select
            id="priority"
            v-model="formData.priority"
            class="w-full px-4 py-2 rounded-lg bg-input text-primary border border-input-border focus:border-button-primary transition-colors"
            required
          >
            <option value="">Выберите приоритет</option>
            <option value="low">Низкий</option>
            <option value="medium">Средний</option>
            <option value="high">Высокий</option>
            <option value="critical">Критический</option>
          </select>
        </div>

        <div>
          <label for="description" class="block text-sm font-medium text-secondary mb-1">Описание</label>
          <textarea
            id="description"
            v-model="formData.description"
            rows="4"
            class="w-full px-4 py-2 rounded-lg bg-input text-primary border border-input-border focus:border-button-primary transition-colors"
            placeholder="Опишите вашу проблему..."
            required
          ></textarea>
        </div>

        <div class="flex justify-end">
          <button
            type="submit"
            class="px-4 py-2 bg-button-primary hover:bg-button-hover text-white font-medium rounded-lg transition-colors"
            :disabled="loading"
          >
            <span v-if="loading" class="flex items-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Отправка...
            </span>
            <span v-else>Отправить заявку</span>
          </button>
        </div>

        <div v-if="error" class="mt-2 text-sm text-red-600 bg-red-50 p-3 rounded-md">
          {{ error }}
        </div>

        <div v-if="success" class="mt-2 text-sm text-green-600 bg-green-50 p-3 rounded-md">
          Заявка успешно создана!
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import ThemeToggle from '@/components/ThemeToggle.vue'

const router = useRouter()
const formData = reactive({
  request_type: '',
  priority: '',
  description: '',
  employee_id: 0
})

const loading = ref(false)
const error = ref('')
const success = ref(false)

onMounted(() => {
  // Получаем данные сотрудника из localStorage
  const employeeData = localStorage.getItem('employee')
  if (employeeData) {
    const employee = JSON.parse(employeeData)
    formData.employee_id = employee.id
  }
})

const handleSubmit = async () => {
  loading.value = true
  error.value = ''
  success.value = false

  try {
    const token = localStorage.getItem('token')
    const employeeData = localStorage.getItem('employee')
    
    if (!token) {
      throw new Error('Не найден токен авторизации')
    }
    
    if (!employeeData) {
      throw new Error('Не найдены данные сотрудника')
    }

    const employee = JSON.parse(employeeData)
    
    const requestData = {
      description: formData.description,
      priority: formData.priority,
      request_type: formData.request_type
    }

    await axios.post('/api/requests/', requestData, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    success.value = true
    // Очищаем форму
    formData.request_type = ''
    formData.priority = ''
    formData.description = ''
  } catch (e: any) {
    console.error('Ошибка при создании заявки:', e)
    error.value = e.response?.data?.detail || 'Произошла ошибка при создании заявки'
  } finally {
    loading.value = false
  }
}

const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('employee')
  router.push('/login')
}
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