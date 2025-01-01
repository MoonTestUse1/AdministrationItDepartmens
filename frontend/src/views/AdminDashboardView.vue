<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
        <h1 class="text-2xl font-bold text-gray-900">Панель администратора</h1>
        <button 
          @click="handleLogout"
          class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors flex items-center gap-2"
        >
          Выйти
        </button>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Статистика -->
      <div class="mb-8">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">Статистика заявок</h2>
        <div class="grid grid-cols-1 gap-5 sm:grid-cols-3">
          <!-- Новые заявки -->
          <div class="bg-white overflow-hidden shadow-lg rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="rounded-md bg-blue-500 p-3">
                    <svg class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">Новые заявки</dt>
                    <dd class="flex items-baseline">
                      <div class="text-2xl font-semibold text-gray-900">{{ statistics.new || 0 }}</div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <!-- В работе -->
          <div class="bg-white overflow-hidden shadow-lg rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="rounded-md bg-yellow-500 p-3">
                    <svg class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">В работе</dt>
                    <dd class="flex items-baseline">
                      <div class="text-2xl font-semibold text-gray-900">{{ statistics.inProgress || 0 }}</div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <!-- Решенные -->
          <div class="bg-white overflow-hidden shadow-lg rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="rounded-md bg-green-500 p-3">
                    <svg class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">Решенные</dt>
                    <dd class="flex items-baseline">
                      <div class="text-2xl font-semibold text-gray-900">{{ statistics.resolved || 0 }}</div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Заявки -->
      <div class="mb-8">
        <div class="sm:flex sm:items-center sm:justify-between mb-4">
          <h2 class="text-lg font-semibold text-gray-900">Список заявок</h2>
          <div class="mt-3 sm:mt-0 sm:ml-4">
            <button
              @click="activeTab = 'requests'"
              class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Все заявки
            </button>
          </div>
        </div>
        
        <div class="bg-white shadow-lg rounded-lg overflow-hidden">
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Сотрудник</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Отдел</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Тип</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Приоритет</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Статус</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Действия</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="request in requests" :key="request.id">
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ request.id }}</td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm text-gray-900">{{ request.employee?.last_name }}</div>
                    <div class="text-sm text-gray-500">{{ request.employee?.first_name }}</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ request.department }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ request.request_type }}</td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span :class="getPriorityClass(request.priority)">
                      {{ request.priority }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span :class="getStatusClass(request.status)">
                      {{ request.status }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <button
                      @click="openRequestDetails(request)"
                      class="text-blue-600 hover:text-blue-900 mr-3"
                    >
                      Подробнее
                    </button>
                    <button
                      v-if="request.status !== 'resolved'"
                      @click="updateRequestStatus(request)"
                      class="text-green-600 hover:text-green-900"
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
      <div>
        <div class="sm:flex sm:items-center sm:justify-between mb-4">
          <h2 class="text-lg font-semibold text-gray-900">Список сотрудников</h2>
          <div class="mt-3 sm:mt-0 sm:ml-4">
            <button
              @click="openAddEmployeeModal"
              class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Добавить сотрудника
            </button>
          </div>
        </div>

        <div class="bg-white shadow-lg rounded-lg overflow-hidden">
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Имя</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Фамилия</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Отдел</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Кабинет</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Действия</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="employee in employees" :key="employee.id">
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ employee.id }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ employee.first_name }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ employee.last_name }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ employee.department }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ employee.office }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button
                      @click="openEditEmployeeModal(employee)"
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
    </main>

    <!-- Модальное окно для заявки -->
    <div v-if="showRequestModal" class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center p-4">
      <div class="bg-white rounded-lg max-w-2xl w-full p-6">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-medium">Детали заявки #{{ selectedRequest?.id }}</h3>
          <button @click="showRequestModal = false" class="text-gray-400 hover:text-gray-500">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Описание</label>
            <p class="mt-1 text-sm text-gray-900">{{ selectedRequest?.description }}</p>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Сотрудник</label>
              <p class="mt-1 text-sm text-gray-900">
                {{ selectedRequest?.employee?.last_name }} {{ selectedRequest?.employee?.first_name }}
              </p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Отдел</label>
              <p class="mt-1 text-sm text-gray-900">{{ selectedRequest?.department }}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Тип заявки</label>
              <p class="mt-1 text-sm text-gray-900">{{ selectedRequest?.request_type }}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Приоритет</label>
              <p class="mt-1">
                <span :class="getPriorityClass(selectedRequest?.priority)">
                  {{ selectedRequest?.priority }}
                </span>
              </p>
            </div>
          </div>
        </div>
        <div class="mt-6 flex justify-end gap-3">
          <button
            @click="showRequestModal = false"
            class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            Закрыть
          </button>
          <button
            v-if="selectedRequest?.status !== 'resolved'"
            @click="updateRequestStatus(selectedRequest)"
            class="px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-medium hover:bg-blue-700"
          >
            {{ selectedRequest?.status === 'new' ? 'Взять в работу' : 'Завершить' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Модальное окно для сотрудника -->
    <div v-if="showEmployeeModal" class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center p-4">
      <div class="bg-white rounded-lg max-w-md w-full p-6">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-medium">
            {{ isEditingEmployee ? 'Редактировать сотрудника' : 'Добавить сотрудника' }}
          </h3>
          <button @click="showEmployeeModal = false" class="text-gray-400 hover:text-gray-500">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <form @submit.prevent="handleEmployeeSubmit" class="space-y-4">
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
          <div class="flex justify-end gap-3">
            <button
              type="button"
              @click="showEmployeeModal = false"
              class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
            >
              Отмена
            </button>
            <button
              type="submit"
              class="px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-medium hover:bg-blue-700"
            >
              {{ isEditingEmployee ? 'Сохранить' : 'Добавить' }}
            </button>
          </div>
        </form>
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
  resolved: number
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
  status: 'new' | 'in_progress' | 'resolved'
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
const activeTab = ref('statistics')
const statistics = ref<Statistics>({ new: 0, inProgress: 0, resolved: 0 })
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
  isEditingEmployee.value = false
  employeeForm.value = {
    id: null,
    first_name: '',
    last_name: '',
    department: '',
    office: '',
    password: ''
  }
  showEmployeeModal.value = true
}

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
  if (!request) return;
  
  try {
    const token = localStorage.getItem('admin_token')
    if (!token) {
      throw new Error('Не найден токен авторизации')
    }

    const headers = { Authorization: `Bearer ${token}` }
    
    // Определяем следующий статус
    let newStatus: Request['status'] = 'in_progress'
    if (request.status === 'new') {
      newStatus = 'in_progress'
    } else if (request.status === 'in_progress') {
      newStatus = 'resolved'
    }

    await axios.put(`/api/requests/${request.id}`, { status: newStatus }, { headers })
    await fetchData()
  } catch (error) {
    console.error('Ошибка при обновлении статуса:', error)
  }
}

// Вспомогательные функции для стилей
const priorityClasses = {
  low: 'px-2 py-1 text-sm rounded-full bg-gray-100 text-gray-800',
  medium: 'px-2 py-1 text-sm rounded-full bg-yellow-100 text-yellow-800',
  high: 'px-2 py-1 text-sm rounded-full bg-orange-100 text-orange-800',
  critical: 'px-2 py-1 text-sm rounded-full bg-red-100 text-red-800'
} as const

const statusClasses = {
  new: 'px-2 py-1 text-sm rounded-full bg-blue-100 text-blue-800',
  in_progress: 'px-2 py-1 text-sm rounded-full bg-yellow-100 text-yellow-800',
  resolved: 'px-2 py-1 text-sm rounded-full bg-green-100 text-green-800'
} as const

const getPriorityClass = (priority: Request['priority'] | undefined) => {
  if (!priority) return priorityClasses.low;
  return priorityClasses[priority];
}

const getStatusClass = (status: Request['status']) => {
  return statusClasses[status]
}

// Загрузка данных при монтировании
onMounted(fetchData)
</script> 
