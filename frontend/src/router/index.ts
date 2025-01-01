import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomeView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue')
    },
    {
      path: '/admin',
      name: 'admin-login',
      component: () => import('@/views/AdminLoginView.vue')
    },
    {
      path: '/requests',
      name: 'requests',
      component: () => import('@/views/RequestsView.vue'),
      meta: { requiresAuth: true }
    }
  ]
});

router.beforeEach((to, from, next) => {
  console.log('Проверка маршрута:', to.path)
  
  if (to.meta.requiresAuth) {
    console.log('Маршрут требует авторизации')
    const token = localStorage.getItem('token')
    console.log('Токен:', token ? 'Присутствует' : 'Отсутствует')
    
    if (!token) {
      console.log('Перенаправление на /login')
      next('/login')
      return
    }
  }
  
  console.log('Разрешаем переход')
  next()
})

export default router