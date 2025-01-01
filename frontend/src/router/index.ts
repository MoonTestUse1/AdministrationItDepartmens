import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const router = createRouter({
  history: createWebHistory(),
  routes: [
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
    }
  ]
});

router.beforeEach((to, _, next) => {
  const authStore = useAuthStore();

  if (to.meta.requiresAdmin && !authStore.isAdmin) {
    next({ name: 'AdminLogin' });
  } else {
    next();
  }
});

export default router;