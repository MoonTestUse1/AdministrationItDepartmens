<template>
    <button
      @click="openAddEmployeeModal"
      class="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg flex items-center gap-2 transition-colors"
    >
      <PlusCircle class="w-5 h-5" />
      Добавить работника
    </button>
  </template>
  
  <script setup lang="ts">
  import { PlusCircle } from 'lucide-vue-next';
  import { useRouter } from 'vue-router';
  
  const router = useRouter();
  
  const openAddEmployeeModal = () => {
    router.push('/employees/add');
  };
  </script>