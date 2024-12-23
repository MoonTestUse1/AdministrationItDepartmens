<template>
  <div class="md:col-span-2 bg-white p-4 rounded-lg shadow">
    <h3 class="text-lg font-medium mb-4">Количество заявок</h3>
    <canvas ref="chartRef"></canvas>
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

function createChart() {
  if (!chartRef.value) return;

  chart?.destroy();
  chart = new Chart(chartRef.value, {
    type: 'line',
    data: {
      labels: props.labels,
      datasets: [{
        label: 'Количество заявок',
        data: props.data,
        borderColor: '#2563eb',
        backgroundColor: 'rgba(37, 99, 235, 0.1)',
        fill: true
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          display: false
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            precision: 0
          }
        }
      }
    }
  });
}

watch(() => [props.labels, props.data], createChart, { deep: true });
onMounted(createChart);
</script>