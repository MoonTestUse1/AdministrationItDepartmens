<template>
  <div class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center">
    <div class="bg-white rounded-lg p-6 max-w-md w-full">
      <h3 class="text-lg font-semibold mb-4">Изменение статуса заявки</h3>

      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Текущий статус
        </label>
        <RequestStatusBadge :status="currentStatus" />
      </div>

      <div class="space-y-3">
        <label class="block text-sm font-medium text-gray-700">
          Выберите новый статус
        </label>
        <div class="space-y-2">
          <button
            v-for="status in allStatuses"
            :key="status"
            @click="handleStatusSelect(status)"
            :disabled="status === currentStatus"
            :class="[
              'w-full text-left px-4 py-2 rounded-md border transition-colors',
              status === currentStatus
                ? 'border-gray-200 bg-gray-50 cursor-not-allowed'
                : 'border-gray-200 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500'
            ]"
          >
            <RequestStatusBadge :status="status" />
          </button>
        </div>
      </div>

      <div class="flex justify-end space-x-3 mt-6">
        <button
          @click="$emit('close')"
          class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
        >
          Отмена
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import RequestStatusBadge from './RequestStatusBadge.vue';
import type { RequestStatus } from '@/types/request';

const props = defineProps<{
  currentStatus: RequestStatus;
}>();

const emit = defineEmits(['close', 'update']);

const allStatuses: RequestStatus[] = ['new', 'in_progress', 'resolved', 'closed'];

function handleStatusSelect(newStatus: RequestStatus) {
  if (newStatus === props.currentStatus) return;
  emit('update', newStatus);
  emit('close');
}
</script>