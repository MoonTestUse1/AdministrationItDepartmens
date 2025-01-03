<template>
  <div class="admin-login">
    <div class="login-container">
      <div class="login-header">
        <h1>IT Support</h1>
        <p>Панель администратора</p>
      </div>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">Имя пользователя</label>
          <input
            type="text"
            id="username"
            v-model="username"
            required
            class="form-input"
            placeholder="Введите имя пользователя"
          >
        </div>

        <div class="form-group">
          <label for="password">Пароль</label>
          <input
            type="password"
            id="password"
            v-model="password"
            required
            class="form-input"
            placeholder="Введите пароль"
          >
        </div>

        <button type="submit" class="login-button" :disabled="isLoading">
          {{ isLoading ? 'Вход...' : 'Войти' }}
        </button>

        <p v-if="error" class="error-message">{{ error }}</p>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminLoginView',
  data() {
    return {
      username: '',
      password: '',
      error: '',
      isLoading: false
    }
  },
  methods: {
    async handleLogin() {
      this.error = ''
      this.isLoading = true
      
      try {
        const formData = new FormData()
        formData.append('username', this.username)
        formData.append('password', this.password)
        
        const response = await axios.post('/api/auth/admin/login', formData)
        
        localStorage.setItem('admin_token', response.data.access_token)
        this.$router.push('/admin/dashboard')
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка при входе'
      } finally {
        this.isLoading = false
      }
    }
  }
}
</script>

<style scoped>
.admin-login {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1a237e 0%, #3949ab 100%);
  padding: 1rem;
}

.login-container {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  width: 100%;
  max-width: 400px;
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.login-header h1 {
  color: #1a237e;
  margin: 0;
  font-size: 2rem;
  font-weight: 600;
}

.login-header p {
  color: #666;
  margin: 0.5rem 0 0;
}

.login-form {
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

.login-button {
  background-color: #1a237e;
  color: white;
  padding: 1rem;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.login-button:hover:not(:disabled) {
  background-color: #283593;
}

.login-button:disabled {
  background-color: #9fa8da;
  cursor: not-allowed;
}

.error-message {
  color: #d32f2f;
  text-align: center;
  margin: 0;
  font-size: 0.9rem;
}
</style>
