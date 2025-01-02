<template>
  <div class="admin-dashboard">
    <div class="dashboard-header">
      <h1>Панель администратора</h1>
      <button @click="logout" class="logout-button">Выйти</button>
    </div>

    <div class="dashboard-content">
      <div class="action-buttons">
        <button @click="showAddEmployeeModal = true" class="action-button">
          Добавить сотрудника
        </button>
        <button @click="showEmployeesModal = true" class="action-button">
          Список сотрудников
        </button>
        <button @click="showRequestsModal = true" class="action-button">
          Управление заявками
        </button>
      </div>

      <!-- Модальные окна -->
      <AddEmployeeModal
        v-if="showAddEmployeeModal"
        :isOpen="showAddEmployeeModal"
        @close="showAddEmployeeModal = false"
        @employee-added="handleEmployeeAdded"
      />

      <EmployeesModal
        v-if="showEmployeesModal"
        :isOpen="showEmployeesModal"
        @close="showEmployeesModal = false"
      />

      <RequestsModal
        v-if="showRequestsModal"
        :isOpen="showRequestsModal"
        @close="showRequestsModal = false"
      />
    </div>
  </div>
</template>

<script>
import AddEmployeeModal from '@/components/admin/AddEmployeeModal.vue'
import EmployeesModal from '@/components/admin/EmployeesModal.vue'
import RequestsModal from '@/components/admin/RequestsModal.vue'

export default {
  name: 'AdminDashboardView',
  components: {
    AddEmployeeModal,
    EmployeesModal,
    RequestsModal
  },
  data() {
    return {
      showAddEmployeeModal: false,
      showEmployeesModal: false,
      showRequestsModal: false
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('admin_token')
      this.$router.push('/admin/login')
    },
    handleEmployeeAdded() {
      // Обновляем список сотрудников, если модальное окно списка открыто
      if (this.showEmployeesModal) {
        this.$refs.employeesModal?.fetchEmployees()
      }
    }
  }
}
</script>

<style scoped>
.admin-dashboard {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 3rem;
}

.dashboard-header h1 {
  margin: 0;
  color: #1a237e;
  font-size: 2rem;
}

.logout-button {
  background-color: #f44336;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.logout-button:hover {
  background-color: #d32f2f;
}

.action-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.action-button {
  background-color: #1a237e;
  color: white;
  padding: 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  min-height: 100px;
}

.action-button:hover {
  background-color: #283593;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

@media (max-width: 768px) {
  .admin-dashboard {
    padding: 1rem;
  }

  .dashboard-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
    margin-bottom: 2rem;
  }

  .action-buttons {
    grid-template-columns: 1fr;
  }

  .action-button {
    padding: 1rem;
    min-height: 80px;
  }
}
</style> 