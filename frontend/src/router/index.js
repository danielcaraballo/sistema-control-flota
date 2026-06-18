import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: { layout: 'auth' },
    },
    {
      path: '/',
      component: () => import('../layouts/DefaultLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          name: 'dashboard',
          component: () => import('../views/DashboardView.vue'),
        },
        {
          path: 'usuarios',
          name: 'usuarios',
          component: () => import('../views/UsuariosView.vue'),
          meta: { roles: ['gerente_nacional'] },
        },
        {
          path: 'vehiculos',
          name: 'vehiculos',
          component: () => import('../views/VehiculosView.vue'),
        },
        {
          path: 'taller',
          name: 'taller',
          component: () => import('../views/TallerView.vue'),
        },
        {
          path: 'reportes',
          name: 'reportes',
          component: () => import('../views/ReportesView.vue'),
        },
      ],
    },
  ],
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')

  if (to.name === 'login' && token) {
    return next({ name: 'dashboard' })
  }

  if (to.meta.requiresAuth && !token) {
    return next({ name: 'login' })
  }

  next()
})

export default router
