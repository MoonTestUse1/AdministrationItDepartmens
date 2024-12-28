<template>
  <Transition
    enter-active-class="transform ease-out duration-300 transition"
    enter-from-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2"
    enter-to-class="translate-y-0 opacity-100 sm:translate-x-0"
    leave-active-class="transition ease-in duration-100"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
  >
    <div
      v-if="show"
      class="fixed top-4 right-4 z-50 max-w-sm w-full bg-white rounded-lg shadow-lg ring-1 ring-black ring-opacity-5 overflow-hidden"
      :class="{
        'bg-green-50 ring-green-500': type === 'success',
        'bg-red-50 ring-red-500': type === 'error'
      }"
    >
      <div class="p-4">
        <div class="flex items-start">
          <div class="flex-shrink-0">
            <component 
              :is="type === 'error' ? XCircleIcon : CheckCircleIcon"
              class="h-5 w-5"
              :class="type === 'error' ? 'text-red-400' : 'text-green-400'"
            />
          </div>
          <div class="ml-3 w-0 flex-1 pt-0.5">
            <p class="text-sm font-medium" :class="type === 'error' ? 'text-red-800' : 'text-green-800'">
              {{ message }}
            </p>
          </div>
          <div class="ml-4 flex-shrink-0 flex">
            <button
              @click="$emit('close')"
              class="inline-flex rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2"
              :class="type === 'error' ? 'text-red-500 hover:text-red-600 focus:ring-red-500' : 'text-green-500 hover:text-green-600 focus:ring-green-500'"
            >
              <XIcon class="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { CheckCircleIcon, XIcon, XCircleIcon } from 'lucide-vue-next';

withDefaults(defineProps<{
  show: boolean;
  message: string;
  type?: 'success' | 'error';
}>(), {
  type: 'success'
});

defineEmits<{
  (e: 'close'): void;
}>();
</script>