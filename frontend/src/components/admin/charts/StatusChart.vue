<template>
  <div class="bg-white p-4 rounded-lg shadow">
    <h3 class="text-lg font-medium mb-4">Распределение по статусам</h3>
    <div class="h-48">
      <canvas ref="chartRef"></canvas>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { Chart } from 'chart.js/auto';

const props = defineProps<{
  labels: string[];
  data: number[];
}>();

const chartRef = ref<HTMLCanvasElement | null>(null);
let chart: Chart | null = null;

const statusLabels = {
  new: 'Новые',
  in_progress: 'В работе',
  resolved: 'Решены',
  closed: 'Закрыты'
};

const statusColors = {
  new: '#3b82f6',
  in_progress: '#f59e0b',
  resolved: '#10b981',
  closed: '#6b7280'
};

function createChart() {
  if (!chartRef.value) return;

  chart?.destroy();
  chart = new Chart(chartRef.value, {
    type: 'bar',
    data: {
      labels: props.labels.map(status => statusLabels[status as keyof typeof statusLabels]),
      datasets: [{
        data: props.data,
        backgroundColor: props.labels.map(status => statusColors[status as keyof typeof statusColors]),
        barThickness: 30,
        maxBarThickness: 35
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            precision: 0,
            font: { size: 11 }
          }
        },
        x: {
          ticks: {
            font: { size: 11 }
          }
        }
      },
      layout: {
        padding: {
          left: 10,
          right: 10,
          top: 10,
          bottom: 10
        }
      }
    }
  });
}

watch(() => [props.labels, props.data], createChart, { deep: true });
onMounted(createChart);
</script>