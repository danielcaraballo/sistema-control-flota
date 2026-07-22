import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ROL_NACIONAL } from '@/utils/roles'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'

NProgress.configure({ showSpinner: false })

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
          meta: { rolMinimo: ROL_NACIONAL },
        },
      ],
    },
  ],
})

router.beforeEach(async (to, _from) => {
  NProgress.start()
  const auth = useAuthStore()

  if (auth.loading) {
    await auth.initialized
  }

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

router.afterEach(() => {
  NProgress.done()
})

router.onError(() => {
  NProgress.done()
})

export default router
