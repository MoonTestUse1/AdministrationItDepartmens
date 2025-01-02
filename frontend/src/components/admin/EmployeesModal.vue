<template>
  <div v-if="isOpen" class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2>Список сотрудников</h2>
        <button class="close-button" @click="closeModal">&times;</button>
      </div>

      <div class="employees-container">
        <div class="search-bar">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Поиск по имени или отделу..."
            class="search-input"
          >
        </div>

        <div class="employees-list" v-if="filteredEmployees.length">
          <div v-for="employee in filteredEmployees" :key="employee.id" class="employee-card">
            <div class="employee-info">
              <h3>{{ employee.last_name }} {{ employee.first_name }}</h3>
              <p class="department">{{ employee.department }}</p>
            </div>

            <div class="employee-actions">
              <button class="edit-button" @click="editEmployee(employee)">
                Изменить
              </button>
              <button class="delete-button" @click="deleteEmployee(employee.id)">
                Удалить
              </button>
            </div>
          </div>
        </div>
        
        <div v-else class="no-employees">
          <p>Сотрудники не найдены</p>
        </div>
      </div>
    </div>

    <!-- Модальное окно редактирования -->
    <div v-if="editingEmployee" class="edit-modal">
      <div class="edit-modal-content" @click.stop>
        <h3>Редактировать сотрудника</h3>
        
        <form @submit.prevent="saveEmployee" class="edit-form">
          <div class="form-group">
            <label>Имя</label>
            <input
              type="text"
              v-model="editingEmployee.first_name"
              required
              class="form-input"
            >
          </div>

          <div class="form-group">
            <label>Фамилия</label>
            <input
              type="text"
              v-model="editingEmployee.last_name"
              required
              class="form-input"
            >
          </div>

          <div class="form-group">
            <label>Отдел</label>
            <input
              type="text"
              v-model="editingEmployee.department"
              required
              class="form-input"
            >
          </div>

          <div class="form-actions">
            <button type="submit" class="save-button">Сохранить</button>
            <button type="button" class="cancel-button" @click="cancelEdit">
              Отмена
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'EmployeesModal',
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
      editingEmployee: null,
      isLoading: false
    }
  },
  computed: {
    filteredEmployees() {
      const query = this.searchQuery.toLowerCase()
      return this.employees.filter(employee => {
        const fullName = `${employee.last_name} ${employee.first_name}`.toLowerCase()
        const department = employee.department.toLowerCase()
        return fullName.includes(query) || department.includes(query)
      })
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
          }
        })
        this.employees = response.data
      } catch (error) {
        console.error('Error fetching employees:', error)
      }
    },
    editEmployee(employee) {
      this.editingEmployee = { ...employee }
    },
    cancelEdit() {
      this.editingEmployee = null
    },
    async saveEmployee() {
      try {
        await axios.put(`/api/employees/${this.editingEmployee.id}`,
          this.editingEmployee,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('admin_token')}`
            }
          }
        )
        
        await this.fetchEmployees()
        this.editingEmployee = null
      } catch (error) {
        console.error('Error updating employee:', error)
      }
    },
    async deleteEmployee(employeeId) {
      if (!confirm('Вы уверены, что хотите удалить этого сотрудника?')) {
        return
      }

      try {
        await axios.delete(`/api/employees/${employeeId}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('admin_token')}`
          }
        })
        
        await this.fetchEmployees()
      } catch (error) {
        console.error('Error deleting employee:', error)
      }
    }
  },
  watch: {
    isOpen(newValue) {
      if (newValue) {
        this.fetchEmployees()
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
  max-width: 800px;
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

.search-bar {
  margin-bottom: 1.5rem;
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
  gap: 1rem;
}

.employee-card {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
  border: 1px solid #e0e0e0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.employee-info h3 {
  margin: 0 0 0.5rem 0;
  color: #1a237e;
  font-size: 1.2rem;
}

.department {
  margin: 0;
  color: #666;
}

.employee-actions {
  display: flex;
  gap: 0.5rem;
}

.edit-button, .delete-button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
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
  background-color: #fbe9e7;
  color: #d32f2f;
}

.delete-button:hover {
  background-color: #ffcdd2;
}

.no-employees {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.edit-modal {
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

.edit-modal-content {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  color: #1a237e;
  font-weight: 500;
}

.form-input {
  padding: 0.75rem;
  border: 2px solid #e0e0e0;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-input:focus {
  outline: none;
  border-color: #1a237e;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.save-button {
  flex: 1;
  background-color: #1a237e;
  color: white;
  padding: 0.75rem;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.save-button:hover {
  background-color: #283593;
}

.cancel-button {
  flex: 1;
  background-color: #f5f5f5;
  color: #666;
  padding: 0.75rem;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.cancel-button:hover {
  background-color: #e0e0e0;
  color: #1a237e;
}

@media (max-width: 768px) {
  .modal-content {
    padding: 1rem;
    width: 95%;
  }

  .employee-card {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .employee-actions {
    width: 100%;
    justify-content: center;
  }
}
</style> 