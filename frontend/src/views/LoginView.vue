<template>
  <div class="min-h-screen bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center p-4">
    <div class="max-w-md w-full bg-white rounded-xl shadow-2xl p-8">
      <div class="text-center mb-8">
        <h2 class="text-3xl font-bold text-gray-900">
          Вход для сотрудников
        </h2>
        <p class="mt-2 text-gray-600">
          Введите свои учетные данные
        </p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label for="last-name" class="block text-sm font-medium text-gray-700">
            Фамилия
          </label>
          <div class="mt-1">
            <input
              id="last-name"
              v-model="lastName"
              name="last-name"
              type="text"
              required
              class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="Введите фамилию"
            />
          </div>
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-gray-700">
            Пароль
          </label>
          <div class="mt-1">
            <input
              id="password"
              v-model="password"
              name="password"
              type="password"
              required
              class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="Введите пароль"
            />
          </div>
        </div>

        <div>
          <button
            type="submit"
            class="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors duration-200"
            :class="{ 'opacity-75 cursor-not-allowed': loading }"
            :disabled="loading"
          >
            <span v-if="loading">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Вход...
            </span>
            <span v-else>Войти</span>
          </button>
        </div>

        <div v-if="error" class="rounded-lg bg-red-50 p-4 text-sm text-red-700">
          {{ error }}
        </div>

        <div class="text-center">
          <router-link 
            to="/" 
            class="text-sm text-indigo-600 hover:text-indigo-500"
          >
            Вернуться на главную
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const lastName = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  loading.value = true
  error.value = ''

  try {
    console.log('Отправка запроса на авторизацию...')
    const formData = new FormData()
    formData.append('username', lastName.value)
    formData.append('password', password.value)
    
    const response = await axios.post('/api/auth/login', formData)
    console.log('Ответ от сервера:', response.data)

    // Сохраняем данные сотрудника и токен
    localStorage.setItem('employee', JSON.stringify(response.data))
    localStorage.setItem('token', response.data.access_token)

    console.log('Перенаправление на /requests...')
    // Перенаправляем на страницу заявок
    await router.push('/requests')
  } catch (e: any) {
    console.error('Ошибка при авторизации:', e)
    error.value = e.response?.data?.detail || 'Неверная фамилия или пароль'
  } finally {
    loading.value = false
  }
}
</script>
