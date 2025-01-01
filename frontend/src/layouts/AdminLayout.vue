<template>
  <div class="min-h-screen bg-gray-100">
    <!-- Sidebar -->
    <aside class="fixed inset-y-0 left-0 w-64 bg-slate-800 text-white">
      <div class="p-4">
        <h1 class="text-xl font-bold">Админ-панель</h1>
      </div>
      <nav class="mt-4">
        <router-link 
          v-for="item in menuItems" 
          :key="item.path"
          :to="item.path"
          class="flex items-center px-4 py-2 text-gray-300 hover:bg-slate-700 hover:text-white"
          :class="{ 'bg-slate-700 text-white': isCurrentRoute(item.path) }"
        >
          <component :is="item.icon" class="w-5 h-5 mr-2" />
          {{ item.name }}
        </router-link>
      </nav>
    </aside>

    <!-- Main content -->
    <main class="pl-64">
      <div class="p-8">
        <router-view></router-view>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router';
import { 
  LayoutDashboard, 
  ClipboardList, 
  Users 
} from 'lucide-vue-next';

const route = useRoute();

const menuItems = [
  { 
    name: 'Дашборд', 
    path: '/admin/dashboard',
    icon: LayoutDashboard 
  },
  { 
    name: 'Заявки', 
    path: '/admin/requests',
    icon: ClipboardList 
  },
  { 
    name: 'Сотрудники', 
    path: '/admin/employees',
    icon: Users 
  }
];

const isCurrentRoute = (path: string) => {
  return route.path.startsWith(path);
};
</script> 