<template>
  <div v-if="isOpen" class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2>Управление заявками</h2>
        <button class="close-button" @click="closeModal">&times;</button>
      </div>

      <div class="requests-container">
        <div class="filters">
          <select v-model="statusFilter" class="filter-select">
            <option value="">Все статусы</option>
            <option value="new">Новые</option>
            <option value="in_progress">В работе</option>
            <option value="completed">Завершенные</option>
          </select>

          <select v-model="priorityFilter" class="filter-select">
            <option value="">Все приоритеты</option>
            <option value="low">Низкий</option>
            <option value="medium">Средний</option>
            <option value="high">Высокий</option>
          </select>
        </div>

        <div class="requests-list" v-if="requests.length">
          <div v-for="request in filteredRequests" :key="request.id" class="request-card">
            <div class="request-header">
              <h3>{{ request.title }}</h3>
              <span :class="['status-badge', request.status]">{{ getStatusText(request.status) }}</span>
            </div>
            
            <p class="request-description">{{ request.description }}</p>
            
            <div class="request-info">
              <span class="priority-badge" :class="request.priority">
                {{ getPriorityText(request.priority) }}
              </span>
              <span class="employee-name">{{ request.employee_name }}</span>
              <span class="request-date">{{ formatDate(request.created_at) }}</span>
            </div>

            <div class="request-actions">
              <select 
                v-model="request.status" 
                class="status-select"
                @change="updateRequestStatus(request.id, request.status)"
              >
                <option value="new">Новая</option>
                <option value="in_progress">В работе</option>
                <option value="completed">Завершена</option>
              </select>
            </div>
          </div>
        </div>
        
        <div v-else class="no-requests">
          <p>Заявок не найдено</p>
        </div>
      </div>
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
      required: true
    }
  },
  data() {
    return {
      requests: [],
      statusFilter: '',
      priorityFilter: '',
      isLoading: false
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
      return date.toLocaleDateString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      })
    },
    async fetchRequests() {
      try {
        const response = await axios.get('/api/requests', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('admin_token')}`
          },
          validateStatus: function (status) {
            return status < 500
          }
        })

        if (response.status === 307) {
          const redirectUrl = response.headers.location
          const finalResponse = await axios.get(redirectUrl, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('admin_token')}`
            }
          })
          this.requests = finalResponse.data
        } else {
          this.requests = response.data
        }

        // Получаем информацию о сотрудниках для отображения имен
        const employeesResponse = await axios.get('/api/employees', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('admin_token')}`
          }
        })
        const employees = employeesResponse.data
        
        // Добавляем имена сотрудников к заявкам
        this.requests = this.requests.map(request => {
          const employee = employees.find(emp => emp.id === request.employee_id)
          return {
            ...request,
            employee_name: employee ? `${employee.last_name} ${employee.first_name}` : 'Неизвестный сотрудник'
          }
        })
      } catch (error) {
        console.error('Error fetching requests:', error)
      }
    },
    async updateRequestStatus(requestId, newStatus) {
      try {
        await axios.patch(`/api/requests/${requestId}`, 
          { status: newStatus },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('admin_token')}`
            }
          }
        )
      } catch (error) {
        console.error('Error updating request status:', error)
      }
    }
  },
  watch: {
    isOpen(newValue) {
      if (newValue) {
        this.fetchRequests()
      }
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
  max-width: 1000px;
  max-height: 90vh;
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
  margin-bottom: 1.5rem;
}

.filter-select {
  padding: 0.5rem;
  border: 2px solid #e0e0e0;
  border-radius: 6px;
  font-size: 1rem;
  color: #1a237e;
  background-color: white;
}

.requests-list {
  display: grid;
  gap: 1rem;
}

.request-card {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
  border: 1px solid #e0e0e0;
}

.request-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.request-header h3 {
  margin: 0;
  color: #1a237e;
  font-size: 1.2rem;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  font-size: 0.875rem;
  font-weight: 500;
}

.status-badge.new {
  background-color: #e3f2fd;
  color: #1976d2;
}

.status-badge.in_progress {
  background-color: #fff3e0;
  color: #f57c00;
}

.status-badge.completed {
  background-color: #e8f5e9;
  color: #388e3c;
}

.request-description {
  margin: 0 0 1rem 0;
  color: #666;
}

.request-info {
  display: flex;
  gap: 1rem;
  align-items: center;
  margin-bottom: 1rem;
}

.priority-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  font-size: 0.875rem;
  font-weight: 500;
}

.priority-badge.low {
  background-color: #e8f5e9;
  color: #388e3c;
}

.priority-badge.medium {
  background-color: #fff3e0;
  color: #f57c00;
}

.priority-badge.high {
  background-color: #fbe9e7;
  color: #d32f2f;
}

.employee-name {
  color: #1a237e;
  font-weight: 500;
}

.request-date {
  color: #666;
  font-size: 0.875rem;
}

.request-actions {
  display: flex;
  justify-content: flex-end;
}

.status-select {
  padding: 0.5rem;
  border: 2px solid #e0e0e0;
  border-radius: 6px;
  font-size: 0.875rem;
  color: #1a237e;
  background-color: white;
  cursor: pointer;
}

.no-requests {
  text-align: center;
  padding: 2rem;
  color: #666;
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
    align-items: flex-start;
    gap: 0.5rem;
  }

  .request-info {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style> 