<template>
  <div class="min-h-screen bg-gray-100">
    <!-- Верхняя панель -->
    <nav class="bg-blue-800 shadow-lg">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex">
            <div class="flex-shrink-0 flex items-center">
              <h1 class="text-xl font-bold text-white">IT Support Admin</h1>
            </div>
          </div>
          <div class="flex items-center">
            <button
              @click="handleLogout"
              class="ml-3 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-blue-800 bg-white hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Выйти
            </button>
          </div>
        </div>
      </div>
    </nav>

    <div class="flex">
      <!-- Боковая панель -->
      <aside class="w-64 bg-white shadow-lg h-screen">
        <nav class="mt-5 px-2">
          <a 
            href="#statistics" 
            class="group flex items-center px-2 py-2 text-base font-medium rounded-md text-blue-800 hover:bg-blue-50"
            :class="{ 'bg-blue-50': activeTab === 'statistics' }"
            @click="activeTab = 'statistics'"
          >
            Статистика
          </a>
          <a 
            href="#requests" 
            class="mt-1 group flex items-center px-2 py-2 text-base font-medium rounded-md text-blue-800 hover:bg-blue-50"
            :class="{ 'bg-blue-50': activeTab === 'requests' }"
            @click="activeTab = 'requests'"
          >
            Заявки
          </a>
          <a 
            href="#employees" 
            class="mt-1 group flex items-center px-2 py-2 text-base font-medium rounded-md text-blue-800 hover:bg-blue-50"
            :class="{ 'bg-blue-50': activeTab === 'employees' }"
            @click="activeTab = 'employees'"
          >
            Сотрудники
          </a>
        </nav>
      </aside>

      <!-- Основной контент -->
      <main class="flex-1 p-8">
        <!-- Статистика -->
        <div v-if="activeTab === 'statistics'" class="bg-white shadow-lg rounded-lg p-6">
          <h2 class="text-2xl font-bold text-gray-900 mb-6">Статистика заявок</h2>
          <div class="grid grid-cols-1 gap-5 sm:grid-cols-3">
            <div class="bg-white overflow-hidden shadow rounded-lg border-l-4 border-blue-400">
              <div class="px-4 py-5 sm:p-6">
                <dt class="text-sm font-medium text-gray-500 truncate">Новые заявки</dt>
                <dd class="mt-1 text-3xl font-semibold text-blue-600">{{ statistics.new || 0 }}</dd>
              </div>
            </div>
            <div class="bg-white overflow-hidden shadow rounded-lg border-l-4 border-yellow-400">
              <div class="px-4 py-5 sm:p-6">
                <dt class="text-sm font-medium text-gray-500 truncate">В работе</dt>
                <dd class="mt-1 text-3xl font-semibold text-yellow-600">{{ statistics.inProgress || 0 }}</dd>
              </div>
            </div>
            <div class="bg-white overflow-hidden shadow rounded-lg border-l-4 border-green-400">
              <div class="px-4 py-5 sm:p-6">
                <dt class="text-sm font-medium text-gray-500 truncate">Решенные</dt>
                <dd class="mt-1 text-3xl font-semibold text-green-600">{{ statistics.resolved || 0 }}</dd>
              </div>
            </div>
          </div>
        </div>

        <!-- Заявки -->
        <div v-if="activeTab === 'requests'" class="bg-white shadow-lg rounded-lg p-6">
          <h2 class="text-2xl font-bold text-gray-900 mb-6">Список заявок</h2>
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Сотрудник</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Отдел</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Кабинет</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Тип</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Описание</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Срочность</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Статус</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Действия</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="request in requests" :key="request.id">
                  <td class="px-6 py-4 whitespace-nowrap">
                    {{ request.employee.last_name }} {{ request.employee.first_name }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">{{ request.employee.department }}</td>
                  <td class="px-6 py-4 whitespace-nowrap">{{ request.employee.office }}</td>
                  <td class="px-6 py-4 whitespace-nowrap">{{ request.request_type }}</td>
                  <td class="px-6 py-4">
                    <button 
                      @click="openRequestDetails(request)"
                      class="text-blue-600 hover:text-blue-900"
                    >
                      Просмотр
                    </button>
                  </td>
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
                  <td class="px-6 py-4 whitespace-nowrap">
                    <button 
                      @click="updateRequestStatus(request)"
                      class="text-blue-600 hover:text-blue-900"
                    >
                      Изменить статус
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Сотрудники -->
        <div v-if="activeTab === 'employees'" class="bg-white shadow-lg rounded-lg p-6">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold text-gray-900">Список сотрудников</h2>
            <button
              @click="openAddEmployeeModal"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Добавить сотрудника
            </button>
          </div>
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Фамилия</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Имя</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Отдел</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Кабинет</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Должность</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Действия</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="employee in employees" :key="employee.id">
                  <td class="px-6 py-4 whitespace-nowrap">{{ employee.last_name }}</td>
                  <td class="px-6 py-4 whitespace-nowrap">{{ employee.first_name }}</td>
                  <td class="px-6 py-4 whitespace-nowrap">{{ employee.department }}</td>
                  <td class="px-6 py-4 whitespace-nowrap">{{ employee.office }}</td>
                  <td class="px-6 py-4 whitespace-nowrap">{{ employee.position }}</td>
                  <td class="px-6 py-4 whitespace-nowrap">
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
      </main>
    </div>

    <!-- Модальное окно для просмотра заявки -->
    <div v-if="showRequestModal" class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center p-4">
      <div class="bg-white rounded-lg max-w-2xl w-full p-6">
        <div class="flex justify-between items-start mb-4">
          <h3 class="text-lg font-medium text-gray-900">Детали заявки</h3>
          <button @click="showRequestModal = false" class="text-gray-400 hover:text-gray-500">
            <span class="sr-only">Закрыть</span>
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="space-y-4" v-if="selectedRequest">
          <div>
            <h4 class="text-sm font-medium text-gray-500">Сотрудник</h4>
            <p class="mt-1">{{ selectedRequest.employee.last_name }} {{ selectedRequest.employee.first_name }}</p>
          </div>
          <div>
            <h4 class="text-sm font-medium text-gray-500">Отдел</h4>
            <p class="mt-1">{{ selectedRequest.employee.department }}</p>
          </div>
          <div>
            <h4 class="text-sm font-medium text-gray-500">Кабинет</h4>
            <p class="mt-1">{{ selectedRequest.employee.office }}</p>
          </div>
          <div>
            <h4 class="text-sm font-medium text-gray-500">Тип проблемы</h4>
            <p class="mt-1">{{ selectedRequest.request_type }}</p>
          </div>
          <div>
            <h4 class="text-sm font-medium text-gray-500">Описание</h4>
            <p class="mt-1">{{ selectedRequest.description }}</p>
          </div>
          <div>
            <h4 class="text-sm font-medium text-gray-500">Срочность</h4>
            <p class="mt-1">
              <span :class="getPriorityClass(selectedRequest.priority)">
                {{ selectedRequest.priority }}
              </span>
            </p>
          </div>
          <div>
            <h4 class="text-sm font-medium text-gray-500">Статус</h4>
            <p class="mt-1">
              <span :class="getStatusClass(selectedRequest.status)">
                {{ selectedRequest.status }}
              </span>
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Модальное окно для редактирования сотрудника -->
    <div v-if="showEmployeeModal" class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center p-4">
      <div class="bg-white rounded-lg max-w-md w-full p-6">
        <div class="flex justify-between items-start mb-4">
          <h3 class="text-lg font-medium text-gray-900">
            {{ isEditingEmployee ? 'Редактирование сотрудника' : 'Добавление сотрудника' }}
          </h3>
          <button @click="showEmployeeModal = false" class="text-gray-400 hover:text-gray-500">
            <span class="sr-only">Закрыть</span>
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <form @submit.prevent="handleEmployeeSubmit" class="space-y-4">
          <div>
            <label for="last_name" class="block text-sm font-medium text-gray-700">Фамилия</label>
            <input
              type="text"
              id="last_name"
              v-model="employeeForm.last_name"
              class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              required
            />
          </div>
          <div>
            <label for="first_name" class="block text-sm font-medium text-gray-700">Имя</label>
            <input
              type="text"
              id="first_name"
              v-model="employeeForm.first_name"
              class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              required
            />
          </div>
          <div>
            <label for="department" class="block text-sm font-medium text-gray-700">Отдел</label>
            <input
              type="text"
              id="department"
              v-model="employeeForm.department"
              class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              required
            />
          </div>
          <div>
            <label for="office" class="block text-sm font-medium text-gray-700">Кабинет</label>
            <input
              type="text"
              id="office"
              v-model="employeeForm.office"
              class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              required
            />
          </div>
          <div>
            <label for="position" class="block text-sm font-medium text-gray-700">Должность</label>
            <input
              type="text"
              id="position"
              v-model="employeeForm.position"
              class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              required
            />
          </div>
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">Пароль</label>
            <input
              type="password"
              id="password"
              v-model="employeeForm.password"
              class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              :required="!isEditingEmployee"
            />
          </div>
          <div class="flex justify-end">
            <button
              type="submit"
              class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
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
  position: '',
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
    position: '',
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
    position: employee.position,
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

const updateRequestStatus = async (request: Request) => {
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

const getPriorityClass = (priority: Request['priority']) => {
  return priorityClasses[priority]
}

const getStatusClass = (status: Request['status']) => {
  return statusClasses[status]
}

// Загрузка данных при монтировании
onMounted(fetchData)
</script> 
</script> 