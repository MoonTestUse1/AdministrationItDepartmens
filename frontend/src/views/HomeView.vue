<template>
  <div class="text-center">
    <h1 class="text-4xl font-bold text-gray-900 mb-8">
      Добро пожаловать в IT Form Help
    </h1>
    <p class="text-xl text-gray-600 mb-8">
      Система поддержки и обработки IT-заявок
    </p>
    <div class="space-x-4">
      <router-link
        to="/login"
        class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
      >
        Войти как сотрудник
      </router-link>
      <router-link
        to="/admin/login"
        class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-indigo-600 bg-white hover:bg-gray-50"
      >
        Войти как администратор
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
// Главная страница
</script> 