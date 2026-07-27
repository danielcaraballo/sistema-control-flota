import { http, HttpResponse } from 'msw'
import { estados, gerencias, centrosServicio } from '../data/organizacion'

const mutableEstados = estados.map((e) => ({ ...e }))
const mutableGerencias = gerencias.map((g) => ({ ...g }))
const mutableCentros = centrosServicio.map((c) => ({ ...c }))

let nextIdEstado = 100
let nextIdGerencia = 100
let nextIdCentro = 100

function parseQuery(url) {
  const params = {}
  for (const [key, value] of new URL(url).searchParams.entries()) {
    params[key] = value
  }
  return params
}

function filterActive(arr, incluirInactivos) {
  if (incluirInactivos) return arr
  return arr.filter((item) => item.estatus_activo !== false)
}

export const organizacionHandlers = [
  http.get('/api/organizacion/estados/', ({ request }) => {
    const query = parseQuery(request.url)
    return HttpResponse.json(filterActive(mutableEstados, query.incluir_inactivos === 'true'))
  }),

  http.post('/api/organizacion/estados/', async ({ request }) => {
    const body = await request.json()
    const item = { id: nextIdEstado++, nombre: body.nombre, estatus_activo: true }
    mutableEstados.push(item)
    return HttpResponse.json(item, { status: 201 })
  }),

  http.put('/api/organizacion/estados/:id', async ({ params, request }) => {
    const id = Number(params.id)
    const idx = mutableEstados.findIndex((e) => e.id === id)
    if (idx === -1) return HttpResponse.json({ detail: 'No encontrado' }, { status: 404 })
    const body = await request.json()
    mutableEstados[idx] = { ...mutableEstados[idx], ...body }
    return HttpResponse.json(mutableEstados[idx])
  }),

  http.delete('/api/organizacion/estados/:id', ({ params }) => {
    const id = Number(params.id)
    const idx = mutableEstados.findIndex((e) => e.id === id)
    if (idx === -1) return HttpResponse.json({ detail: 'No encontrado' }, { status: 404 })
    mutableEstados[idx].estatus_activo = false
    return HttpResponse.json({ detail: 'Estado desactivado' })
  }),

  http.get('/api/organizacion/gerencias/', ({ request }) => {
    const query = parseQuery(request.url)
    return HttpResponse.json(filterActive(mutableGerencias, query.incluir_inactivos === 'true'))
  }),

  http.post('/api/organizacion/gerencias/', async ({ request }) => {
    const body = await request.json()
    const item = { id: nextIdGerencia++, nombre: body.nombre, estatus_activo: true }
    mutableGerencias.push(item)
    return HttpResponse.json(item, { status: 201 })
  }),

  http.put('/api/organizacion/gerencias/:id', async ({ params, request }) => {
    const id = Number(params.id)
    const idx = mutableGerencias.findIndex((g) => g.id === id)
    if (idx === -1) return HttpResponse.json({ detail: 'No encontrado' }, { status: 404 })
    const body = await request.json()
    mutableGerencias[idx] = { ...mutableGerencias[idx], ...body }
    return HttpResponse.json(mutableGerencias[idx])
  }),

  http.delete('/api/organizacion/gerencias/:id', ({ params }) => {
    const id = Number(params.id)
    const idx = mutableGerencias.findIndex((g) => g.id === id)
    if (idx === -1) return HttpResponse.json({ detail: 'No encontrado' }, { status: 404 })
    mutableGerencias[idx].estatus_activo = false
    return HttpResponse.json({ detail: 'Gerencia desactivada' })
  }),

  http.get('/api/organizacion/centros-servicio/', ({ request }) => {
    const query = parseQuery(request.url)
    return HttpResponse.json(filterActive(mutableCentros, query.incluir_inactivos === 'true'))
  }),

  http.post('/api/organizacion/centros-servicio/', async ({ request }) => {
    const body = await request.json()
    const item = {
      id: nextIdCentro++,
      nombre: body.nombre,
      estatus_activo: true,
      estado: body.estado,
      estado_nombre: '',
    }
    mutableCentros.push(item)
    return HttpResponse.json(item, { status: 201 })
  }),

  http.put('/api/organizacion/centros-servicio/:id', async ({ params, request }) => {
    const id = Number(params.id)
    const idx = mutableCentros.findIndex((c) => c.id === id)
    if (idx === -1) return HttpResponse.json({ detail: 'No encontrado' }, { status: 404 })
    const body = await request.json()
    mutableCentros[idx] = { ...mutableCentros[idx], ...body }
    return HttpResponse.json(mutableCentros[idx])
  }),

  http.delete('/api/organizacion/centros-servicio/:id', ({ params }) => {
    const id = Number(params.id)
    const idx = mutableCentros.findIndex((c) => c.id === id)
    if (idx === -1) return HttpResponse.json({ detail: 'No encontrado' }, { status: 404 })
    mutableCentros[idx].estatus_activo = false
    return HttpResponse.json({ detail: 'Centro desactivado' })
  }),
]
