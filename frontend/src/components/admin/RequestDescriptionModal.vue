<template>
  <div class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center">
    <div class="bg-white rounded-lg p-6 max-w-2xl w-full mx-4">
      <div class="flex justify-between items-start mb-4">
        <h3 class="text-lg font-semibold">Описание заявки №{{ request.id }}</h3>
        <button
          @click="$emit('close')"
          class="text-gray-400 hover:text-gray-500"
        >
          <XIcon :size="20" />
        </button>
      </div>
      
      <div class="space-y-4">
        <div class="grid grid-cols-2 gap-4 text-sm">
          <div>
            <span class="text-gray-500">Сотрудник:</span>
            <p>{{ request.employee_last_name }} {{ request.employee_first_name }}</p>
          </div>
          <div>
            <span class="text-gray-500">Кабинет:</span>
            <p>{{ request.employee_office }}</p>
          </div>
          <div>
            <span class="text-gray-500">Тип заявки:</span>
            <p>{{ getRequestTypeLabel(request.request_type) }}</p>
          </div>
          <div>
            <span class="text-gray-500">Приоритет:</span>
            <RequestPriorityBadge :priority="request.priority" />
          </div>
        </div>

        <div>
          <span class="text-gray-500">Описание проблемы:</span>
          <p class="mt-2 text-gray-700 whitespace-pre-wrap">{{ request.description }}</p>
        </div>
      </div>

      <div class="mt-6 flex justify-end">
        <button
          @click="$emit('close')"
          class="px-4 py-2 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200"
        >
          Закрыть
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { XIcon } from 'lucide-vue-next';
import { getRequestTypeLabel } from '@/utils/constants';
import RequestPriorityBadge from './RequestPriorityBadge.vue';

defineProps<{
  request: any;
}>();

defineEmits<{
  (e: 'close'): void;
}>();
</script>