<template>
  <span :class="[
    'px-2 inline-flex text-xs leading-5 font-semibold rounded-full',
    priorityClasses[priority]
  ]">
    {{ priorityLabels[priority] }}
  </span>
</template>

<script setup lang="ts">
const { priority } = defineProps<{
  priority: 'low' | 'medium' | 'high' | 'critical'
}>();

const priorityClasses = {
  low: 'bg-green-100 text-green-800',
  medium: 'bg-yellow-100 text-yellow-800',
  high: 'bg-orange-100 text-orange-800',
  critical: 'bg-red-100 text-red-800'
};

const priorityLabels = {
  low: 'Низкий',
  medium: 'Средний',
  high: 'Высокий',
  critical: 'Критический'
};
</script>