import { http, HttpResponse } from 'msw'
import { demoUsers } from '../data/usuarios'

let users = [...demoUsers]
let nextId = 10

export const usuariosHandlers = [
  http.get('/api/usuarios/', () => {
    return HttpResponse.json(users.filter((u) => u.is_active !== false))
  }),

  http.post('/api/usuarios/', async ({ request }) => {
    const body = await request.json()
    const id = nextId++
    const newUser = {
      id,
      username: body.username || `usuario_${id}`,
      email: body.email,
      first_name: body.first_name || '',
      last_name: body.last_name || '',
      rol: body.rol,
      is_active: true,
      estado: body.estado_id || null,
      estado_nombre: null,
    }
    users.push(newUser)
    return HttpResponse.json({ user: newUser, password: 'Temp1234' }, { status: 201 })
  }),

  http.get('/api/usuarios/:id', ({ params }) => {
    const id = Number(params.id)
    const user = users.find((u) => u.id === id)
    if (!user) {
      return HttpResponse.json({ detail: 'No encontrado' }, { status: 404 })
    }
    return HttpResponse.json(user)
  }),

  http.put('/api/usuarios/:id', async ({ params, request }) => {
    const id = Number(params.id)
    const idx = users.findIndex((u) => u.id === id)
    if (idx === -1) {
      return HttpResponse.json({ detail: 'No encontrado' }, { status: 404 })
    }
    const body = await request.json()
    if (body.is_active !== undefined) {
      users[idx] = { ...users[idx], is_active: body.is_active }
    } else {
      users[idx] = {
        ...users[idx],
        email: body.email ?? users[idx].email,
        first_name: body.first_name ?? users[idx].first_name,
        last_name: body.last_name ?? users[idx].last_name,
        rol: body.rol ?? users[idx].rol,
        estado: body.estado_id ?? users[idx].estado,
      }
    }
    return HttpResponse.json(users[idx])
  }),

  http.delete('/api/usuarios/:id', ({ params }) => {
    const id = Number(params.id)
    const idx = users.findIndex((u) => u.id === id)
    if (idx === -1) {
      return HttpResponse.json({ detail: 'No encontrado' }, { status: 404 })
    }
    users[idx] = { ...users[idx], is_active: false }
    return HttpResponse.json({ detail: 'Usuario desactivado' })
  }),

  http.post('/api/usuarios/:id/reset-password', ({ params }) => {
    const id = Number(params.id)
    const user = users.find((u) => u.id === id)
    if (!user) {
      return HttpResponse.json({ detail: 'No encontrado' }, { status: 404 })
    }
    return HttpResponse.json({ password: 'NuevaPass123' })
  }),
]
