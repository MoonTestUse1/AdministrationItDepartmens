<template>
  <div v-if="isOpen" class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2>Список сотрудников</h2>
        <button class="close-button" @click="closeModal">&times;</button>
      </div>

      <div class="search-bar">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="Поиск сотрудников..."
          class="search-input"
        >
      </div>

      <div class="employees-list">
        <div v-for="employee in filteredEmployees" :key="employee.id" class="employee-card">
          <div class="employee-info">
            <h3>{{ employee.last_name }} {{ employee.first_name }}</h3>
            <p>Отдел: {{ employee.department }}</p>
            <p>Кабинет: {{ employee.office }}</p>
          </div>
          <div class="employee-actions">
            <button @click="editEmployee(employee)" class="edit-button">
              Изменить
            </button>
            <button @click="confirmDelete(employee)" class="delete-button">
              Удалить
            </button>
          </div>
        </div>
      </div>

      <!-- Модальное окно редактирования -->
      <EditEmployeeModal
        v-if="showEditModal"
        :isOpen="showEditModal"
        :employee="selectedEmployee"
        @close="closeEditModal"
        @employee-updated="handleEmployeeUpdated"
      />

      <!-- Модальное окно подтверждения удаления -->
      <div v-if="showDeleteConfirm" class="confirm-modal">
        <div class="confirm-content">
          <h3>Подтверждение удаления</h3>
          <p>Вы действительно хотите удалить сотрудника {{ selectedEmployee?.last_name }} {{ selectedEmployee?.first_name }}?</p>
          <div class="confirm-actions">
            <button @click="deleteEmployee" class="delete-button">Удалить</button>
            <button @click="cancelDelete" class="cancel-button">Отмена</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import EditEmployeeModal from './EditEmployeeModal.vue'

export default {
  name: 'EmployeesModal',
  components: {
    EditEmployeeModal
  },
  props: {
    isOpen: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      employees: [],
      searchQuery: '',
      showEditModal: false,
      showDeleteConfirm: false,
      selectedEmployee: null,
      error: ''
    }
  },
  computed: {
    filteredEmployees() {
      const query = this.searchQuery.toLowerCase()
      return this.employees.filter(employee => 
        employee.last_name.toLowerCase().includes(query) ||
        employee.first_name.toLowerCase().includes(query) ||
        employee.department.toLowerCase().includes(query)
      )
    }
  },
  methods: {
    closeModal() {
      this.$emit('close')
    },
    async fetchEmployees() {
      try {
        const response = await axios.get('/api/employees', {
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
          this.employees = finalResponse.data
        } else {
          this.employees = response.data
        }

        console.log('Fetched employees:', this.employees) // Для отладки
      } catch (error) {
        console.error('Error fetching employees:', error)
        this.employees = []
      }
    },
    editEmployee(employee) {
      this.selectedEmployee = employee
      this.showEditModal = true
    },
    closeEditModal() {
      this.showEditModal = false
      this.selectedEmployee = null
    },
    handleEmployeeUpdated() {
      this.fetchEmployees()
      this.closeEditModal()
    },
    confirmDelete(employee) {
      this.selectedEmployee = employee
      this.showDeleteConfirm = true
    },
    cancelDelete() {
      this.showDeleteConfirm = false
      this.selectedEmployee = null
    },
    async deleteEmployee() {
      try {
        await axios.delete(`/api/employees/${this.selectedEmployee.id}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('admin_token')}`
          }
        })
        this.showDeleteConfirm = false
        this.selectedEmployee = null
        this.fetchEmployees()
      } catch (error) {
        console.error('Error deleting employee:', error)
      }
    }
  },
  watch: {
    isOpen: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.fetchEmployees()
        }
      }
    }
  },
  mounted() {
    this.fetchEmployees()
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

.search-bar {
  margin-bottom: 2rem;
}

.search-input {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e0e0e0;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.search-input:focus {
  outline: none;
  border-color: #1a237e;
}

.employees-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.employee-card {
  background: #f5f5f5;
  border-radius: 8px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.employee-info h3 {
  margin: 0;
  color: #1a237e;
  font-size: 1.2rem;
}

.employee-info p {
  margin: 0.5rem 0;
  color: #666;
}

.employee-actions {
  display: flex;
  gap: 1rem;
}

.edit-button, .delete-button {
  flex: 1;
  padding: 0.5rem;
  border: none;
  border-radius: 4px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s;
}

.edit-button {
  background-color: #1a237e;
  color: white;
}

.edit-button:hover {
  background-color: #283593;
}

.delete-button {
  background-color: #f44336;
  color: white;
}

.delete-button:hover {
  background-color: #d32f2f;
}

.confirm-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1100;
}

.confirm-content {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  width: 100%;
  max-width: 400px;
  text-align: center;
}

.confirm-content h3 {
  margin: 0 0 1rem;
  color: #1a237e;
}

.confirm-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.cancel-button {
  flex: 1;
  background-color: #9e9e9e;
  color: white;
  padding: 0.75rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.cancel-button:hover {
  background-color: #757575;
}
</style> 