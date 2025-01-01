<template>
  <div class="min-h-screen bg-gray-100">
    <!-- Верхняя панель -->
    <nav class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex">
            <div class="flex-shrink-0 flex items-center">
              <h1 class="text-xl font-bold text-gray-900">IT Support Admin</h1>
            </div>
          </div>
          <div class="flex items-center">
            <button
              @click="handleLogout"
              class="ml-3 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
            >
              Выйти
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Основной контент -->
    <div class="py-6">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="bg-white shadow rounded-lg divide-y divide-gray-200">
          <!-- Статистика -->
          <div class="px-6 py-5">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
              Общая статистика
            </h3>
            <div class="grid grid-cols-1 gap-5 sm:grid-cols-3">
              <div class="bg-purple-50 overflow-hidden shadow rounded-lg">
                <div class="px-4 py-5 sm:p-6">
                  <dt class="text-sm font-medium text-purple-600 truncate">
                    Всего заявок
                  </dt>
                  <dd class="mt-1 text-3xl font-semibold text-purple-900">
                    0
                  </dd>
                </div>
              </div>

              <div class="bg-indigo-50 overflow-hidden shadow rounded-lg">
                <div class="px-4 py-5 sm:p-6">
                  <dt class="text-sm font-medium text-indigo-600 truncate">
                    Активные заявки
                  </dt>
                  <dd class="mt-1 text-3xl font-semibold text-indigo-900">
                    0
                  </dd>
                </div>
              </div>

              <div class="bg-green-50 overflow-hidden shadow rounded-lg">
                <div class="px-4 py-5 sm:p-6">
                  <dt class="text-sm font-medium text-green-600 truncate">
                    Решенные заявки
                  </dt>
                  <dd class="mt-1 text-3xl font-semibold text-green-900">
                    0
                  </dd>
                </div>
              </div>
            </div>
          </div>

          <!-- Последние заявки -->
          <div class="px-6 py-5">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
              Последние заявки
            </h3>
            <div class="bg-white shadow overflow-hidden sm:rounded-md">
              <div class="p-4 text-center text-gray-500">
                Пока нет заявок
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const handleLogout = async () => {
  // Очищаем данные администратора
  localStorage.removeItem('admin_token')
  localStorage.removeItem('is_admin')
  
  // Перенаправляем на страницу входа
  await router.push('/admin')
}
</script> 