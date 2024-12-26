<template>
  <div class="space-y-4">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-lg font-semibold">Сотрудники</h2>
      <button
        @click="showAddForm = true"
        class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 flex items-center gap-2"
      >
        <UserPlusIcon :size="18" />
        Добавить сотрудника
      </button>
    </div>

    <div class="bg-white rounded-lg shadow overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Фамилия</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Имя</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Отдел</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Кабинет</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Действия</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="employee in employees" :key="employee.id">
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              {{ employee.last_name }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              {{ employee.first_name }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              {{ getDepartmentLabel(employee.department) }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              {{ employee.office }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              <button 
                @click="editEmployee(employee)"
                class="text-blue-600 hover:text-blue-900 mr-4 flex items-center gap-2"
              >
                <PencilIcon :size="16" />
                Редактировать
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Модальное окно -->
    <div v-show="showAddForm || editingEmployee" class="fixed inset-0 overflow-y-auto" style="z-index: 100;">
      <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 transition-opacity" aria-hidden="true">
          <div class="absolute inset-0 bg-gray-500 opacity-75"></div>
        </div>

        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="sm:flex sm:items-start">
              <div class="mt-3 text-center sm:mt-0 sm:text-left w-full">
                <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                  {{ editingEmployee ? 'Редактировать сотрудника' : 'Добавить сотрудника' }}
                </h3>
                
                <form @submit.prevent="handleSubmit" class="space-y-4">
                  <div class="grid grid-cols-1 gap-4">
                    <div>
                      <label class="block text-sm font-medium text-gray-700">Фамилия</label>
                      <input
                        v-model="formData.last_name"
                        type="text"
                        required
                        class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                    
                    <div>
                      <label class="block text-sm font-medium text-gray-700">Имя</label>
                      <input
                        v-model="formData.first_name"
                        type="text"
                        required
                        class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                    
                    <div>
                      <label class="block text-sm font-medium text-gray-700">Отдел</label>
                      <select
                        v-model="formData.department"
                        required
                        class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
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
                        v-model="formData.office"
                        type="text"
                        required
                        class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                    
                    <div>
                      <label class="block text-sm font-medium text-gray-700">
                        Пароль {{ !editingEmployee ? '(обязательно)' : '(оставьте пустым, чтобы не менять)' }}
                      </label>
                      <input
                        v-model="formData.password"
                        type="password"
                        :required="!editingEmployee"
                        class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                  </div>

                  <div class="mt-5 sm:mt-4 sm:flex sm:flex-row-reverse">
                    <button
                      type="submit"
                      class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-3 sm:w-auto sm:text-sm"
                    >
                      {{ editingEmployee ? 'Сохранить' : 'Добавить' }}
                    </button>
                    <button
                      type="button"
                      @click="closeForm"
                      class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:mt-0 sm:w-auto sm:text-sm"
                    >
                      Отмена
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { UserPlusIcon, PencilIcon } from 'lucide-vue-next';
import { departments } from '@/utils/constants';
import type { Employee, EmployeeFormData } from '@/types/employee';

const employees = ref<Employee[]>([]);
const showAddForm = ref(false);
const editingEmployee = ref<Employee | null>(null);

const formData = ref<EmployeeFormData>({
  first_name: '',
  last_name: '',
  department: '',
  office: '',
  password: ''
});

// Сброс формы при закрытии
function resetForm() {
  formData.value = {
    first_name: '',
    last_name: '',
    department: '',
    office: '',
    password: ''
  };
}

// Наблюдаем за изменением editingEmployee
watch(editingEmployee, (newEmployee) => {
  if (newEmployee) {
    formData.value = {
      first_name: newEmployee.first_name,
      last_name: newEmployee.last_name,
      department: newEmployee.department,
      office: newEmployee.office,
      password: ''
    };
  } else {
    resetForm();
  }
});

function getDepartmentLabel(value: string) {
  return departments.find(d => d.value === value)?.label || value;
}

function editEmployee(employee: Employee) {
  editingEmployee.value = employee;
  showAddForm.value = true;
}

function closeForm() {
  showAddForm.value = false;
  editingEmployee.value = null;
  resetForm();
}

async function handleSubmit() {
  try {
    const data = { ...formData.value };
    if (editingEmployee.value && !data.password) {
      delete data.password;
    }

    if (editingEmployee.value) {
      // Update existing employee
      const response = await fetch(`/api/employees/${editingEmployee.value.id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to update employee');
      }
    } else {
      // Create new employee
      const response = await fetch('/api/employees/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to create employee');
      }
    }
    await fetchEmployees();
    closeForm();
    alert(editingEmployee.value ? 'Сотрудник обновлен' : 'Сотрудник добавлен');
  } catch (error: any) {
    console.error('Error:', error);
    alert(`Ошибка: ${error.message}`);
  }
}

async function fetchEmployees() {
  try {
    const response = await fetch('/api/employees/');
    if (!response.ok) throw new Error('Failed to fetch employees');
    employees.value = await response.json();
  } catch (error) {
    console.error('Error fetching employees:', error);
  }
}

onMounted(() => {
  fetchEmployees();
});
</script>