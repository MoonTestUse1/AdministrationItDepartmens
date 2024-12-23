<template>
  <div class="bg-white p-4 rounded-lg shadow">
    <h3 class="text-lg font-medium mb-4">Типы заявок</h3>
    <div class="h-48">
      <canvas ref="chartRef"></canvas>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { Chart } from 'chart.js/auto';
import { getRequestTypeLabel } from '@/utils/constants';

const props = defineProps<{
  labels: string[];
  data: number[];
}>();

const chartRef = ref<HTMLCanvasElement | null>(null);
let chart: Chart | null = null;

const colors = [
  '#3b82f6',
  '#10b981',
  '#f59e0b',
  '#ef4444',
  '#8b5cf6'
];

function createChart() {
  if (!chartRef.value) return;

  chart?.destroy();
  chart = new Chart(chartRef.value, {
    type: 'doughnut',
    data: {
      labels: props.labels.map(getRequestTypeLabel),
      datasets: [{
        data: props.data,
        backgroundColor: colors
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'right',
          labels: {
            font: {
              size: 11
            }
          }
        }
      }
    }
  });
}

watch(() => [props.labels, props.data], createChart, { deep: true });
onMounted(createChart);
</script>