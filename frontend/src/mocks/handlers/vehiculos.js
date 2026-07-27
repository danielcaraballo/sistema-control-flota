import { http, HttpResponse } from 'msw'
import vehiculosData from '../data/vehiculos'

let vehiculos = [...vehiculosData]
let nextId = 100

function paginate(items, limit, offset) {
  const sliced = items.slice(offset, offset + limit)
  return {
    items: sliced,
    count: items.length,
  }
}

function parseQuery(url) {
  const params = {}
  const searchParams = new URL(url).searchParams
  for (const [key, value] of searchParams.entries()) {
    params[key] = value
  }
  return params
}

function filterVehiculos(params) {
  let result = [...vehiculos]

  if (params.incluir_inactivos !== 'true') {
    result = result.filter((v) => v.estatus_activo === true)
  }

  if (params.search) {
    const q = params.search.toLowerCase()
    result = result.filter(
      (v) =>
        v.numero_economico.toLowerCase().includes(q) ||
        v.placa?.toLowerCase().includes(q) ||
        v.vin.toLowerCase().includes(q) ||
        v.placa_intt.toLowerCase().includes(q),
    )
  }

  if (params.estado_id) {
    result = result.filter((v) => v.estado === Number(params.estado_id))
  }

  if (params.estatus_id) {
    result = result.filter((v) => v.estatus === Number(params.estatus_id))
  }

  if (params.gerencia_id) {
    result = result.filter((v) => v.gerencia === Number(params.gerencia_id))
  }

  if (params.sort_by) {
    const field = params.sort_by
    const order = params.sort_order === 'desc' ? -1 : 1
    result.sort((a, b) => {
      const aVal = a[field] ?? ''
      const bVal = b[field] ?? ''
      if (typeof aVal === 'string') {
        return aVal.localeCompare(bVal) * order
      }
      return (aVal - bVal) * order
    })
  }

  return result
}

export const vehiculosHandlers = [
  http.get('/api/vehiculos/exportar', ({ request }) => {
    const params = parseQuery(request.url)
    const filtered = filterVehiculos(params)
    const formato = params.formato || 'csv'
    const csvHeader = 'ID,Nro Económico,Placa,VIN,Marca,Modelo,Estado,Estatus'
    const csvRows = filtered.map(
      (v) =>
        `${v.id},${v.numero_economico},${v.placa},${v.vin},${v.marca_nombre},${v.modelo_nombre},${v.estado_nombre},${v.estatus_nombre}`,
    )
    const content = [csvHeader, ...csvRows].join('\n')
    const mimeType =
      formato === 'xlsx'
        ? 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        : 'text/csv'
    return HttpResponse.arrayBuffer(new TextEncoder().encode(content).buffer, {
      headers: {
        'Content-Type': mimeType,
        'Content-Disposition': `attachment; filename=vehiculos.${formato}`,
      },
    })
  }),

  http.get('/api/vehiculos/', ({ request }) => {
    const params = parseQuery(request.url)
    const filtered = filterVehiculos(params)
    const limit = params.limit ? Number(params.limit) : 50
    const offset = params.offset ? Number(params.offset) : 0
    const result = paginate(filtered, limit, offset)

    const items = result.items.map(({ codigo_qr: _qr, ...rest }) => rest)
    return HttpResponse.json({ items, count: result.count })
  }),

  http.get('/api/vehiculos/:id', ({ params }) => {
    const id = Number(params.id)
    const vehiculo = vehiculos.find((v) => v.id === id)
    if (!vehiculo) {
      return HttpResponse.json({ detail: 'No encontrado' }, { status: 404 })
    }
    return HttpResponse.json({
      ...vehiculo,
      codigo_qr:
        'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAC0lEQVQI12NgAAIABQABNjN9GQAAAAlwSFlzAAAWJQAAFiUBSVIk8AAAAA0lEQVQI12P4z8BQDwAEgAF/QualHwAAAABJRU5ErkJggg==',
    })
  }),

  http.post('/api/vehiculos/', async ({ request }) => {
    const body = await request.json()
    const newVehiculo = {
      id: nextId++,
      ...body,
      estatus_activo: true,
      porcentaje_completado: 50,
      codigo_qr: null,
      gerencia_nombre: '',
      categoria_nombre: '',
      marca_nombre: '',
      modelo_nombre: '',
      estado_nombre: '',
      emplazamiento_nombre: '',
      estatus_nombre: '',
      color_nombre: body.color ? '' : null,
      color_placa_nombre: body.color_placa ? '' : null,
      tipo_uso_nombre: body.tipo_uso ? '' : null,
      clase_nombre: '',
      tipo_combustible_nombre: '',
      unidad_usuaria_nombre: null,
    }
    vehiculos.push(newVehiculo)
    return HttpResponse.json(newVehiculo, { status: 201 })
  }),

  http.put('/api/vehiculos/:id', async ({ params, request }) => {
    const id = Number(params.id)
    const idx = vehiculos.findIndex((v) => v.id === id)
    if (idx === -1) {
      return HttpResponse.json({ detail: 'No encontrado' }, { status: 404 })
    }
    const body = await request.json()
    vehiculos[idx] = { ...vehiculos[idx], ...body }
    return HttpResponse.json(vehiculos[idx])
  }),

  http.delete('/api/vehiculos/:id', ({ params }) => {
    const id = Number(params.id)
    const idx = vehiculos.findIndex((v) => v.id === id)
    if (idx === -1) {
      return HttpResponse.json({ detail: 'No encontrado' }, { status: 404 })
    }
    vehiculos[idx] = { ...vehiculos[idx], estatus_activo: false }
    return HttpResponse.json({ detail: 'Vehículo desactivado' })
  }),

  http.post('/api/vehiculos/:id/regenerar-qr', ({ params }) => {
    const id = Number(params.id)
    const vehiculo = vehiculos.find((v) => v.id === id)
    if (!vehiculo) {
      return HttpResponse.json({ detail: 'No encontrado' }, { status: 404 })
    }
    return HttpResponse.json({
      ...vehiculo,
      codigo_qr:
        'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAC0lEQVQI12NgAAIABQABNjN9GQAAAAlwSFlzAAAWJQAAFiUBSVIk8AAAAA0lEQVQI12P4z8BQDwAEgAF/QualHwAAAABJRU5ErkJggg==',
    })
  }),
]
