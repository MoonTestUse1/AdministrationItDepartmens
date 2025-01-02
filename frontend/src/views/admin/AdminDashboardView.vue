<template>
  <div class="admin-layout">
    <AdminHeader />
    <main class="admin-main">
      <div class="dashboard-container">
        <h1 class="dashboard-title">Панель управления</h1>
        
        <div class="stats-grid">
          <div class="stat-card">
            <h3>Всего заявок</h3>
            <p class="stat-number">{{ statistics.total_requests || 0 }}</p>
          </div>
          
          <div class="stat-card">
            <h3>Новые заявки</h3>
            <p class="stat-number">{{ statistics.by_status?.new || 0 }}</p>
          </div>
          
          <div class="stat-card">
            <h3>В работе</h3>
            <p class="stat-number">{{ statistics.by_status?.in_progress || 0 }}</p>
          </div>
          
          <div class="stat-card">
            <h3>Завершенные</h3>
            <p class="stat-number">{{ statistics.by_status?.completed || 0 }}</p>
          </div>
        </div>

        <div class="actions-grid">
          <router-link to="/admin/employees/add" class="action-card">
            <div class="action-icon">👥</div>
            <h3>Добавить сотрудника</h3>
            <p>Регистрация нового сотрудника в системе</p>
          </router-link>

          <router-link to="/admin/requests" class="action-card">
            <div class="action-icon">📝</div>
            <h3>Управление заявками</h3>
            <p>Просмотр и обработка заявок</p>
          </router-link>

          <router-link to="/admin/employees" class="action-card">
            <div class="action-icon">👤</div>
            <h3>Список сотрудников</h3>
            <p>Управление учетными записями</p>
          </router-link>
        </div>
      </div>
    </main>
    <AdminFooter />
  </div>
</template>

<script>
import AdminHeader from '@/components/AdminHeader.vue'
import AdminFooter from '@/components/AdminFooter.vue'
import axios from 'axios'

export default {
  name: 'AdminDashboardView',
  components: {
    AdminHeader,
    AdminFooter
  },
  data() {
    return {
      statistics: {
        total_requests: 0,
        by_status: {},
        by_priority: {}
      }
    }
  },
  async created() {
    try {
      const response = await axios.get('/api/requests/statistics', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('admin_token')}`
        }
      });
      this.statistics = response.data;
    } catch (error) {
      console.error('Error fetching statistics:', error);
    }
  }
}
</script>

<style scoped>
.admin-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f5f5;
}

.admin-main {
  flex: 1;
  padding: 2rem;
}

.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
}

.dashboard-title {
  color: #1a237e;
  margin-bottom: 2rem;
  font-size: 2rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.stat-card h3 {
  color: #1a237e;
  margin: 0 0 1rem 0;
  font-size: 1.1rem;
}

.stat-number {
  font-size: 2rem;
  font-weight: bold;
  color: #1a237e;
  margin: 0;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.action-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-decoration: none;
  color: inherit;
  transition: transform 0.3s, box-shadow 0.3s;
}

.action-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.action-icon {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.action-card h3 {
  color: #1a237e;
  margin: 0 0 0.5rem 0;
}

.action-card p {
  margin: 0;
  color: #666;
}

@media (max-width: 768px) {
  .admin-main {
    padding: 1rem;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .actions-grid {
    grid-template-columns: 1fr;
  }
}
</style> 