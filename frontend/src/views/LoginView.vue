<template>
  <div class="max-w-md mx-auto bg-white rounded-lg shadow-lg p-6">
    <h2 class="text-2xl font-semibold text-slate-800 mb-4">Вход в систему</h2>
    
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-slate-700 mb-1">
          Фамилия
        </label>
        <div class="relative">
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center">
            <UserIcon :size="18" class="text-slate-400" />
          </div>
          <input
            v-model="lastName"
            type="text"
            required
            class="w-full pl-10 pr-3 py-2 border border-slate-300 rounded-md focus:ring-2 focus:ring-blue-500"
            placeholder="Введите фамилию"
          />
        </div>
      </div>

      <div>
        <label class="block text-sm font-medium text-slate-700 mb-1">
          Пароль
        </label>
        <div class="relative">
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center">
            <LockIcon :size="18" class="text-slate-400" />
          </div>
          <input
            v-model="password"
            type="password"
            required
            class="w-full pl-10 pr-3 py-2 border border-slate-300 rounded-md focus:ring-2 focus:ring-blue-500"
            placeholder="Введите пароль"
          />
        </div>
      </div>

      <button
        type="submit"
        :disabled="isLoading"
        class="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
      >
        <component 
          :is="isLoading ? LoaderIcon : LogInIcon" 
          :size="18"
          :class="{ 'animate-spin': isLoading }" 
        />
        {{ isLoading ? 'Вход...' : 'Войти' }}
      </button>

      <div class="text-center">
        <router-link 
          to="/admin" 
          class="text-sm text-blue-600 hover:text-blue-800"
        >
          Вход для администраторов
        </router-link>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { UserIcon, LockIcon, LogInIcon, LoaderIcon } from 'lucide-vue-next';

const router = useRouter();
const authStore = useAuthStore();

const lastName = ref('');
const password = ref('');
const isLoading = ref(false);

async function handleSubmit() {
  if (isLoading.value) return;
  
  isLoading.value = true;
  try {
    const success = await authStore.login(lastName.value, password.value);
    if (success) {
      router.push('/support');
    } else {
      alert('Неверная фамилия или пароль');
    }
  } catch (error) {
    console.error('Error:', error);
    alert('Ошибка авторизации');
  } finally {
    isLoading.value = false;
  }
}
</script>
