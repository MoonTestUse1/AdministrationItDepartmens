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
    },
    {
      path: '/admin/dashboard',
      name: 'admin-dashboard',
      component: () => import('@/views/AdminDashboardView.vue'),
      meta: { requiresAdmin: true }
    }
  ]
});

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAdmin) {
    const adminToken = localStorage.getItem('admin_token')
    if (!adminToken) {
      next('/admin')
      return
    }
  } else if (to.meta.requiresAuth) {
    const token = localStorage.getItem('token')
    if (!token) {
      next('/login')
      return
    }
  }
  next()
})

export default router