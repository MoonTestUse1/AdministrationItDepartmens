<template>
  <div v-if="isOpen" class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2>Добавить сотрудника</h2>
        <button class="close-button" @click="closeModal">&times;</button>
      </div>

      <form @submit.prevent="handleSubmit" class="modal-form">
        <div class="form-group">
          <label for="first_name">Имя</label>
          <input
            type="text"
            id="first_name"
            v-model="formData.first_name"
            required
            class="form-input"
            placeholder="Введите имя"
          >
        </div>

        <div class="form-group">
          <label for="last_name">Фамилия</label>
          <input
            type="text"
            id="last_name"
            v-model="formData.last_name"
            required
            class="form-input"
            placeholder="Введите фамилию"
          >
        </div>

        <div class="form-group">
          <label for="password">Пароль</label>
          <input
            type="password"
            id="password"
            v-model="formData.password"
            required
            class="form-input"
            placeholder="Введите пароль"
          >
        </div>

        <div class="form-group">
          <label for="department">Отдел</label>
          <input
            type="text"
            id="department"
            v-model="formData.department"
            required
            class="form-input"
            placeholder="Введите название отдела"
          >
        </div>

        <div class="form-group">
          <label for="office">Кабинет</label>
          <input
            type="text"
            id="office"
            v-model="formData.office"
            required
            class="form-input"
            placeholder="Введите номер кабинета"
          >
        </div>

        <div class="form-actions">
          <button type="submit" class="submit-button" :disabled="isLoading">
            {{ isLoading ? 'Добавление...' : 'Добавить' }}
          </button>
          <button type="button" class="cancel-button" @click="closeModal">
            Отмена
          </button>
        </div>

        <p v-if="error" class="error-message">{{ error }}</p>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AddEmployeeModal',
  props: {
    isOpen: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      formData: {
        first_name: '',
        last_name: '',
        password: '',
        department: '',
        office: ''
      },
      error: '',
      isLoading: false
    }
  },
  methods: {
    closeModal() {
      this.$emit('close')
      this.resetForm()
    },
    resetForm() {
      this.formData = {
        first_name: '',
        last_name: '',
        password: '',
        department: '',
        office: ''
      }
      this.error = ''
    },
    async handleSubmit() {
      this.error = ''
      this.isLoading = true
      
      try {
        console.log('Sending employee data:', this.formData)
        const response = await axios.post('/api/employees', this.formData, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('admin_token')}`,
            'Content-Type': 'application/json'
          },
          validateStatus: function (status) {
            return status < 500
          }
        })

        console.log('Response:', response)

        if (response.status === 307) {
          const redirectUrl = response.headers.location
          console.log('Redirecting to:', redirectUrl)
          const finalResponse = await axios.post(redirectUrl, this.formData, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('admin_token')}`,
              'Content-Type': 'application/json'
            }
          })
          
          console.log('Final response:', finalResponse)
          
          if (finalResponse.status === 200 || finalResponse.status === 201) {
            this.$emit('employee-added')
            this.closeModal()
          } else {
            this.error = finalResponse.data?.detail || 'Ошибка при добавлении сотрудника'
          }
        } else if (response.status === 200 || response.status === 201) {
          this.$emit('employee-added')
          this.closeModal()
        } else {
          this.error = response.data?.detail || 'Ошибка при добавлении сотрудника'
        }
      } catch (error) {
        console.error('Error creating employee:', error)
        this.error = error.response?.data?.detail || 'Ошибка при добавлении сотрудника'
      } finally {
        this.isLoading = false
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
  width: 100%;
  max-width: 500px;
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

.modal-form {
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

.submit-button {
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

.submit-button:hover:not(:disabled) {
  background-color: #283593;
}

.submit-button:disabled {
  background-color: #9fa8da;
  cursor: not-allowed;
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

.error-message {
  color: #d32f2f;
  text-align: center;
  margin: 0;
  font-size: 0.9rem;
}
</style> 