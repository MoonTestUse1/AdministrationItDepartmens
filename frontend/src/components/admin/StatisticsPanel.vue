<template>
  <div class="space-y-6">
    <!-- Period selector -->
    <div class="flex justify-between items-center">
      <div class="flex gap-4">
        <button
          v-for="option in periodOptions"
          :key="option.value"
          @click="period = option.value"
          :class="[
            'px-3 py-1 rounded-md text-sm',
            period === option.value
              ? 'bg-blue-600 text-white'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          ]"
        >
          {{ option.label }}
        </button>
      </div>
    </div>

    <!-- Summary cards -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <div
        v-for="stat in summaryStats"
        :key="stat.label"
        class="bg-white p-4 rounded-lg shadow"
      >
        <div class="text-sm text-gray-500">{{ stat.label }}</div>
        <div class="text-2xl font-semibold mt-1">{{ stat.value }}</div>
      </div>
    </div>

    <!-- Charts -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <VolumeChart
        :labels="chartData.volumeLabels"
        :data="chartData.volumeData"
      />
      <TypesChart
        :labels="chartData.typeLabels"
        :data="chartData.typeData"
      />
      <StatusChart
        :labels="chartData.statusLabels"
        :data="chartData.statusData"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue';
import VolumeChart from './charts/VolumeChart.vue';
import TypesChart from './charts/TypesChart.vue';
import StatusChart from './charts/StatusChart.vue';

const period = ref('week');
const chartData = ref({
  volumeLabels: [],
  volumeData: [],
  typeLabels: [],
  typeData: [],
  statusLabels: [],
  statusData: [],
  totalRequests: 0,
  resolvedRequests: 0,
  averageResolutionTime: '0ч'
});

const periodOptions = [
  { value: 'day', label: 'День' },
  { value: 'week', label: 'Неделя' },
  { value: 'month', label: 'Месяц' }
];

const summaryStats = computed(() => [
  { label: 'Всего заявок', value: chartData.value.totalRequests },
  { label: 'Решено за период', value: chartData.value.resolvedRequests },
  { label: 'Среднее время решения', value: chartData.value.averageResolutionTime }
]);

async function fetchStatistics() {
  try {
    const response = await fetch(`/api/statistics?period=${period.value}`);
    if (!response.ok) throw new Error('Failed to fetch statistics');
    chartData.value = await response.json();
  } catch (error) {
    console.error('Error fetching statistics:', error);
  }
}

watch(period, fetchStatistics);
onMounted(fetchStatistics);
</script>