<template>
  <div class="min-h-screen bg-gray-100">
    <div class="max-w-4xl mx-auto p-6">
      <h1 class="text-2xl font-bold text-gray-900 mb-6">Создание заявки</h1>

      <form @submit.prevent="handleSubmit" class="space-y-6 bg-white shadow-lg rounded-lg p-6">
        <div>
          <label for="department" class="block text-sm font-medium text-gray-700">Отдел</label>
          <select
            id="department"
            v-model="formData.department"
            class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
            required
          >
            <option value="">Выберите отдел</option>
            <option value="IT">IT</option>
            <option value="HR">HR</option>
            <option value="Finance">Финансы</option>
            <option value="Marketing">Маркетинг</option>
          </select>
        </div>

        <div>
          <label for="request_type" class="block text-sm font-medium text-gray-700">Тип заявки</label>
          <select
            id="request_type"
            v-model="formData.request_type"
            class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
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
          <label for="priority" class="block text-sm font-medium text-gray-700">Приоритет</label>
          <select
            id="priority"
            v-model="formData.priority"
            class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
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
          <label for="description" class="block text-sm font-medium text-gray-700">Описание</label>
          <textarea
            id="description"
            v-model="formData.description"
            rows="4"
            class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            placeholder="Опишите вашу проблему..."
            required
          ></textarea>
        </div>

        <div class="flex justify-end">
          <button
            type="submit"
            class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            :disabled="loading"
          >
            <span v-if="loading">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
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
import axios from 'axios'

interface Employee {
  id: number
  first_name: string
  last_name: string
  department: string
  office: string
}

const formData = reactive({
  department: '',
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
    const employee = JSON.parse(employeeData) as Employee
    formData.employee_id = employee.id
  }
})

const handleSubmit = async () => {
  loading.value = true
  error.value = ''
  success.value = false

  try {
    const token = localStorage.getItem('token')
    if (!token) {
      throw new Error('Не найден токен авторизации')
    }

    await axios.post('/api/requests/', formData, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    success.value = true
    // Очищаем форму
    formData.department = ''
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
</script> 