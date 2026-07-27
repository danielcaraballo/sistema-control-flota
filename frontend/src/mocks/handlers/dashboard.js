import { http, HttpResponse } from 'msw'
import vehiculos from '../data/vehiculos'

const estatusMap = {
  1: { id: 1, nombre: 'Operativo' },
  2: { id: 2, nombre: 'En taller' },
  3: { id: 3, nombre: 'Inactivo' },
  4: { id: 4, nombre: 'Asignado' },
}

function getKpis() {
  const active = vehiculos.filter((v) => v.estatus_activo)
  const total = active.length
  const operativos = active.filter((v) => v.estatus === 1).length
  const inactivos = total - operativos
  const completitud = Math.round(
    active.reduce((sum, v) => sum + (v.porcentaje_completado || 0), 0) / (total || 1),
  )

  const estatusCounts = {}
  for (const v of active) {
    const key = v.estatus
    estatusCounts[key] = (estatusCounts[key] || 0) + 1
  }
  const estatus = Object.entries(estatusCounts)
    .map(([id, cantidad]) => ({
      id: Number(id),
      nombre: estatusMap[id]?.nombre || 'Desconocido',
      cantidad,
    }))
    .sort((a, b) => b.cantidad - a.cantidad)

  return {
    total_vehiculos: total,
    porcentaje_operatividad: total > 0 ? Math.round((operativos / total) * 1000) / 10 : 0,
    operativos,
    inactivos,
    completitud_promedio: completitud,
    estatus,
  }
}

function getNacional() {
  const active = vehiculos.filter((v) => v.estatus_activo)
  const estadoMap = {}
  for (const v of active) {
    if (!estadoMap[v.estado_nombre]) {
      estadoMap[v.estado_nombre] = { total: 0, activos: 0, estatus: {} }
    }
    estadoMap[v.estado_nombre].total++
    if (v.estatus === 1) estadoMap[v.estado_nombre].activos++
    const key = v.estatus
    estadoMap[v.estado_nombre].estatus[key] = (estadoMap[v.estado_nombre].estatus[key] || 0) + 1
  }

  const resumenEstados = Object.entries(estadoMap).map(([nombre, data]) => ({
    estado_nombre: nombre,
    total: data.total,
    operatividad: data.total > 0 ? Math.round((data.activos / data.total) * 1000) / 10 : 0,
    activos: data.activos,
    inactivos: data.total - data.activos,
    estatus: Object.entries(data.estatus).map(([id, cantidad]) => ({
      id: Number(id),
      nombre: estatusMap[id]?.nombre || 'Desconocido',
      cantidad,
    })),
  }))

  let mejor = null
  let peor = null
  for (const est of resumenEstados) {
    if (!mejor || est.operatividad > mejor.operatividad) mejor = est
    if (!peor || est.operatividad < peor.operatividad) peor = est
  }

  return {
    resumen_estados: resumenEstados,
    total_vehiculos: active.length,
    total_estados_con_vehiculos: resumenEstados.length,
    mejor_operatividad: mejor,
    peor_operatividad: peor,
  }
}

export const dashboardHandlers = [
  http.get('/api/dashboard/kpis', () => {
    return HttpResponse.json(getKpis())
  }),

  http.get('/api/dashboard/nacional', () => {
    return HttpResponse.json(getNacional())
  }),
]
