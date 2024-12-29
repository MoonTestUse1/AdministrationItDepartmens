template>
  <div class="max-w-2xl mx-auto bg-white p-6 rounded-lg shadow-md">
    <h1 class="text-2xl font-bold mb-6">Добавить работника</h1>
    
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700">Имя</label>
        <input
          v-model="form.firstName"
          type="text"
          required
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700">Фамилия</label>
        <input
          v-model="form.lastName"
          type="text"
          required
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700">Отдел</label>
        <select
          v-model="form.department"
          required
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
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
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700">Пароль</label>
        <input
          v-model="form.password"
          type="password"
          required
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
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
          class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
          :disabled="isSubmitting"
        >
          {{ isSubmitting ? 'Сохранение...' : 'Сохранить' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { departments } from '@/utils/constants';
type Department = typeof departments[number];

const router = useRouter();
const isSubmitting = ref(false);

const form = ref({
  firstName: '',
  lastName: '',
  department: '',
  office: '',
  password: ''
});

// @vue-ignore
const handleSubmit = async () => {
  try {
    isSubmitting.value = true;
    const response = await fetch('/api/employees', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(form.value)
    });

    if (!response.ok) {
      throw new Error('Ошибка при создании сотрудника');
    }

    router.push('/admin/dashboard');
  } catch (error) {
    console.error('Error creating employee:', error);
    alert('Произошла ошибка при создании сотрудника');
  } finally {
    isSubmitting.value = false;
  }
};
</script>