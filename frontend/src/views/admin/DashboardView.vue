<template>
  <div class="container mx-auto px-4 py-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Панель администратора</h1>
      <button
        @click="handleLogout"
        class="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 transition-colors"
      >
        Выйти
      </button>
    </div>

    <div class="bg-white rounded-lg shadow-lg p-6">
      <div class="border-b border-gray-200">
        <nav class="-mb-px flex space-x-8">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="currentTab = tab.id"
            :class="[
              currentTab === tab.id
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
              'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm'
            ]"
          >
            {{ tab.name }}
          </button>
        </nav>
      </div>

      <div class="mt-6">
        <StatisticsPanel v-if="currentTab === 'statistics'" />
        <RequestList v-if="currentTab === 'requests'" />
        <EmployeeList v-if="currentTab === 'employees'" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import RequestList from '@/components/admin/RequestList.vue';
import EmployeeList from '@/components/admin/EmployeeList.vue';
import StatisticsPanel from '@/components/admin/StatisticsPanel.vue';

const router = useRouter();
const authStore = useAuthStore();

const tabs = [
  { id: 'statistics', name: 'Статистика' },
  { id: 'requests', name: 'Заявки' },
  { id: 'employees', name: 'Сотрудники' }
];

const currentTab = ref('statistics');

function handleLogout() {
  authStore.logout();
  router.push('/admin');
}
</script>