<template>
  <div class="bg-white rounded-lg shadow-lg p-4 sm:p-6">
    <h2 class="text-xl sm:text-2xl font-semibold text-slate-800 mb-2">
      Техническая поддержка
    </h2>
    <p class="text-sm sm:text-base text-slate-600 mb-4 sm:mb-6">
      Заполните форму для создания заявки в IT-отдел
    </p>
    
    <RequestForm />
  </div>
</template>

<script setup lang="ts">
import RequestForm from '@/components/request/RequestForm.vue';
</script>