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
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Фамилия<span class="text-red-500">*</span>
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <UserIcon :size="18" class="text-gray-400" />
              </div>
              <input
                v-model="formData.last_name"
                type="text"
                required
                placeholder="Введите фамилию"
                class="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
              />
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Имя<span class="text-red-500">*</span>
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <UserIcon :size="18" class="text-gray-400" />
              </div>
              <input
                v-model="formData.first_name"
                type="text"
                required
                placeholder="Введите имя"
                class="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
              />
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Отдел<span class="text-red-500">*</span>
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <BuildingIcon :size="18" class="text-gray-400" />
              </div>
              <select
                v-model="formData.department"
                required
                class="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
              >
                <option value="">Выберите отдел</option>
                <option v-for="dept in departments" :key="dept.value" :value="dept.value">
                  {{ dept.label }}
                </option>
              </select>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Кабинет<span class="text-red-500">*</span>
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <DoorClosedIcon :size="18" class="text-gray-400" />
              </div>
              <input
                v-model="formData.office"
                type="text"
                required
                placeholder="Номер кабинета"
                class="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
              />
            </div>
          </div>

          <div class="sm:col-span-2">
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Пароль{{ !employee ? '*' : '' }}
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <LockIcon :size="18" class="text-gray-400" />
              </div>
              <input
                v-model="formData.password"
                type="password"
                :required="!employee"
                placeholder="Введите пароль"
                class="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
              />
            </div>
            <p v-if="employee" class="mt-1 text-sm text-gray-500">
              Оставьте пустым, чтобы не менять пароль
            </p>
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
import type { EmployeeFormData } from '@/types/employee';


const props = defineProps<{
  employee?: any;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'submit', data: any): void;
}>();

const formData = ref<EmployeeFormData>({
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
    delete data.password; // Теперь это безопасно, так как password опциональный
  }
  emit('submit', data);
}
</script>