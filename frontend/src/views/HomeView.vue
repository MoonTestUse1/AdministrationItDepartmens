<template>
  <div class="min-h-screen bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center p-4">
    <div class="max-w-md w-full bg-white rounded-xl shadow-2xl p-8">
      <div class="text-center">
        <h1 class="text-4xl font-bold text-gray-900 mb-2">IT Support Portal</h1>
        <p class="text-lg text-gray-600 mb-8">Система поддержки IT департамента</p>
      </div>

      <div class="space-y-4">
        <router-link 
          to="/login" 
          class="block w-full py-3 px-4 text-center text-white bg-indigo-600 hover:bg-indigo-700 rounded-lg transition-colors duration-200 font-medium shadow-md hover:shadow-lg"
        >
          Вход для сотрудников
        </router-link>

        <router-link 
          to="/admin/login" 
          class="block w-full py-3 px-4 text-center text-indigo-700 bg-indigo-100 hover:bg-indigo-200 rounded-lg transition-colors duration-200 font-medium border-2 border-indigo-200"
        >
          Вход для администраторов
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Очищаем токены при входе на главную страницу
localStorage.removeItem('token')
localStorage.removeItem('admin_token')
localStorage.removeItem('employee')
localStorage.removeItem('is_admin')
</script> 