<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold">Сотрудники</h1>
      <router-link 
        to="/admin/employees/add"
        class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 inline-flex items-center gap-2"
      >
        <PlusCircle class="w-5 h-5" />
        Добавить сотрудника
      </router-link>
    </div>

    <!-- Employees table -->
    <div class="bg-white rounded-lg shadow">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Фамилия</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Имя</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Отдел</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Кабинет</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Действия</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="employee in employees" :key="employee.id">
              <td class="px-6 py-4 whitespace-nowrap">{{ employee.last_name }}</td>
              <td class="px-6 py-4 whitespace-nowrap">{{ employee.first_name }}</td>
              <td class="px-6 py-4 whitespace-nowrap">{{ employee.department }}</td>
              <td class="px-6 py-4 whitespace-nowrap">{{ employee.office }}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <button 
                  @click="editEmployee(employee)"
                  class="text-blue-600 hover:text-blue-900"
                >
                  Редактировать
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { PlusCircle } from 'lucide-vue-next';
import { useRouter } from 'vue-router';

interface Employee {
  id: number;
  first_name: string;
  last_name: string;
  department: string;
  office: string;
}

const router = useRouter();
const employees = ref<Employee[]>([]);

const fetchEmployees = async () => {
  try {
    const response = await fetch('/api/employees/');
    if (!response.ok) throw new Error('Failed to fetch employees');
    employees.value = await response.json();
  } catch (error) {
    console.error('Error fetching employees:', error);
  }
};

const editEmployee = (employee: Employee) => {
  // Implement edit functionality
  console.log('Edit employee:', employee);
};

const addEmployee = () => {
  router.push('/admin/employees/add');
};

onMounted(() => {
  fetchEmployees();
});
</script> 