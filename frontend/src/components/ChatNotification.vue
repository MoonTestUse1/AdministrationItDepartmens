<template>
  <Transition
    enter-active-class="transform ease-out duration-300 transition"
    enter-from-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2"
    enter-to-class="translate-y-0 opacity-100 sm:translate-x-0"
    leave-active-class="transition ease-in duration-200"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
  >
    <div v-if="show" class="fixed bottom-4 right-4 z-50">
      <div class="max-w-sm w-full bg-white dark:bg-gray-800 shadow-lg rounded-lg pointer-events-auto ring-1 ring-black ring-opacity-5">
        <div class="p-4">
          <div class="flex items-start">
            <div class="flex-shrink-0">
              <svg class="h-6 w-6 text-blue-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
            </div>
            <div class="ml-3 w-0 flex-1">
              <p class="text-sm font-medium text-gray-900 dark:text-white">
                {{ title }}
              </p>
              <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
                {{ message }}
              </p>
              <div class="mt-3 flex space-x-4">
                <button
                  type="button"
                  @click="$emit('action')"
                  class="bg-blue-500 hover:bg-blue-600 text-white text-sm px-3 py-1.5 rounded-md transition-colors"
                >
                  Открыть чат
                </button>
                <button
                  type="button"
                  @click="$emit('close')"
                  class="bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600 text-sm px-3 py-1.5 rounded-md transition-colors"
                >
                  Закрыть
                </button>
              </div>
            </div>
            <div class="ml-4 flex-shrink-0 flex">
              <button
                @click="$emit('close')"
                class="rounded-md inline-flex text-gray-400 hover:text-gray-500 focus:outline-none"
              >
                <span class="sr-only">Закрыть</span>
                <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
defineProps({
  show: {
    type: Boolean,
    required: true
  },
  title: {
    type: String,
    default: 'Новое сообщение'
  },
  message: {
    type: String,
    required: true
  }
})

defineEmits(['close', 'action'])
</script> 