<template>
  <form @submit.prevent="handleSubmit" class="space-y-4">
    <div>
      <label class="block text-sm font-medium text-slate-700 mb-1">
        Тип обращения<span class="text-red-500">*</span>
      </label>
      <select
        v-model="formData.request_type"
        required
        :disabled="isSubmitting"
        class="w-full px-3 py-2 text-sm border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="">Выберите тип обращения</option>
        <option v-for="type in requestTypes" :key="type.value" :value="type.value">
          {{ type.label }}
        </option>
      </select>
    </div>

    <div>
      <label class="block text-sm font-medium text-slate-700 mb-1">
        Приоритет<span class="text-red-500">*</span>
      </label>
      <select
        v-model="formData.priority"
        required
        :disabled="isSubmitting"
        class="w-full px-3 py-2 text-sm border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="">Выберите приоритет</option>
        <option value="low">Низкий</option>
        <option value="medium">Средний</option>
        <option value="high">Высокий</option>
        <option value="critical">Критический</option>
      </select>
    </div>

    <div>
      <label class="block text-sm font-medium text-slate-700 mb-1">
        Описание проблемы<span class="text-red-500">*</span>
      </label>
      <textarea
        v-model="formData.description"
        required
        :disabled="isSubmitting"
        rows="4"
        class="w-full px-3 py-2 text-sm border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        placeholder="Опишите вашу проблему..."
      ></textarea>
    </div>

    <button
      type="submit"
      :disabled="isSubmitting"
      class="w-full bg-blue-600 text-white py-2 px-4 text-sm sm:text-base rounded-md hover:bg-blue-700 transition-colors flex items-center justify-center gap-2 disabled:opacity-50"
    >
      <component :is="isSubmitting ? LoaderIcon : SendIcon" 
        :size="18" 
        :class="{ 'animate-spin': isSubmitting }" 
      />
      {{ isSubmitting ? 'Отправка...' : 'Отправить заявку' }}
    </button>
  </form>

  <Transition
    enter-active-class="transform ease-out duration-300"
    enter-from-class="translate-y-2 opacity-0"
    enter-to-class="translate-y-0 opacity-100"
    leave-active-class="transition ease-in duration-200"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
  >
    <div 
      v-if="showNotification"
      class="fixed top-4 right-4 z-50 max-w-sm w-full bg-green-50 rounded-lg shadow-lg ring-1 ring-green-500 ring-opacity-5 overflow-hidden"
    >
      <div class="p-4">
        <div class="flex items-start">
          <div class="flex-shrink-0">
            <CheckCircleIcon class="h-5 w-5 text-green-400" />
          </div>
          <div class="ml-3 w-0 flex-1 pt-0.5">
            <p class="text-sm font-medium text-green-800">
              Заявка успешно отправлена. Ожидайте прибытия технического специалиста.
            </p>
          </div>
          <div class="ml-4 flex-shrink-0 flex">
            <button
              @click="showNotification = false"
              class="inline-flex text-green-500 hover:text-green-600 focus:outline-none focus:ring-2 focus:ring-green-500"
            >
              <XIcon class="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { SendIcon, LoaderIcon, CheckCircleIcon, XIcon } from 'lucide-vue-next';
import { useAuthStore } from '@/stores/auth';
import { requestTypes } from '@/utils/constants';

const authStore = useAuthStore();
const isSubmitting = ref(false);
const showNotification = ref(false);

const formData = ref({
  request_type: '',
  priority: '',
  description: '',
  department: ''
});

async function handleSubmit() {
  if (!authStore.user) {
    alert('Необходимо авторизоваться');
    return;
  }

  isSubmitting.value = true;
  try {
    const response = await fetch('/api/requests/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        ...formData.value,
        employee_id: parseInt(authStore.user.id),
        department: authStore.user.department
      }),
    });

    if (!response.ok) {
      throw new Error('Failed to submit request');
    }

    // Show notification
    showNotification.value = true;
    setTimeout(() => {
      showNotification.value = false;
    }, 5000);

    // Reset form
    formData.value = {
      request_type: '',
      priority: '',
      description: '',
      department: ''
    };
  } catch (error) {
    console.error('Error submitting request:', error);
    alert('Ошибка при отправке заявки');
  } finally {
    isSubmitting.value = false;
  }
}
</script>