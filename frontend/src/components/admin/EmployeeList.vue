<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { departments } from '@/utils/constants';
import type { Employee } from '@/types/employee';

const employees = ref<Employee[]>([]); // Добавляем типизацию массива сотрудников
const showAddForm = ref(false);
const editingEmployee = ref<Employee | null>(null);

function getDepartmentLabel(value: string) {
  return departments.find(d => d.value === value)?.label || value;
}

function editEmployee(employee: any) {
  editingEmployee.value = employee;
}

function closeForm() {
  showAddForm.value = false;
  editingEmployee.value = null;
}

async function handleSubmit(data: any) {
  try {
    if (editingEmployee.value) {
      // Update existing employee
      await fetch(`/api/employees/${editingEmployee.value.id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
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
    alert(`Ошибка: ${error.message}`);
  }
}

async function fetchEmployees() {
  try {
    const response = await fetch('/api/employees');
    if (!response.ok) throw new Error('Failed to fetch employees');
    employees.value = await response.json();
  } catch (error) {
    console.error('Error fetching employees:', error);
  }
}

onMounted(fetchEmployees);
</script>

<template>
  <div class="space-y-4">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-lg font-semibold">Сотрудники88</h2>
      <button
        @click="showAddForm = true"
        class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
      >
        Добавить сотрудника222
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
                class="text-blue-600 hover:text-blue-900 mr-4"
              >
                Редактировать
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Employee form modal -->
    <EmployeeForm
      v-if="showAddForm || editingEmployee"
      :employee="editingEmployee"
      @close="closeForm"
      @submit="handleSubmit"
    />
  </div>
</template>
