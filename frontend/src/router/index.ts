import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: () => import('@/layouts/MainLayout.vue'),
      children: [
        {
          path: '',
          name: 'Home',
          component: () => import('@/views/HomeView.vue')
        },
        {
          path: 'login',
          name: 'Login',
          component: () => import('@/views/LoginView.vue')
        }
      ]
    },
    {
      path: '/admin',
      component: () => import('@/layouts/AdminLayout.vue'),
      meta: { requiresAdmin: true },
      children: [
        {
          path: '',
          redirect: '/admin/dashboard'
        },
        {
          path: 'dashboard',
          name: 'AdminDashboard',
          component: () => import('@/views/admin/DashboardView.vue')
        },
        {
          path: 'requests',
          name: 'AdminRequests',
          component: () => import('@/views/admin/RequestsView.vue')
        },
        {
          path: 'employees',
          name: 'AdminEmployees',
          component: () => import('@/views/admin/EmployeesView.vue')
        },
        {
          path: 'employees/add',
          name: 'AdminEmployeeAdd',
          component: () => import('@/views/admin/AddEmployeeView.vue')
        }
      ]
    },
    {
      path: '/admin/login',
      name: 'AdminLogin',
      component: () => import('@/views/admin/AdminLoginView.vue')
    },
    {
      path: '/requests',
      name: 'requests',
      component: () => import('@/views/RequestsView.vue'),
      meta: { requiresAuth: true }
    }
  ]
});

router.beforeEach((to, _, next) => {
  const authStore = useAuthStore();

  if (to.meta.requiresAdmin && !authStore.isAdmin) {
    next({ name: 'AdminLogin' });
  } else if (to.meta.requiresAuth) {
    const token = localStorage.getItem('token');
    if (!token) {
      next('/login');
      return;
    }
  } else {
    next();
  }
});

export default router;