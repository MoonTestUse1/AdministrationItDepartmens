<template>
  <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-lg flex flex-col h-full">
    <!-- Заголовок -->
    <div class="p-6 border-b border-gray-200 dark:border-gray-700">
      <div v-if="chat" class="flex items-center space-x-3">
        <!-- Аватар -->
        <div class="w-10 h-10 rounded-full bg-gray-200 dark:bg-gray-600 flex items-center justify-center">
          <span class="text-gray-600 dark:text-gray-300 font-medium">
            {{ getInitials(chat.employee.full_name) }}
          </span>
        </div>

        <!-- Информация о сотруднике -->
        <div>
          <h2 class="text-lg font-bold text-gray-800 dark:text-white">
            {{ chat.employee.full_name }}
          </h2>
          <p class="text-sm text-gray-500 dark:text-gray-400">
            {{ chat.employee.email }}
          </p>
        </div>
      </div>
      <div v-else class="text-center text-gray-500 dark:text-gray-400">
        Выберите чат для начала общения
      </div>
    </div>

    <!-- Область сообщений -->
    <div v-if="chat" class="flex-1 overflow-y-auto p-6 space-y-4" ref="messagesContainer">
      <template v-for="(messageGroup, date) in groupedMessages" :key="date">
        <!-- Дата -->
        <div class="flex justify-center">
          <span class="bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 text-sm px-3 py-1 rounded-full">
            {{ formatDate(date) }}
          </span>
        </div>

        <!-- Сообщения за день -->
        <div v-for="message in messageGroup" :key="message.id" class="flex flex-col space-y-2">
          <div :class="[
            'flex max-w-[80%] space-x-2',
            message.sender_id === currentUserId ? 'ml-auto' : 'mr-auto'
          ]">
            <!-- Сообщение -->
            <div :class="[
              'rounded-2xl px-4 py-2 break-words',
              message.sender_id === currentUserId 
                ? 'bg-blue-500 text-white ml-auto' 
                : 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-white'
            ]">
              <p>{{ message.content }}</p>
              
              <!-- Файлы -->
              <div v-if="message.files && message.files.length > 0" class="mt-2 space-y-1">
                <div v-for="file in message.files" :key="file.id" 
                  class="flex items-center space-x-2 text-sm"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                  </svg>
                  <a :href="file.file_path" 
                    download
                    class="hover:underline"
                  >
                    {{ file.file_name }}
                  </a>
                </div>
              </div>

              <!-- Время и статус -->
              <div class="flex items-center justify-end mt-1 space-x-1">
                <span class="text-xs opacity-75">
                  {{ formatTime(message.created_at) }}
                </span>
                <span v-if="message.sender_id === currentUserId">
                  <svg v-if="message.is_read" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                  </svg>
                </span>
              </div>
            </div>
          </div>
        </div>
      </template>
    </div>

    <!-- Форма отправки -->
    <div v-if="chat" class="p-6 border-t border-gray-200 dark:border-gray-700">
      <form @submit.prevent="sendMessage" class="flex flex-col space-y-4">
        <!-- Область ввода -->
        <div class="flex space-x-4">
          <div class="flex-1 relative">
            <textarea
              v-model="newMessage"
              @keydown.enter.exact.prevent="sendMessage"
              rows="1"
              class="w-full rounded-xl border-gray-200 dark:border-gray-700 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:text-white resize-none"
              placeholder="Введите сообщение..."
            ></textarea>
            <!-- Эмодзи -->
            <div class="absolute right-3 bottom-3">
              <button
                type="button"
                @click="showEmoji = !showEmoji"
                class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM7 9a1 1 0 100-2 1 1 0 000 2zm7-1a1 1 0 11-2 0 1 1 0 012 0zm-7.536 5.879a1 1 0 001.415 0 3 3 0 014.242 0 1 1 0 001.415-1.415 5 5 0 00-7.072 0 1 1 0 000 1.415z" clip-rule="evenodd" />
                </svg>
              </button>
              <!-- Панель эмодзи -->
              <div v-if="showEmoji" class="absolute bottom-full right-0 mb-2 bg-white dark:bg-gray-800 rounded-lg shadow-xl border border-gray-200 dark:border-gray-700 p-2">
                <div class="grid grid-cols-8 gap-1">
                  <button
                    v-for="emoji in emojis"
                    :key="emoji"
                    type="button"
                    @click="addEmoji(emoji)"
                    class="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded"
                  >
                    {{ emoji }}
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Кнопки -->
          <div class="flex space-x-2">
            <!-- Загрузка файла -->
            <label class="cursor-pointer">
              <input
                type="file"
                ref="fileInput"
                @change="handleFileUpload"
                class="hidden"
                multiple
              >
              <div class="w-10 h-10 flex items-center justify-center rounded-full bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-600 dark:text-gray-300" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M8 4a3 3 0 00-3 3v4a5 5 0 0010 0V7a1 1 0 112 0v4a7 7 0 11-14 0V7a5 5 0 0110 0v4a3 3 0 11-6 0V7a1 1 0 012 0v4a1 1 0 102 0V7a3 3 0 00-3-3z" clip-rule="evenodd" />
                </svg>
              </div>
            </label>

            <!-- Отправка -->
            <button
              type="submit"
              :disabled="!newMessage.trim() && !selectedFiles.length"
              class="w-10 h-10 flex items-center justify-center rounded-full bg-blue-500 hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Предпросмотр файлов -->
        <div v-if="selectedFiles.length" class="flex flex-wrap gap-2">
          <div
            v-for="(file, index) in selectedFiles"
            :key="index"
            class="flex items-center space-x-2 bg-gray-100 dark:bg-gray-700 rounded-lg px-3 py-1"
          >
            <span class="text-sm text-gray-600 dark:text-gray-300 truncate max-w-[200px]">
              {{ file.name }}
            </span>
            <button
              type="button"
              @click="removeFile(index)"
              class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, nextTick, watch } from 'vue'

const props = defineProps({
  chat: {
    type: Object,
    default: null
  },
  currentUserId: {
    type: Number,
    required: true
  }
})

// Состояние
const messages = ref([])
const newMessage = ref('')
const selectedFiles = ref([])
const showEmoji = ref(false)
const messagesContainer = ref(null)
const ws = ref(null)
const reconnectAttempts = ref(0)
const maxReconnectAttempts = 5

// Эмодзи
const emojis = ['😊', '👍', '❤️', '😂', '🙏', '😭', '🎉', '🔥', '👋', '😉', '🤔', '👌', '😍', '💪', '🙌', '✨']

// Группировка сообщений по датам
const groupedMessages = computed(() => {
  const groups = {}
  messages.value.forEach(message => {
    const date = new Date(message.created_at).toLocaleDateString()
    if (!groups[date]) {
      groups[date] = []
    }
    groups[date].push(message)
  })
  return groups
})

// Получение инициалов
const getInitials = (fullName) => {
  return fullName
    .split(' ')
    .map(name => name[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

// Форматирование даты
const formatDate = (date) => {
  const today = new Date().toLocaleDateString()
  const yesterday = new Date(Date.now() - 86400000).toLocaleDateString()

  if (date === today) return 'Сегодня'
  if (date === yesterday) return 'Вчера'
  return date
}

// Форматирование времени
const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

// WebSocket подключение
const connectWebSocket = () => {
  if (!props.chat) return

  const token = localStorage.getItem('token')
  ws.value = new WebSocket(`ws://${window.location.host}/api/ws/chat?token=${token}`)

  ws.value.onmessage = (event) => {
    const data = JSON.parse(event.data)
    
    if (data.type === 'message') {
      messages.value.push(data)
      scrollToBottom()
    } else if (data.type === 'read_confirmation') {
      // Обновляем статус прочтения
      data.message_ids.forEach(id => {
        const message = messages.value.find(m => m.id === id)
        if (message) {
          message.is_read = true
        }
      })
    }
  }

  ws.value.onclose = () => {
    if (reconnectAttempts.value < maxReconnectAttempts) {
      setTimeout(() => {
        reconnectAttempts.value++
        connectWebSocket()
      }, 1000 * Math.min(reconnectAttempts.value + 1, 30))
    }
  }
}

// Отправка сообщения
const sendMessage = async () => {
  if (!newMessage.value.trim() && !selectedFiles.value.length) return

  try {
    // Загружаем файлы, если есть
    const uploadedFiles = []
    if (selectedFiles.value.length) {
      for (const file of selectedFiles.value) {
        const formData = new FormData()
        formData.append('file', file)
        
        const response = await fetch('/api/chat/files/', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: formData
        })
        
        if (response.ok) {
          const fileData = await response.json()
          uploadedFiles.push(fileData)
        }
      }
    }

    // Отправляем сообщение через WebSocket
    ws.value.send(JSON.stringify({
      type: 'message',
      content: newMessage.value,
      files: uploadedFiles
    }))

    // Очищаем форму
    newMessage.value = ''
    selectedFiles.value = []
    showEmoji.value = false
  } catch (error) {
    console.error('Error sending message:', error)
  }
}

// Загрузка файлов
const handleFileUpload = (event) => {
  const files = Array.from(event.target.files)
  selectedFiles.value.push(...files)
  event.target.value = '' // Сброс input
}

// Удаление файла
const removeFile = (index) => {
  selectedFiles.value.splice(index, 1)
}

// Добавление эмодзи
const addEmoji = (emoji) => {
  newMessage.value += emoji
}

// Прокрутка к последнему сообщению
const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// Загрузка истории сообщений
const loadMessages = async () => {
  if (!props.chat) return

  try {
    const response = await fetch(`/api/chat/messages/${props.chat.id}/`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    if (response.ok) {
      messages.value = await response.json()
      await scrollToBottom()

      // Отмечаем сообщения как прочитанные
      const unreadMessages = messages.value
        .filter(m => !m.is_read && m.sender_id !== props.currentUserId)
        .map(m => m.id)

      if (unreadMessages.length > 0) {
        ws.value.send(JSON.stringify({
          type: 'read',
          message_ids: unreadMessages
        }))
      }
    }
  } catch (error) {
    console.error('Error loading messages:', error)
  }
}

// Следим за изменением чата
watch(() => props.chat, async (newChat) => {
  if (ws.value) {
    ws.value.close()
  }
  
  if (newChat) {
    messages.value = []
    await loadMessages()
    connectWebSocket()
  }
}, { immediate: true })

// Очистка при размонтировании
onUnmounted(() => {
  if (ws.value) {
    ws.value.close()
  }
})
</script> 