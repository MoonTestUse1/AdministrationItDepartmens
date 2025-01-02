<template>
  <header class="admin-header">
    <div class="header-container">
      <router-link to="/admin/dashboard" class="logo">
        <h1>IT Support</h1>
      </router-link>
      
      <nav class="nav-menu">
        <router-link to="/admin/dashboard" class="nav-link">Главная</router-link>
        <router-link to="/admin/requests" class="nav-link">Заявки</router-link>
        <router-link to="/admin/employees" class="nav-link">Сотрудники</router-link>
      </nav>
      
      <button @click="handleLogout" class="logout-button">
        Выйти
      </button>
    </div>
  </header>
</template>

<script>
export default {
  name: 'AdminHeader',
  methods: {
    handleLogout() {
      localStorage.removeItem('admin_token')
      this.$router.push('/admin/login')
    }
  }
}
</script>

<style scoped>
.admin-header {
  background-color: #1a237e;
  color: white;
  padding: 1rem;
}

.header-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  text-decoration: none;
  color: white;
}

.logo h1 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
}

.nav-menu {
  display: flex;
  gap: 1.5rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.logout-button {
  background: transparent;
  border: 2px solid white;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.logout-button:hover {
  background-color: white;
  color: #1a237e;
}

@media (max-width: 768px) {
  .header-container {
    flex-direction: column;
    gap: 1rem;
  }
  
  .nav-menu {
    flex-direction: column;
    align-items: center;
  }
}
</style> 