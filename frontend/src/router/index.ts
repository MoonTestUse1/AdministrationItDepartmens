import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/admin',
      component: () => import('@/layouts/AdminLayout.vue'),
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

export default router;