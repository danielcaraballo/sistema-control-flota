import { http, HttpResponse } from 'msw'
import { demoUser } from '../data/usuarios'
import { DEMO_ACCESS_TOKEN, DEMO_REFRESH_TOKEN } from '../constants'

export const authHandlers = [
  http.post('/api/auth/login', async ({ request }) => {
    const body = await request.json()
    if (body.username === 'demo' && body.password === 'demo123') {
      return HttpResponse.json({
        access: DEMO_ACCESS_TOKEN,
        refresh: DEMO_REFRESH_TOKEN,
        user: demoUser,
      })
    }
    return HttpResponse.json({ detail: 'Credenciales inválidas' }, { status: 401 })
  }),

  http.get('/api/auth/me', ({ request }) => {
    const auth = request.headers.get('Authorization')
    if (auth !== 'Bearer ' + DEMO_ACCESS_TOKEN) {
      return HttpResponse.json({ detail: 'No autenticado' }, { status: 401 })
    }
    return HttpResponse.json(demoUser)
  }),

  http.post('/api/auth/change-password', async ({ request }) => {
    const auth = request.headers.get('Authorization')
    if (auth !== 'Bearer ' + DEMO_ACCESS_TOKEN) {
      return HttpResponse.json({ detail: 'No autenticado' }, { status: 401 })
    }
    return HttpResponse.json({ detail: 'Contraseña cambiada exitosamente' })
  }),

  http.post('/api/auth/refresh', async ({ request }) => {
    const body = await request.json()
    if (body.refresh === DEMO_REFRESH_TOKEN) {
      return HttpResponse.json({ access: DEMO_ACCESS_TOKEN })
    }
    return HttpResponse.json({ detail: 'Token inválido' }, { status: 401 })
  }),

  http.post('/api/auth/logout', () => {
    return HttpResponse.json({ detail: 'Sesión cerrada' })
  }),
]
