<!-- AdminFooter.vue -->
<template>
  <footer class="admin-footer">
    <div class="footer-container">
      <div class="footer-content">
        <div class="footer-section">
          <h3>IT Support</h3>
          <p>Система управления заявками технической поддержки</p>
        </div>
        
        <div class="footer-section">
          <h3>Навигация</h3>
          <nav class="footer-nav">
            <router-link to="/admin/dashboard">Главная</router-link>
            <router-link to="/admin/requests">Заявки</router-link>
            <router-link to="/admin/employees">Сотрудники</router-link>
          </nav>
        </div>
      </div>
      
      <div class="footer-bottom">
        <p>&copy; 2024 IT Support. Все права защищены.</p>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'AdminFooter'
}
</script>

<style scoped>
.admin-footer {
  background-color: #1a237e;
  color: white;
  padding: 2rem 1rem;
  margin-top: auto;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.footer-section h3 {
  margin: 0 0 1rem 0;
  font-size: 1.2rem;
  font-weight: 600;
}

.footer-section p {
  margin: 0;
  color: rgba(255, 255, 255, 0.8);
}

.footer-nav {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.footer-nav a {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: color 0.3s;
}

.footer-nav a:hover {
  color: white;
}

.footer-bottom {
  padding-top: 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  text-align: center;
}

.footer-bottom p {
  margin: 0;
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .footer-content {
    grid-template-columns: 1fr;
    text-align: center;
  }
  
  .footer-nav {
    align-items: center;
  }
}
</style> 