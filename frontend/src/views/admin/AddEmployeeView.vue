<template>
  <div class="max-w-2xl mx-auto bg-white p-6 rounded-lg shadow-md">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Добавить сотрудника</h1>
      <button
        @click="router.back()"
        class="text-gray-600 hover:text-gray-800"
      >
        <XIcon class="w-6 h-6" />
      </button>
    </div>
    
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700">Имя</label>
        <input
          v-model="form.first_name"
          type="text"
          required
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700">Фамилия</label>
        <input
          v-model="form.last_name"
          type="text"
          required
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700">Отдел</label>
        <select
          v-model="form.department"
          required
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
        >
          <option value="">Выберите отдел</option>
          <option v-for="dept in departments" :key="dept.value" :value="dept.value">
            {{ dept.label }}
          </option>
        </select>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700">Кабинет</label>
        <input
          v-model="form.office"
          type="text"
          required
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700">Пароль</label>
        <input
          v-model="form.password"
          type="password"
          required
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
        />
      </div>

      <div class="flex justify-end space-x-3 pt-4">
        <button
          type="button"
          @click="router.back()"
          class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
        >
          Отмена
        </button>
        <button
          type="submit"
          class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 flex items-center gap-2"
          :disabled="isSubmitting"
        >
          <LoaderIcon v-if="isSubmitting" class="animate-spin w-5 h-5" />
          <SaveIcon v-else class="w-5 h-5" />
          {{ isSubmitting ? 'Сохранение...' : 'Сохранить' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { XIcon, SaveIcon, LoaderIcon } from 'lucide-vue-next';

const router = useRouter();
const isSubmitting = ref(false);

const departments = [
  { value: 'it', label: 'IT отдел' },
  { value: 'hr', label: 'HR отдел' },
  { value: 'finance', label: 'Финансовый отдел' },
  { value: 'sales', label: 'Отдел продаж' }
];

const form = ref({
  first_name: '',
  last_name: '',
  department: '',
  office: '',
  password: ''
});

const handleSubmit = async () => {
  try {
    isSubmitting.value = true;
    const token = localStorage.getItem('admin_token');
    
    if (!token) {
      throw new Error('Не найден токен авторизации');
    }

    console.log('Отправляем данные:', form.value);
    
    const response = await fetch('/api/employees', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(form.value)
    });

    console.log('Статус ответа:', response.status);
    
    if (!response.ok) {
      const errorData = await response.json();
      console.error('Ошибка от сервера:', errorData);
      throw new Error(errorData.detail || 'Ошибка при создании сотрудника');
    }

    const data = await response.json();
    console.log('Успешный ответ:', data);

    router.push('/admin/dashboard');
  } catch (error) {
    console.error('Error creating employee:', error);
    alert(error instanceof Error ? error.message : 'Произошла ошибка при создании сотрудника');
  } finally {
    isSubmitting.value = false;
  }
};
</script>