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
      children: [
        {
          path: '',
          name: 'dashboard',
          component: () => import('../views/DashboardView.vue'),
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

export default router
