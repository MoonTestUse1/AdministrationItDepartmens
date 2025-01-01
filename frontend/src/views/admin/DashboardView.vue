```vue
<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold">Панель администратора</h1>
    </div>

    <!-- Statistics -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <div v-for="stat in statisticsCards" :key="stat.period" class="bg-white p-4 rounded-lg shadow">
        <h3 class="text-lg font-semibold">{{ stat.label }}</h3>
        <p class="text-2xl font-bold">{{ stat.value }}</p>
      </div>
    </div>

    <!-- Requests -->
    <div class="bg-white rounded-lg shadow">
      <div class="p-4">
        <h2 class="text-xl font-semibold">Последние заявки</h2>
      </div>
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
import { useStatistics } from '@/composables/useStatistics';
import { getRequestTypeLabel, getStatusLabel } from '@/utils/labels';

const { requests, fetchRequests } = useRequests();
const { statisticsCards, fetchStatistics } = useStatistics();

const formatDate = (date: string) => {
  return new Date(date).toLocaleString('ru-RU');
};

onMounted(() => {
  fetchStatistics();
  fetchRequests();
});
</script>
```