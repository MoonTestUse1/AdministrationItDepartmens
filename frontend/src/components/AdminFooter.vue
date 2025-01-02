<!-- AdminFooter.vue -->
<template>
  <footer class="admin-footer">
    <div class="footer-content">
      <div class="footer-info">
        <p>&copy; 2024 IT Support. Все права защищены.</p>
      </div>
      <div class="footer-links">
        <a href="#" class="footer-link">Помощь</a>
        <a href="#" class="footer-link">Политика конфиденциальности</a>
        <a href="#" class="footer-link">Условия использования</a>
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
  padding: 1.5rem 2rem;
  margin-top: auto;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-info p {
  margin: 0;
  font-size: 0.9rem;
}

.footer-links {
  display: flex;
  gap: 2rem;
}

.footer-link {
  color: white;
  text-decoration: none;
  font-size: 0.9rem;
  opacity: 0.8;
  transition: opacity 0.3s;
}

.footer-link:hover {
  opacity: 1;
}

@media (max-width: 768px) {
  .footer-content {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .footer-links {
    flex-direction: column;
    gap: 0.5rem;
  }
}
</style> 