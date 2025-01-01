<template>
  <div class="min-h-screen bg-gray-900 flex">
    <!-- Основной контент -->
    <div class="flex-1">
      <!-- Верхняя панель -->
      <header class="bg-navy-900 border-b border-navy-700">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="flex justify-between items-center h-16">
            <h1 class="text-xl font-medium text-white">Панель администратора</h1>
            <button 
              @click="handleLogout"
              class="text-gray-300 hover:text-white font-medium transition-colors"
            >
              Выйти
            </button>
          </div>
        </div>
      </header>

      <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <!-- Статистика -->
        <div v-if="activeSection === 'statistics'" class="space-y-8">
          <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
            <div class="bg-navy-800 p-6 rounded-lg border border-navy-700">
              <div class="text-sm font-medium text-gray-400 mb-1">Новые заявки</div>
              <div class="text-2xl font-medium text-white">{{ statistics.new || 0 }}</div>
            </div>
            <div class="bg-navy-800 p-6 rounded-lg border border-navy-700">
              <div class="text-sm font-medium text-gray-400 mb-1">В работе</div>
              <div class="text-2xl font-medium text-white">{{ statistics.inProgress || 0 }}</div>
            </div>
            <div class="bg-navy-800 p-6 rounded-lg border border-navy-700">
              <div class="text-sm font-medium text-gray-400 mb-1">Решенные</div>
              <div class="text-2xl font-medium text-white">{{ statistics.resolved || 0 }}</div>
            </div>
          </div>
        </div>

        <!-- Заявки -->
        <div v-if="activeSection === 'requests'" class="space-y-8">
          <div class="bg-navy-800 rounded-lg overflow-hidden border border-navy-700">
            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-navy-700">
                <thead>
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider bg-navy-900">ID</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider bg-navy-900">Сотрудник</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider bg-navy-900">Отдел</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider bg-navy-900">Тип</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider bg-navy-900">Приоритет</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider bg-navy-900">Статус</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider bg-navy-900">Действия</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-navy-700">
                  <tr v-for="request in requests" :key="request.id" class="hover:bg-navy-700">
                    <td class="px-6 py-4 text-sm text-gray-300">{{ request.id }}</td>
                    <td class="px-6 py-4">
                      <div class="text-sm text-gray-300">{{ request.employee?.last_name }}</div>
                      <div class="text-sm text-gray-400">{{ request.employee?.first_name }}</div>
                    </td>
                    <td class="px-6 py-4 text-sm text-gray-300">{{ request.department }}</td>
                    <td class="px-6 py-4 text-sm text-gray-300">{{ request.request_type }}</td>
                    <td class="px-6 py-4">
                      <span :class="getPriorityClass(request.priority)">{{ request.priority }}</span>
                    </td>
                    <td class="px-6 py-4">
                      <span :class="getStatusClass(request.status)">{{ request.status }}</span>
                    </td>
                    <td class="px-6 py-4 text-sm">
                      <button
                        @click="openRequestDetails(request)"
                        class="text-blue-400 hover:text-blue-300 mr-3"
                      >
                        Подробнее
                      </button>
                      <button
                        v-if="request.status !== 'resolved'"
                        @click="updateRequestStatus(request)"
                        class="text-blue-400 hover:text-blue-300"
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
        <div v-if="activeSection === 'employees'" class="space-y-8">
          <div class="flex justify-end mb-4">
            <button
              @click="openAddEmployeeModal"
              class="inline-flex items-center px-4 py-2 text-sm font-medium text-blue-400 hover:text-blue-300 transition-colors"
            >
              + Добавить сотрудника
            </button>
          </div>
          <div class="bg-navy-800 rounded-lg overflow-hidden border border-navy-700">
            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-navy-700">
                <thead>
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider bg-navy-900">ID</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider bg-navy-900">Имя</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider bg-navy-900">Фамилия</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider bg-navy-900">Отдел</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider bg-navy-900">Кабинет</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider bg-navy-900">Действия</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-navy-700">
                  <tr v-for="employee in employees" :key="employee.id" class="hover:bg-navy-700">
                    <td class="px-6 py-4 text-sm text-gray-300">{{ employee.id }}</td>
                    <td class="px-6 py-4 text-sm text-gray-300">{{ employee.first_name }}</td>
                    <td class="px-6 py-4 text-sm text-gray-300">{{ employee.last_name }}</td>
                    <td class="px-6 py-4 text-sm text-gray-300">{{ employee.department }}</td>
                    <td class="px-6 py-4 text-sm text-gray-300">{{ employee.office }}</td>
                    <td class="px-6 py-4 text-sm">
                      <button
                        @click="openEditEmployeeModal(employee)"
                        class="text-blue-400 hover:text-blue-300"
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

    <!-- Боковое меню -->
    <div class="w-64 bg-navy-900 border-l border-navy-700">
      <div class="p-4">
        <nav class="space-y-2">
          <button
            @click="activeSection = 'statistics'"
            :class="[
              'w-full px-4 py-2 text-left rounded-lg text-sm font-medium transition-colors',
              activeSection === 'statistics'
                ? 'bg-blue-500 text-white'
                : 'text-gray-300 hover:bg-navy-800'
            ]"
          >
            Статистика
          </button>
          <button
            @click="activeSection = 'requests'"
            :class="[
              'w-full px-4 py-2 text-left rounded-lg text-sm font-medium transition-colors',
              activeSection === 'requests'
                ? 'bg-blue-500 text-white'
                : 'text-gray-300 hover:bg-navy-800'
            ]"
          >
            Заявки
          </button>
          <button
            @click="activeSection = 'employees'"
            :class="[
              'w-full px-4 py-2 text-left rounded-lg text-sm font-medium transition-colors',
              activeSection === 'employees'
                ? 'bg-blue-500 text-white'
                : 'text-gray-300 hover:bg-navy-800'
            ]"
          >
            Сотрудники
          </button>
        </nav>
      </div>
    </div>

    <!-- Модальное окно для заявки -->
    <div v-if="showRequestModal" class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center p-4">
      <div class="bg-navy-800 rounded-lg max-w-2xl w-full border border-navy-700">
        <div class="flex justify-between items-center p-6 border-b border-navy-700">
          <h3 class="text-lg font-medium text-white">Заявка #{{ selectedRequest?.id }}</h3>
          <button @click="showRequestModal = false" class="text-gray-400 hover:text-gray-300">
            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="p-6">
          <div class="space-y-4">
            <div>
              <div class="text-sm font-medium text-gray-400">Описание</div>
              <div class="mt-1 text-sm text-gray-300">{{ selectedRequest?.description }}</div>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <div class="text-sm font-medium text-gray-400">Сотрудник</div>
                <div class="mt-1 text-sm text-gray-300">
                  {{ selectedRequest?.employee?.last_name }} {{ selectedRequest?.employee?.first_name }}
                </div>
              </div>
              <div>
                <div class="text-sm font-medium text-gray-400">Отдел</div>
                <div class="mt-1 text-sm text-gray-300">{{ selectedRequest?.department }}</div>
              </div>
              <div>
                <div class="text-sm font-medium text-gray-400">Тип заявки</div>
                <div class="mt-1 text-sm text-gray-300">{{ selectedRequest?.request_type }}</div>
              </div>
              <div>
                <div class="text-sm font-medium text-gray-400">Приоритет</div>
                <div class="mt-1">
                  <span :class="getPriorityClass(selectedRequest?.priority)">
                    {{ selectedRequest?.priority }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="flex justify-end gap-3 p-6 border-t border-navy-700 bg-navy-900">
          <button
            @click="showRequestModal = false"
            class="px-4 py-2 text-sm font-medium text-gray-400 hover:text-gray-300"
          >
            Закрыть
          </button>
          <button
            v-if="selectedRequest?.status !== 'resolved'"
            @click="updateRequestStatus(selectedRequest)"
            class="px-4 py-2 text-sm font-medium text-blue-400 hover:text-blue-300"
          >
            {{ selectedRequest?.status === 'new' ? 'Взять в работу' : 'Завершить' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Модальное окно для сотрудника -->
    <div v-if="showEmployeeModal" class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center p-4">
      <div class="bg-navy-800 rounded-lg max-w-md w-full border border-navy-700">
        <div class="flex justify-between items-center p-6 border-b border-navy-700">
          <h3 class="text-lg font-medium text-white">
            {{ isEditingEmployee ? 'Редактировать сотрудника' : 'Добавить сотрудника' }}
          </h3>
          <button @click="showEmployeeModal = false" class="text-gray-400 hover:text-gray-300">
            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <form @submit.prevent="handleEmployeeSubmit" class="p-6">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-400">Имя</label>
              <input
                v-model="employeeForm.first_name"
                type="text"
                required
                class="mt-1 block w-full rounded-md bg-navy-900 border-navy-700 text-gray-300 focus:border-blue-500 focus:ring-0"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-400">Фамилия</label>
              <input
                v-model="employeeForm.last_name"
                type="text"
                required
                class="mt-1 block w-full rounded-md bg-navy-900 border-navy-700 text-gray-300 focus:border-blue-500 focus:ring-0"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-400">Отдел</label>
              <input
                v-model="employeeForm.department"
                type="text"
                required
                class="mt-1 block w-full rounded-md bg-navy-900 border-navy-700 text-gray-300 focus:border-blue-500 focus:ring-0"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-400">Кабинет</label>
              <input
                v-model="employeeForm.office"
                type="text"
                required
                class="mt-1 block w-full rounded-md bg-navy-900 border-navy-700 text-gray-300 focus:border-blue-500 focus:ring-0"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-400">
                Пароль {{ isEditingEmployee ? '(оставьте пустым, чтобы не менять)' : '' }}
              </label>
              <input
                v-model="employeeForm.password"
                type="password"
                :required="!isEditingEmployee"
                class="mt-1 block w-full rounded-md bg-navy-900 border-navy-700 text-gray-300 focus:border-blue-500 focus:ring-0"
              />
            </div>
          </div>
        </form>
        <div class="flex justify-end gap-3 p-6 border-t border-navy-700 bg-navy-900">
          <button
            type="button"
            @click="showEmployeeModal = false"
            class="px-4 py-2 text-sm font-medium text-gray-400 hover:text-gray-300"
          >
            Отмена
          </button>
          <button
            type="submit"
            class="px-4 py-2 text-sm font-medium text-blue-400 hover:text-blue-300"
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
const activeSection = ref('statistics')
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

const priorityClasses = {
  low: 'px-2 py-1 text-xs rounded-full bg-navy-700 text-blue-300',
  medium: 'px-2 py-1 text-xs rounded-full bg-yellow-900 text-yellow-300',
  high: 'px-2 py-1 text-xs rounded-full bg-orange-900 text-orange-300',
  critical: 'px-2 py-1 text-xs rounded-full bg-red-900 text-red-300'
} as const

const statusClasses = {
  new: 'px-2 py-1 text-xs rounded-full bg-navy-700 text-blue-300',
  in_progress: 'px-2 py-1 text-xs rounded-full bg-blue-900 text-blue-300',
  resolved: 'px-2 py-1 text-xs rounded-full bg-green-900 text-green-300'
} as const

const getPriorityClass = (priority: Request['priority'] | undefined) => {
  if (!priority) return priorityClasses.low;
  return priorityClasses[priority];
}

const getStatusClass = (status: Request['status']) => {
  return statusClasses[status]
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
