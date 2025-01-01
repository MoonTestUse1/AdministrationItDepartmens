<template>
  <div class="min-h-screen bg-white flex">
    <!-- Боковое меню -->
    <div class="w-64 bg-white border-r border-gray-200">
      <div class="h-16 flex items-center px-6 border-b border-gray-200">
        <h1 class="text-xl font-medium text-gray-900">Админ панель</h1>
      </div>
      <div class="p-4">
        <nav class="space-y-2">
          <button
            @click="activeSection = 'statistics'"
            :class="[
              'w-full px-4 py-3 text-left rounded-lg text-sm font-medium transition-colors flex items-center',
              activeSection === 'statistics'
                ? 'bg-blue-50 text-blue-600'
                : 'text-gray-700 hover:bg-gray-50'
            ]"
          >
            <svg class="w-5 h-5 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            Статистика
          </button>
          <button
            @click="activeSection = 'requests'"
            :class="[
              'w-full px-4 py-3 text-left rounded-lg text-sm font-medium transition-colors flex items-center',
              activeSection === 'requests'
                ? 'bg-blue-50 text-blue-600'
                : 'text-gray-700 hover:bg-gray-50'
            ]"
          >
            <svg class="w-5 h-5 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
            </svg>
            Заявки
          </button>
          <button
            @click="activeSection = 'employees'"
            :class="[
              'w-full px-4 py-3 text-left rounded-lg text-sm font-medium transition-colors flex items-center',
              activeSection === 'employees'
                ? 'bg-blue-50 text-blue-600'
                : 'text-gray-700 hover:bg-gray-50'
            ]"
          >
            <svg class="w-5 h-5 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            Сотрудники
          </button>
        </nav>
      </div>
    </div>

    <!-- Основной контент -->
    <div class="flex-1 flex flex-col">
      <!-- Верхняя панель -->
      <header class="h-16 bg-white border-b border-gray-200">
        <div class="h-full px-6 flex items-center justify-end">
          <button 
            @click="handleLogout"
            class="text-gray-600 hover:text-gray-900 font-medium transition-colors flex items-center"
          >
            <svg class="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            Выйти
          </button>
        </div>
      </header>

      <main class="flex-1 p-6 bg-gray-50">
        <!-- Статистика -->
        <div v-if="activeSection === 'statistics'" class="space-y-6">
          <h2 class="text-2xl font-medium text-gray-900">Статистика</h2>
          <div class="grid grid-cols-1 gap-6 sm:grid-cols-4">
            <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
              <div class="text-sm font-medium text-gray-500 mb-1">Новые заявки</div>
              <div class="text-2xl font-medium text-gray-900">{{ statistics.new || 0 }}</div>
            </div>
            <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
              <div class="text-sm font-medium text-gray-500 mb-1">В работе</div>
              <div class="text-2xl font-medium text-gray-900">{{ statistics.inProgress || 0 }}</div>
            </div>
            <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
              <div class="text-sm font-medium text-gray-500 mb-1">Завершенные</div>
              <div class="text-2xl font-medium text-gray-900">{{ statistics.completed || 0 }}</div>
            </div>
            <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
              <div class="text-sm font-medium text-gray-500 mb-1">Отклоненные</div>
              <div class="text-2xl font-medium text-gray-900">{{ statistics.rejected || 0 }}</div>
            </div>
          </div>
        </div>

        <!-- Заявки -->
        <div v-if="activeSection === 'requests'" class="space-y-6">
          <h2 class="text-2xl font-medium text-gray-900">Заявки</h2>
          <div class="bg-white rounded-lg shadow-sm border border-gray-200">
            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead>
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider bg-gray-50">ID</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider bg-gray-50">Сотрудник</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider bg-gray-50">Отдел</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider bg-gray-50">Тип</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider bg-gray-50">Приоритет</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider bg-gray-50">Статус</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider bg-gray-50">Действия</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-200">
                  <tr v-for="request in requests" :key="request.id" class="hover:bg-gray-50">
                    <td class="px-6 py-4 text-sm text-gray-900">{{ request.id }}</td>
                    <td class="px-6 py-4">
                      <div class="text-sm text-gray-900">{{ request.employee?.last_name }}</div>
                      <div class="text-sm text-gray-500">{{ request.employee?.first_name }}</div>
                    </td>
                    <td class="px-6 py-4 text-sm text-gray-900">{{ request.department }}</td>
                    <td class="px-6 py-4 text-sm text-gray-900">{{ request.request_type }}</td>
                    <td class="px-6 py-4">
                      <span :class="getPriorityClass(request.priority)">{{ request.priority }}</span>
                    </td>
                    <td class="px-6 py-4">
                      <span :class="getStatusClass(request.status)">{{ request.status }}</span>
                    </td>
                    <td class="px-6 py-4 text-sm">
                      <button
                        @click="openRequestDetails(request)"
                        class="text-blue-600 hover:text-blue-700 mr-3"
                      >
                        Подробнее
                      </button>
                      <button
                        v-if="request.status !== 'completed'"
                        @click="updateRequestStatus(request)"
                        class="text-blue-600 hover:text-blue-700"
                      >
                        {{ request.status === 'new' ? 'Взять в работу' : 'Завершить' }}
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Сотрудники -->
        <div v-if="activeSection === 'employees'" class="space-y-6">
          <div class="flex justify-between items-center">
            <h2 class="text-2xl font-medium text-gray-900">Сотрудники</h2>
            <button
              @click="openAddEmployeeModal"
              class="inline-flex items-center px-4 py-2 text-sm font-medium text-blue-600 hover:text-blue-700 transition-colors"
            >
              <svg class="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              Добавить сотрудника
            </button>
          </div>
          <div class="bg-white rounded-lg shadow-sm border border-gray-200">
            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead>
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider bg-gray-50">ID</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider bg-gray-50">Имя</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider bg-gray-50">Фамилия</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider bg-gray-50">Отдел</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider bg-gray-50">Кабинет</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider bg-gray-50">Действия</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-200">
                  <tr v-for="employee in employees" :key="employee.id" class="hover:bg-gray-50">
                    <td class="px-6 py-4 text-sm text-gray-900">{{ employee.id }}</td>
                    <td class="px-6 py-4 text-sm text-gray-900">{{ employee.first_name }}</td>
                    <td class="px-6 py-4 text-sm text-gray-900">{{ employee.last_name }}</td>
                    <td class="px-6 py-4 text-sm text-gray-900">{{ employee.department }}</td>
                    <td class="px-6 py-4 text-sm text-gray-900">{{ employee.office }}</td>
                    <td class="px-6 py-4 text-sm">
                      <button
                        @click="openEditEmployeeModal(employee)"
                        class="text-blue-600 hover:text-blue-700"
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
      </main>
    </div>

    <!-- Модальные окна -->
    <div v-if="showRequestModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
      <div class="bg-white rounded-lg max-w-2xl w-full shadow-xl">
        <div class="flex justify-between items-center p-6 border-b">
          <h3 class="text-lg font-medium text-gray-900">Заявка #{{ selectedRequest?.id }}</h3>
          <button @click="showRequestModal = false" class="text-gray-400 hover:text-gray-500">
            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="p-6">
          <div class="space-y-4">
            <div>
              <div class="text-sm font-medium text-gray-500">Описание</div>
              <div class="mt-1 text-sm text-gray-900">{{ selectedRequest?.description }}</div>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <div class="text-sm font-medium text-gray-500">Сотрудник</div>
                <div class="mt-1 text-sm text-gray-900">
                  {{ selectedRequest?.employee?.last_name }} {{ selectedRequest?.employee?.first_name }}
                </div>
              </div>
              <div>
                <div class="text-sm font-medium text-gray-500">Отдел</div>
                <div class="mt-1 text-sm text-gray-900">{{ selectedRequest?.department }}</div>
              </div>
              <div>
                <div class="text-sm font-medium text-gray-500">Тип заявки</div>
                <div class="mt-1 text-sm text-gray-900">{{ selectedRequest?.request_type }}</div>
              </div>
              <div>
                <div class="text-sm font-medium text-gray-500">Приоритет</div>
                <div class="mt-1">
                  <span :class="getPriorityClass(selectedRequest?.priority)">
                    {{ selectedRequest?.priority }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="flex justify-end gap-3 p-6 border-t bg-gray-50">
          <button
            @click="showRequestModal = false"
            class="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900"
          >
            Закрыть
          </button>
          <button
            v-if="selectedRequest?.status !== 'completed'"
            @click="updateRequestStatus(selectedRequest)"
            class="px-4 py-2 text-sm font-medium text-blue-600 hover:text-blue-700"
          >
            {{ selectedRequest?.status === 'new' ? 'Взять в работу' : 'Завершить' }}
          </button>
        </div>
      </div>
    </div>

    <div v-if="showEmployeeModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
      <div class="bg-white rounded-lg max-w-md w-full shadow-xl">
        <div class="flex justify-between items-center p-6 border-b">
          <h3 class="text-lg font-medium text-gray-900">
            {{ isEditingEmployee ? 'Редактировать сотрудника' : 'Добавить сотрудника' }}
          </h3>
          <button @click="showEmployeeModal = false" class="text-gray-400 hover:text-gray-500">
            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <form @submit.prevent="handleEmployeeSubmit" class="p-6">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Имя</label>
              <input
                v-model="employeeForm.first_name"
                type="text"
                required
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Фамилия</label>
              <input
                v-model="employeeForm.last_name"
                type="text"
                required
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Отдел</label>
              <input
                v-model="employeeForm.department"
                type="text"
                required
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Кабинет</label>
              <input
                v-model="employeeForm.office"
                type="text"
                required
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">
                Пароль {{ isEditingEmployee ? '(оставьте пустым, чтобы не менять)' : '' }}
              </label>
              <input
                v-model="employeeForm.password"
                type="password"
                :required="!isEditingEmployee"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              />
            </div>
          </div>
        </form>
        <div class="flex justify-end gap-3 p-6 border-t bg-gray-50">
          <button
            type="button"
            @click="showEmployeeModal = false"
            class="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900"
          >
            Отмена
          </button>
          <button
            type="submit"
            class="px-4 py-2 text-sm font-medium text-blue-600 hover:text-blue-700"
          >
            {{ isEditingEmployee ? 'Сохранить' : 'Добавить' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

interface Statistics {
  new: number
  inProgress: number
  completed: number
  rejected: number
}

interface Employee {
  id: number
  first_name: string
  last_name: string
  department: string
  office: string
}

interface Request {
  id: number
  employee_id: number
  employee?: Employee
  department: string
  request_type: string
  priority: 'low' | 'medium' | 'high' | 'critical'
  description: string
  status: 'new' | 'in_progress' | 'completed' | 'rejected'
  created_at: string
}

interface EmployeeForm {
  id: number | null
  first_name: string
  last_name: string
  department: string
  office: string
  password: string
}

const router = useRouter()
const activeSection = ref('statistics')
const statistics = ref<Statistics>({ new: 0, inProgress: 0, completed: 0, rejected: 0 })
const requests = ref<Request[]>([])
const employees = ref<Employee[]>([])
const showRequestModal = ref(false)
const showEmployeeModal = ref(false)
const selectedRequest = ref<Request | null>(null)
const isEditingEmployee = ref(false)
const employeeForm = ref<EmployeeForm>({
  id: null,
  first_name: '',
  last_name: '',
  department: '',
  office: '',
  password: ''
})

const priorityClasses = {
  low: 'px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-800',
  medium: 'px-2 py-1 text-xs rounded-full bg-yellow-100 text-yellow-800',
  high: 'px-2 py-1 text-xs rounded-full bg-orange-100 text-orange-800',
  critical: 'px-2 py-1 text-xs rounded-full bg-red-100 text-red-800'
} as const

const statusClasses = {
  new: 'px-2 py-1 text-xs rounded-full bg-gray-100 text-gray-800',
  in_progress: 'px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-800',
  completed: 'px-2 py-1 text-xs rounded-full bg-green-100 text-green-800',
  rejected: 'px-2 py-1 text-xs rounded-full bg-red-100 text-red-800'
} as const

const getPriorityClass = (priority: Request['priority'] | undefined) => {
  if (!priority) return priorityClasses.low
  return priorityClasses[priority]
}

const getStatusClass = (status: Request['status']) => {
  return statusClasses[status]
}

// Получение данных
const fetchData = async () => {
  try {
    const token = localStorage.getItem('admin_token')
    if (!token) {
      throw new Error('Не найден токен авторизации')
    }

    const headers = { Authorization: `Bearer ${token}` }

    // Получаем статистику
    const statsResponse = await axios.get<Statistics>('/api/statistics/', { headers })
    statistics.value = statsResponse.data

    // Получаем заявки
    const requestsResponse = await axios.get<Request[]>('/api/requests/', { headers })
    requests.value = requestsResponse.data

    // Получаем сотрудников
    const employeesResponse = await axios.get<Employee[]>('/api/employees/', { headers })
    employees.value = employeesResponse.data
  } catch (error) {
    console.error('Ошибка при получении данных:', error)
    router.push('/admin')
  }
}

// Обработчики действий
const handleLogout = async () => {
  localStorage.removeItem('admin_token')
  localStorage.removeItem('is_admin')
  await router.push('/admin')
}

const openRequestDetails = (request: Request) => {
  selectedRequest.value = request
  showRequestModal.value = true
}

const openAddEmployeeModal = () => {
  router.push('/admin/employees/add');
};

const openEditEmployeeModal = (employee: Employee) => {
  isEditingEmployee.value = true
  employeeForm.value = {
    id: employee.id,
    first_name: employee.first_name,
    last_name: employee.last_name,
    department: employee.department,
    office: employee.office,
    password: ''
  }
  showEmployeeModal.value = true
}

const handleEmployeeSubmit = async () => {
  try {
    const token = localStorage.getItem('admin_token')
    if (!token) {
      throw new Error('Не найден токен авторизации')
    }

    const headers = { Authorization: `Bearer ${token}` }
    
    if (isEditingEmployee.value && employeeForm.value.id) {
      await axios.put(`/api/employees/${employeeForm.value.id}`, employeeForm.value, { headers })
    } else {
      await axios.post('/api/employees/', employeeForm.value, { headers })
    }

    showEmployeeModal.value = false
    await fetchData()
  } catch (error) {
    console.error('Ошибка при сохранении сотрудника:', error)
  }
}

const updateRequestStatus = async (request: Request | null) => {
  if (!request) return
  
  try {
    const token = localStorage.getItem('admin_token')
    if (!token) {
      throw new Error('Не найден токен авторизации')
    }

    const headers = { Authorization: `Bearer ${token}` }
    
    let newStatus: Request['status'] = 'in_progress'
    if (request.status === 'new') {
      newStatus = 'in_progress'
    } else if (request.status === 'in_progress') {
      newStatus = 'completed'
    } else if (request.status === 'completed') {
      newStatus = 'rejected'
    }

    await axios.put(`/api/requests/${request.id}`, { status: newStatus }, { headers })
    await fetchData()
  } catch (error) {
    console.error('Ошибка при обновлении статуса:', error)
  }
}

onMounted(fetchData)
</script>

<style>
.bg-navy-900 {
  background-color: #1a1f2c;
}
.bg-navy-800 {
  background-color: #1f2937;
}
.bg-navy-700 {
  background-color: #2d3748;
}
.border-navy-700 {
  border-color: #2d3748;
}
</style> 
