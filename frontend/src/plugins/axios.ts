import axios, { InternalAxiosRequestConfig } from 'axios'

const axiosInstance = axios.create({
  baseURL: '/api',
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Добавляем перехватчик для добавления токена
axiosInstance.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Добавляем перехватчик для обработки ошибок
axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/admin/login'
    }
    return Promise.reject(error)
  }
)

export default axiosInstance
