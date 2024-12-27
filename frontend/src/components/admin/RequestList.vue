<template>
  <div class="space-y-4">
    <div class="flex justify-between items-center">
      <h2 class="text-lg font-semibold">Заявки</h2>
      <div class="flex gap-4">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Поиск по фамилии..."
          class="px-3 py-1 border rounded-md"
          @input="handleSearch"
        />
        <select v-model="filter" class="px-3 py-1 border rounded-md" @change="handleFilter">
          <option value="all">Все заявки</option>
          <option value="new">Новые</option>
          <option value="in_progress">В работе</option>
          <option value="resolved">Решенные</option>
          <option value="closed">Закрытые</option>
        </select>
      </div>
    </div>

    <div class="bg-white rounded-lg shadow overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">№</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Дата</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Сотрудник</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Кабинет</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Тип</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Приоритет</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Статус</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Действия</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr 
            v-for="request in filteredRequests" 
            :key="request.id"
            class="hover:bg-gray-50"
          >
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              {{ request.id }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              {{ formatDate(request.created_at) }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              {{ request.employee_last_name }} {{ request.employee_first_name }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              {{ request.employee_office }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              <button 
                @click="showDescription(request)"
                class="text-blue-600 hover:text-blue-900"
              >
                {{ getRequestTypeLabel(request.request_type) }}
              </button>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <RequestPriorityBadge :priority="request.priority" />
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <RequestStatusBadge :status="request.status" />
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <button 
                @click="openStatusModal(request)"
                class="text-blue-600 hover:text-blue-900"
              >
                Изменить статус
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Description modal -->
    <RequestDescriptionModal
      v-if="selectedDescription"
      :request="selectedDescription"
      @close="selectedDescription = null"
    />

    <!-- Status update modal -->
    <RequestStatusModal
      v-if="selectedRequest"
      :current-status="selectedRequest.status"
      @close="selectedRequest = null"
      @update="handleStatusUpdate"
    />

    <!-- Success notification -->
    <Notification
      :show="showNotification"
      message="Статус заявки успешно обновлен"
      @close="showNotification = false"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import type { Request } from '@/types/request';
import RequestStatusBadge from './RequestStatusBadge.vue';
import RequestPriorityBadge from './RequestPriorityBadge.vue';
import RequestStatusModal from './RequestStatusModal.vue';
import RequestDescriptionModal from './RequestDescriptionModal.vue';
import Notification from '@/components/ui/Notification.vue';
import { getRequestTypeLabel } from '@/utils/constants';
const requests = ref<Request[]>([]); // Типизируем массив запросов
const selectedRequest = ref<Request | null>(null);
const selectedDescription = ref<Request | null>(null);
const showNotification = ref(false);
const filter = ref('all');
const searchQuery = ref('');

const filteredRequests = computed(() => {
  let result = requests.value;
  
  if (searchQuery.value) {
    result = result.filter(request => 
      request.employee_last_name.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
  }
  
  if (filter.value !== 'all') {
    result = result.filter(request => request.status === filter.value);
  }
  
  return result;
});


function formatDate(date: string) {
  return new Date(date).toLocaleString('ru-RU');
}

function openStatusModal(request: any) {
  selectedRequest.value = request;
}

function showDescription(request: any) {
  selectedDescription.value = request;
}

async function handleStatusUpdate(newStatus: string) {
  if (!selectedRequest.value) return;

  try {
    const response = await fetch(`/api/requests/${selectedRequest.value.id}/status`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: newStatus })
    });
    
    if (!response.ok) {
      throw new Error('Failed to update status');
    }
    
    await fetchRequests();
    selectedRequest.value = null;
    showNotification.value = true;
    
    setTimeout(() => {
      showNotification.value = false;
    }, 3000);
  } catch (error) {
    console.error('Error updating status:', error);
    alert('Не удалось обновить статус');
  }
}

async function fetchRequests() {
  try {
    const response = await fetch('/api/requests/');
    if (!response.ok) throw new Error('Failed to fetch requests');
    requests.value = await response.json();
  } catch (error) {
    console.error('Error fetching requests:', error);
    alert('Не удалось загрузить заявки');
  }
}

function handleSearch() {
  // Debounce could be added here if needed
}

function handleFilter() {
  // Additional filter logic if needed
}

onMounted(fetchRequests);
</script>