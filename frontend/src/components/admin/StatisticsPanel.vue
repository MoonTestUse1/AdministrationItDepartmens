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
    <div class="grid grid-cols-1 sm:grid-cols-4 gap-4">
      <div class="bg-white p-4 rounded-lg shadow">
        <div class="text-sm text-gray-500">Всего заявок</div>
        <div class="text-2xl font-semibold mt-1">{{ statistics.total || 0 }}</div>
      </div>
      <div class="bg-white p-4 rounded-lg shadow">
        <div class="text-sm text-gray-500">Новые заявки</div>
        <div class="text-2xl font-semibold mt-1 text-blue-600">{{ statistics.by_status?.new || 0 }}</div>
      </div>
      <div class="bg-white p-4 rounded-lg shadow">
        <div class="text-sm text-gray-500">В работе</div>
        <div class="text-2xl font-semibold mt-1 text-yellow-600">{{ statistics.by_status?.in_progress || 0 }}</div>
      </div>
      <div class="bg-white p-4 rounded-lg shadow">
        <div class="text-sm text-gray-500">Завершенные</div>
        <div class="text-2xl font-semibold mt-1 text-green-600">{{ statistics.by_status?.completed || 0 }}</div>
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
import { ref, onMounted, onUnmounted, watch } from 'vue';
import axios from '@/plugins/axios';
import { wsClient } from '@/plugins/websocket';
import VolumeChart from './charts/VolumeChart.vue';
import TypesChart from './charts/TypesChart.vue';
import StatusChart from './charts/StatusChart.vue';

const period = ref('week');
const statistics = ref({
  total: 0,
  by_status: {
    new: 0,
    in_progress: 0,
    completed: 0
  }
});
const chartData = ref({
  volumeLabels: [],
  volumeData: [],
  typeLabels: [],
  typeData: [],
  statusLabels: [],
  statusData: []
});

const periodOptions = [
  { value: 'day', label: 'День' },
  { value: 'week', label: 'Неделя' },
  { value: 'month', label: 'Месяц' }
];

// Загрузка статистики
const fetchStatistics = async () => {
  try {
    console.log('StatisticsPanel: Fetching statistics');
    const [statsResponse, chartsResponse] = await Promise.all([
      axios.get('/api/requests/statistics'),
      axios.get(`/api/statistics?period=${period.value}`)
    ]);
    console.log('StatisticsPanel: Received statistics:', statsResponse.data);
    
    // Принудительно обновляем реактивное состояние
    statistics.value = {
      total: statsResponse.data.total,
      by_status: statsResponse.data.by_status || {}
    };
    chartData.value = chartsResponse.data;
  } catch (error) {
    console.error('Error fetching statistics:', error);
  }
};

// Обработчик WebSocket сообщений
const handleWebSocketMessage = (data: any) => {
  console.log('StatisticsPanel: Received WebSocket message:', data);
  
  if (data.type === 'new_request' || data.type === 'status_update') {
    if (data.statistics) {
      console.log('StatisticsPanel: Old statistics:', statistics.value);
      console.log('StatisticsPanel: Updating statistics:', data.statistics);
      
      // Принудительно обновляем реактивное состояние
      statistics.value = {
        total: data.statistics.total,
        by_status: data.statistics.by_status || {}
      };
      
      console.log('StatisticsPanel: New statistics:', statistics.value);
    }
  }
};

watch(period, () => {
  console.log('StatisticsPanel: Period changed, fetching new data');
  fetchStatistics();
});

onMounted(() => {
  console.log('StatisticsPanel: Component mounted');
  fetchStatistics();
  
  // Подключаемся к WebSocket
  setTimeout(() => {
    console.log('StatisticsPanel: Adding WebSocket handler');
    wsClient.addMessageHandler(handleWebSocketMessage);
  }, 1000);
});

onUnmounted(() => {
  console.log('StatisticsPanel: Component unmounting');
  wsClient.removeMessageHandler(handleWebSocketMessage);
});
</script>