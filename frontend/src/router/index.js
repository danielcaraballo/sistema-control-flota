import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ROL_NACIONAL, ROL_ANALISTA } from '@/utils/roles'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
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
          meta: { rolMinimo: ROL_NACIONAL },
        },
        {
          path: 'vehiculos',
          name: 'vehiculos',
          component: () => import('../views/VehiculosView.vue'),
        },
        {
          path: 'vehiculos/:id',
          name: 'vehiculo-detalle',
          component: () => import('../views/VehiculoDetalleView.vue'),
        },
        {
          path: 'catalogos',
          name: 'catalogos',
          component: () => import('../views/CatalogosView.vue'),
          meta: { rolMinimo: ROL_NACIONAL },
        },
        {
          path: 'organizacion',
          name: 'organizacion',
          component: () => import('../views/OrganizacionView.vue'),
          meta: { rolMinimo: ROL_NACIONAL },
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
          meta: { rolMinimo: ROL_ANALISTA },
        },
      ],
    },
  ],
})

router.beforeEach((to, _from) => {
  const auth = useAuthStore()

  if (auth.loading) return

  if (to.name === 'login' && auth.isAuthenticated) {
    return { name: 'dashboard' }
  }

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  if (to.meta.rolMinimo && !auth.tieneRol(to.meta.rolMinimo)) {
    return { name: 'dashboard' }
  }
})

export default router
