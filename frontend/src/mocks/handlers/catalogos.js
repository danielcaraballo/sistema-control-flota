import { http, HttpResponse } from 'msw'
import { allCatalogData } from '../data/catalogos'

const mutableData = {}
for (const key of Object.keys(allCatalogData)) {
  mutableData[key] = allCatalogData[key].map((item) => ({ ...item }))
}

let nextIds = {}
for (const key of Object.keys(mutableData)) {
  const maxId = mutableData[key].reduce((max, item) => Math.max(max, item.id), 0)
  nextIds[key] = maxId + 100
}

function parseQuery(url) {
  const params = {}
  for (const [key, value] of new URL(url).searchParams.entries()) {
    params[key] = value
  }
  return params
}

function respond(collection, incluirInactivos) {
  let data = mutableData[collection]
  if (!incluirInactivos) {
    data = data.filter((item) => item.estatus_activo !== false)
  }
  return HttpResponse.json(data)
}

export const catalogosHandlers = [
  http.get('/api/catalogos/:entity/', ({ request, params }) => {
    const collection = params.entity
    if (!mutableData[collection]) {
      return HttpResponse.json({ detail: 'No encontrado' }, { status: 404 })
    }
    const query = parseQuery(request.url)
    return respond(collection, query.incluir_inactivos === 'true')
  }),

  http.post('/api/catalogos/:entity/', async ({ params, request }) => {
    const collection = params.entity
    if (!mutableData[collection]) {
      return HttpResponse.json({ detail: 'No encontrado' }, { status: 404 })
    }
    const body = await request.json()
    const newItem = {
      id: nextIds[collection]++,
      nombre: body.nombre || body.descripcion || '',
      estatus_activo: true,
      ...body,
    }
    mutableData[collection].push(newItem)
    return HttpResponse.json(newItem, { status: 201 })
  }),

  http.put('/api/catalogos/:entity/:id', async ({ params, request }) => {
    const collection = params.entity
    if (!mutableData[collection]) {
      return HttpResponse.json({ detail: 'No encontrado' }, { status: 404 })
    }
    const id = Number(params.id)
    const idx = mutableData[collection].findIndex((item) => item.id === id)
    if (idx === -1) {
      return HttpResponse.json({ detail: 'No encontrado' }, { status: 404 })
    }
    const body = await request.json()
    mutableData[collection][idx] = { ...mutableData[collection][idx], ...body }
    return HttpResponse.json(mutableData[collection][idx])
  }),

  http.delete('/api/catalogos/:entity/:id', ({ params }) => {
    const collection = params.entity
    if (!mutableData[collection]) {
      return HttpResponse.json({ detail: 'No encontrado' }, { status: 404 })
    }
    const id = Number(params.id)
    const idx = mutableData[collection].findIndex((item) => item.id === id)
    if (idx === -1) {
      return HttpResponse.json({ detail: 'No encontrado' }, { status: 404 })
    }
    mutableData[collection][idx] = { ...mutableData[collection][idx], estatus_activo: false }
    return HttpResponse.json({ detail: 'Item desactivado' })
  }),
]
