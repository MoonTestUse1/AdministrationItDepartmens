import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import LoginView from '../views/LoginView.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'login',
      component: LoginView
    },
    {
      path: '/support',
      name: 'support',
      // Ошибка: Не найден модуль '../views/SupportView.vue'
      component: () => import('../views/SupportView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/admin',
      name: 'admin-login',
      // Ошибка: Не найден модуль '../views/admin/AdminLoginView.vue'
      component: () => import('../views/admin/AdminLoginView.vue')
    },
    {
      path: '/admin/dashboard',
      name: 'admin-dashboard',
      // Ошибка: Не найден модуль '../views/admin/DashboardView.vue'
      component: () => import('../views/admin/DashboardView.vue'),
      meta: { requiresAdmin: true }
    }
  ]
});

router.beforeEach((to, _, next) => {
  const authStore = useAuthStore();

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login' });
  } else if (to.meta.requiresAdmin && !authStore.isAdmin) {
    next({ name: 'admin-login' });
  } else {
    next();
  }
});

export default router;