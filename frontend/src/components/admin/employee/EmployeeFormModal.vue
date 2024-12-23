<template>
  <div class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg p-8 max-w-xl w-full mx-4 shadow-xl">
      <div class="flex justify-between items-center mb-6">
        <div class="flex items-center gap-3">
          <div class="p-2 bg-blue-50 rounded-lg">
            <component 
              :is="employee ? UserIcon : UserPlusIcon"
              :size="24"
              class="text-blue-600"
            />
          </div>
          <h3 class="text-xl font-semibold text-gray-900">
            {{ employee ? 'Редактирование сотрудника' : 'Добавление сотрудника' }}
          </h3>
        </div>
        <button
          @click="$emit('close')"
          class="text-gray-400 hover:text-gray-500 transition-colors"
        >
          <XIcon :size="20" />
        </button>
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-6">
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <FormField
            v-model="formData.last_name"
            label="Фамилия"
            required
            placeholder="Введите фамилию"
            :icon="UserIcon"
          />

          <FormField
            v-model="formData.first_name"
            label="Имя"
            required
            placeholder="Введите имя"
            :icon="UserIcon"
          />

          <FormField
            v-model="formData.department"
            label="Отдел"
            type="select"
            required
            :options="departmentOptions"
            :icon="BuildingIcon"
          />

          <FormField
            v-model="formData.office"
            label="Кабинет"
            required
            placeholder="Номер кабинета"
            :icon="DoorClosedIcon"
          />

          <div class="sm:col-span-2">
            <FormField
              v-model="formData.password"
              label="Пароль"
              type="password"
              :required="!employee"
              placeholder="Введите пароль"
              :icon="LockIcon"
              :help="employee ? 'Оставьте пустым, чтобы не менять пароль' : undefined"
            />
          </div>
        </div>

        <div class="flex justify-end gap-3 mt-8 pt-4 border-t">
          <button
            type="button"
            @click="$emit('close')"
            class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors flex items-center gap-2"
          >
            <XIcon :size="16" />
            Отмена
          </button>
          <button
            type="submit"
            class="px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors flex items-center gap-2"
          >
            <component :is="employee ? SaveIcon : UserPlusIcon" :size="16" />
            {{ employee ? 'Сохранить' : 'Добавить' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { XIcon, UserIcon, BuildingIcon, DoorClosedIcon, LockIcon, UserPlusIcon, SaveIcon } from 'lucide-vue-next';
import { departments } from '@/utils/constants';
import FormField from '@/components/ui/FormField.vue';

interface Employee {
  id: number;
  first_name: string;
  last_name: string;
  department: string;
  office: string;
}

const props = defineProps<{
  employee?: Employee;
}>();

const departmentOptions = departments.map(d => ({
  value: d.value,
  label: d.label
}));


const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'submit', data: any): void;
}>();

const formData = ref({
  first_name: '',
  last_name: '',
  department: '',
  office: '',
  password: ''
});

onMounted(() => {
  if (props.employee) {
    formData.value = {
      first_name: props.employee.first_name,
      last_name: props.employee.last_name,
      department: props.employee.department,
      office: props.employee.office,
      password: ''
    };
  }
});

function handleSubmit() {
  const data = { ...formData.value };
  if (props.employee && !data.password) {
    formData.value.password = ''; // Вместо delete используем присваивание пустой строки
  }
  emit('submit', data);
}
</script>