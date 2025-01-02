<template>
  <header class="admin-header">
    <div class="header-content">
      <div class="logo">
        <h1>IT Support</h1>
      </div>
      <nav class="nav-menu">
        <router-link to="/admin/dashboard" class="nav-link">Панель управления</router-link>
        <router-link to="/admin/employees" class="nav-link">Сотрудники</router-link>
        <router-link to="/admin/requests" class="nav-link">Заявки</router-link>
        <a @click="logout" class="nav-link logout">Выйти</a>
      </nav>
    </div>
  </header>
</template>

<script>
export default {
  name: 'AdminHeader',
  methods: {
    logout() {
      localStorage.removeItem('admin_token');
      this.$router.push('/admin/login');
    }
  }
}
</script>

<style scoped>
.admin-header {
  background-color: #1a237e;
  color: white;
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo h1 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
}

.nav-menu {
  display: flex;
  gap: 2rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.nav-link.router-link-active {
  background-color: rgba(255, 255, 255, 0.2);
}

.logout {
  cursor: pointer;
  color: #ff5252;
}

.logout:hover {
  background-color: rgba(255, 82, 82, 0.1);
}
</style> 