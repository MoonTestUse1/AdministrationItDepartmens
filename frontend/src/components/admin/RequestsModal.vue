<template>
  <div v-if="isOpen" class="modal-overlay">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2>Управление заявками</h2>
        <button class="close-button" @click.stop="closeModal">&times;</button>
      </div>

      <div v-if="isLoading" class="loading-state">
        <p>Загрузка заявок...</p>
      </div>

      <div v-else-if="error" class="error-state">
        <p>{{ error }}</p>
        <button @click="fetchRequests" class="retry-button">Повторить</button>
      </div>

      <template v-else>
        <div class="filters">
          <div class="filter-group">
            <label>Статус:</label>
            <select v-model="statusFilter" class="filter-select" @click.stop>
              <option value="">Все статусы</option>
              <option value="new">Новая</option>
              <option value="in_progress">В работе</option>
              <option value="completed">Завершена</option>
            </select>
          </div>

          <div class="filter-group">
            <label>Приоритет:</label>
            <select v-model="priorityFilter" class="filter-select" @click.stop>
              <option value="">Все приоритеты</option>
              <option value="low">Низкий</option>
              <option value="medium">Средний</option>
              <option value="high">Высокий</option>
            </select>
          </div>
        </div>

        <div class="requests-list">
          <div v-for="request in filteredRequests" :key="request.id" class="request-card" @click.stop>
            <div class="request-header">
              <h3>{{ request.title }}</h3>
              <div class="request-meta">
                <span class="status" :class="request.status">{{ getStatusText(request.status) }}</span>
                <span class="priority" :class="request.priority">{{ getPriorityText(request.priority) }}</span>
              </div>
            </div>
            
            <div class="request-body">
              <p class="description">{{ request.description }}</p>
              <p class="employee">Сотрудник: {{ request.employee_name }}</p>
              <p class="date">Создано: {{ formatDate(request.created_at) }}</p>
            </div>

            <div class="request-actions">
              <select 
                v-model="request.status" 
                class="status-select"
                @change.stop="updateRequestStatus(request)"
              >
                <option value="new">Новая</option>
                <option value="in_progress">В работе</option>
                <option value="completed">Завершена</option>
              </select>
            </div>
          </div>

          <div v-if="filteredRequests.length === 0" class="no-requests">
            <p>Заявки не найдены</p>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'RequestsModal',
  props: {
    isOpen: {
      type: Boolean,
      required: true,
      default: false
    }
  },
  data() {
    return {
      requests: [],
      statusFilter: '',
      priorityFilter: '',
      isLoading: false,
      error: null
    }
  },
  computed: {
    filteredRequests() {
      return this.requests.filter(request => {
        const matchStatus = !this.statusFilter || request.status === this.statusFilter
        const matchPriority = !this.priorityFilter || request.priority === this.priorityFilter
        return matchStatus && matchPriority
      })
    }
  },
  methods: {
    closeModal() {
      this.$emit('close')
    },
    async fetchRequests() {
      this.isLoading = true
      try {
        console.log('Token:', localStorage.getItem('admin_token')) // Для отладки токена
        console.log('Fetching requests...') // Для отладки
        const response = await axios.get('/api/admin/requests', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('admin_token')}`
          },
          validateStatus: function (status) {
            return status < 500
          }
        })
        console.log('Requests response:', response) // Для отладки

        // Убедимся, что у нас есть массив заявок
        let requestsData = []
        if (response.status === 307) {
          const redirectUrl = response.headers.location
          console.log('Following redirect to:', redirectUrl) // Для отладки
          const finalResponse = await axios.get(redirectUrl, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('admin_token')}`
            }
          })
          console.log('Final response:', finalResponse) // Для отладки
          requestsData = Array.isArray(finalResponse.data) ? finalResponse.data : []
        } else {
          requestsData = Array.isArray(response.data) ? response.data : []
        }

        console.log('Requests data after processing:', requestsData) // Для отладки

        if (requestsData.length === 0) {
          console.log('No requests found in the response') // Для отладки
          return
        }

        // Получаем информацию о сотрудниках для отображения имен
        const employeesResponse = await axios.get('/api/employees', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('admin_token')}`
          }
        })
        console.log('Employees response:', employeesResponse.data) // Для отладки
        const employees = Array.isArray(employeesResponse.data) ? employeesResponse.data : []
        
        // Добавляем имена сотрудников к заявкам
        this.requests = requestsData.map(request => {
          const employee = employees.find(emp => emp.id === request.employee_id)
          return {
            ...request,
            employee_name: employee ? `${employee.last_name} ${employee.first_name}` : 'Неизвестный сотрудник'
          }
        })
        console.log('Final processed requests:', this.requests) // Для отладки
      } catch (error) {
        console.error('Error fetching requests:', error.response || error)
        this.error = `Ошибка при загрузке заявок: ${error.response?.data?.detail || error.message}`
        this.requests = []
      } finally {
        this.isLoading = false
      }
    },
    async updateRequestStatus(request) {
      try {
        await axios.put(`/api/requests/${request.id}`, {
          status: request.status
        }, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('admin_token')}`
          }
        })
      } catch (error) {
        console.error('Error updating request status:', error)
        this.fetchRequests()
      }
    },
    getStatusText(status) {
      const statusMap = {
        new: 'Новая',
        in_progress: 'В работе',
        completed: 'Завершена'
      }
      return statusMap[status] || status
    },
    getPriorityText(priority) {
      const priorityMap = {
        low: 'Низкий',
        medium: 'Средний',
        high: 'Высокий'
      }
      return priorityMap[priority] || priority
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleString('ru-RU')
    }
  },
  watch: {
    isOpen: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.fetchRequests()
        }
      }
    }
  },
  mounted() {
    if (this.isOpen) {
      this.fetchRequests()
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  width: 90%;
  max-width: 800px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.modal-header h2 {
  margin: 0;
  color: #1a237e;
  font-size: 1.5rem;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #666;
  cursor: pointer;
  padding: 0.5rem;
  transition: color 0.3s;
}

.close-button:hover {
  color: #1a237e;
}

.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-select {
  padding: 0.5rem;
  border: 2px solid #e0e0e0;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.filter-select:focus {
  outline: none;
  border-color: #1a237e;
}

.requests-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.request-card {
  background: #f5f5f5;
  border-radius: 8px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.request-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.request-header h3 {
  margin: 0;
  color: #1a237e;
  font-size: 1.2rem;
}

.request-meta {
  display: flex;
  gap: 0.5rem;
}

.status, .priority {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.875rem;
}

.status.new {
  background-color: #e3f2fd;
  color: #1565c0;
}

.status.in_progress {
  background-color: #fff3e0;
  color: #f57c00;
}

.status.completed {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.priority.low {
  background-color: #f5f5f5;
  color: #616161;
}

.priority.medium {
  background-color: #fff3e0;
  color: #f57c00;
}

.priority.high {
  background-color: #ffebee;
  color: #c62828;
}

.request-body {
  color: #666;
}

.description {
  margin: 0 0 0.5rem 0;
  white-space: pre-wrap;
}

.employee, .date {
  margin: 0;
  font-size: 0.875rem;
  color: #666;
}

.request-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.status-select {
  padding: 0.5rem;
  border: 2px solid #e0e0e0;
  border-radius: 6px;
  font-size: 0.875rem;
  transition: all 0.3s;
}

.status-select:focus {
  outline: none;
  border-color: #1a237e;
}

.no-requests {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.loading-state,
.error-state {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.retry-button {
  background-color: #1a237e;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  margin-top: 1rem;
  transition: background-color 0.3s;
}

.retry-button:hover {
  background-color: #283593;
}

@media (max-width: 768px) {
  .modal-content {
    padding: 1rem;
    width: 95%;
  }

  .filters {
    flex-direction: column;
  }

  .request-header {
    flex-direction: column;
    gap: 0.5rem;
  }

  .request-meta {
    width: 100%;
    justify-content: flex-start;
  }
}
</style> 