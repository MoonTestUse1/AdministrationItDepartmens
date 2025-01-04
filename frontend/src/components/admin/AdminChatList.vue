<template>
  <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-lg">
    <div class="p-6 border-b border-gray-200 dark:border-gray-700">
      <h2 class="text-xl font-bold text-gray-800 dark:text-white">Чаты сотрудников</h2>
    </div>

    <!-- Список чатов -->
    <div class="divide-y divide-gray-200 dark:divide-gray-700">
      <div
        v-for="chat in chats"
        :key="chat.id"
        class="p-4 hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer transition-colors"
        :class="{ 'bg-blue-50 dark:bg-blue-900/30': selectedChatId === chat.id }"
        @click="$emit('select-chat', chat)"
      >
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <!-- Аватар -->
            <div class="w-10 h-10 rounded-full bg-gray-200 dark:bg-gray-600 flex items-center justify-center">
              <span class="text-gray-600 dark:text-gray-300 font-medium">
                {{ getInitials(chat.employee.full_name) }}
              </span>
            </div>

            <!-- Информация -->
            <div>
              <h3 class="font-medium text-gray-900 dark:text-white">
                {{ chat.employee.full_name }}
              </h3>
              <p class="text-sm text-gray-500 dark:text-gray-400">
                {{ chat.last_message ? truncateMessage(chat.last_message.content) : 'Нет сообщений' }}
              </p>
            </div>
          </div>

          <!-- Индикаторы -->
          <div class="flex flex-col items-end space-y-1">
            <!-- Время последнего сообщения -->
            <span v-if="chat.last_message" class="text-xs text-gray-500 dark:text-gray-400">
              {{ formatTime(chat.last_message.created_at) }}
            </span>
            
            <!-- Непрочитанные сообщения -->
            <span
              v-if="chat.unread_count > 0"
              class="bg-blue-500 text-white text-xs font-bold px-2 py-0.5 rounded-full"
            >
              {{ chat.unread_count }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Пустое состояние -->
    <div
      v-if="chats.length === 0"
      class="p-8 text-center"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
      </svg>
      <p class="mt-4 text-gray-500 dark:text-gray-400">
        Нет активных чатов
      </p>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  chats: {
    type: Array,
    required: true
  },
  selectedChatId: {
    type: Number,
    default: null
  }
})

defineEmits(['select-chat'])

// Получение инициалов из полного имени
const getInitials = (fullName) => {
  return fullName
    .split(' ')
    .map(name => name[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

// Форматирование времени
const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  const now = new Date()
  const yesterday = new Date(now)
  yesterday.setDate(yesterday.getDate() - 1)

  if (date.toDateString() === now.toDateString()) {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  } else if (date.toDateString() === yesterday.toDateString()) {
    return 'Вчера'
  } else {
    return date.toLocaleDateString()
  }
}

// Обрезка длинных сообщений
const truncateMessage = (message, length = 50) => {
  if (message.length <= length) return message
  return message.slice(0, length) + '...'
}
</script> 