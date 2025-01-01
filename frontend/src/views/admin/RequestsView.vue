<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold">Заявки</h1>
    
    <!-- Requests table -->
    <div class="bg-white rounded-lg shadow">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Сотрудник</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Тип</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Статус</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Дата</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="request in requests" :key="request.id">
              <td class="px-6 py-4 whitespace-nowrap">{{ request.id }}</td>
              <td class="px-6 py-4 whitespace-nowrap">{{ request.employee_last_name }}</td>
              <td class="px-6 py-4 whitespace-nowrap">{{ getRequestTypeLabel(request.request_type) }}</td>
              <td class="px-6 py-4 whitespace-nowrap">{{ getStatusLabel(request.status) }}</td>
              <td class="px-6 py-4 whitespace-nowrap">{{ formatDate(request.created_at) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useRequests } from '@/composables/useRequests';
import { getRequestTypeLabel, getStatusLabel } from '@/utils/labels';

const { requests, fetchRequests } = useRequests();

const formatDate = (date: string) => {
  return new Date(date).toLocaleString('ru-RU');
};

onMounted(() => {
  fetchRequests();
});
</script> 