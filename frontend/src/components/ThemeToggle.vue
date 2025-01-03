<template>
  <button
    @click="toggleTheme"
    class="p-2 rounded-lg hover:bg-opacity-20 hover:bg-gray-500 transition-colors"
    :title="isDark ? 'Переключить на светлую тему' : 'Переключить на темную тему'"
  >
    <!-- Иконка солнца для светлой темы -->
    <svg
      v-if="isDark"
      class="w-6 h-6 text-yellow-400"
      fill="none"
      stroke="currentColor"
      viewBox="0 0 24 24"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
      />
    </svg>
    <!-- Иконка луны для темной темы -->
    <svg
      v-else
      class="w-6 h-6 text-gray-600"
      fill="none"
      stroke="currentColor"
      viewBox="0 0 24 24"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
      />
    </svg>
  </button>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const isDark = ref(false)

// Функция переключения темы
const toggleTheme = () => {
  isDark.value = !isDark.value
  updateTheme()
}

// Функция обновления темы
const updateTheme = () => {
  // Обновляем атрибут data-theme на html элементе
  document.documentElement.setAttribute('data-theme', isDark.value ? 'dark' : 'light')
  // Сохраняем выбор в localStorage
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
}

// При монтировании компонента
onMounted(() => {
  // Проверяем сохраненную тему
  const savedTheme = localStorage.getItem('theme')
  // Проверяем системные настройки
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
  
  // Устанавливаем тему
  isDark.value = savedTheme ? savedTheme === 'dark' : prefersDark
  updateTheme()
})
</script> 