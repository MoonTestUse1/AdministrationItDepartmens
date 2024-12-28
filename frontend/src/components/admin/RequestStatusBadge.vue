<template>
  <span :class="[
    'px-2 inline-flex text-xs leading-5 font-semibold rounded-full',
    statusClasses[status]
  ]">
    {{ statusLabels[status] }}
  </span>
</template>

<script setup lang="ts">
defineProps<{
  status: 'new' | 'in_progress' | 'resolved' | 'closed'
}>();



const statusClasses = {
  new: 'bg-blue-100 text-blue-800',
  in_progress: 'bg-yellow-100 text-yellow-800',
  resolved: 'bg-green-100 text-green-800',
  closed: 'bg-gray-100 text-gray-800'
} as const;

const statusLabels = {
  new: 'Новая',
  in_progress: 'В работе',
  resolved: 'Решена',
  closed: 'Закрыта'
};
</script>