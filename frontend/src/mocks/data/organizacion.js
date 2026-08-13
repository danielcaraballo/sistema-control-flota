export const estados = [
  { id: 1, nombre: 'Región Norte', estatus_activo: true },
  { id: 2, nombre: 'Región Sur', estatus_activo: true },
  { id: 3, nombre: 'Región Este', estatus_activo: true },
  { id: 4, nombre: 'Región Oeste', estatus_activo: true },
  { id: 5, nombre: 'Región Central', estatus_activo: true },
]

export const gerencias = [
  { id: 1, nombre: 'Gerencia General', estatus_activo: true },
  { id: 2, nombre: 'Gerencia de Operaciones', estatus_activo: true },
  { id: 3, nombre: 'Gerencia de Logística', estatus_activo: true },
  { id: 4, nombre: 'Gerencia de Mantenimiento', estatus_activo: true },
]

export const centrosServicio = [
  {
    id: 1,
    nombre: 'Centro Norte - Principal',
    estatus_activo: true,
    estado: 1,
    estado_nombre: 'Región Norte',
  },
  {
    id: 2,
    nombre: 'Centro Norte - Secundario',
    estatus_activo: true,
    estado: 1,
    estado_nombre: 'Región Norte',
  },
  {
    id: 3,
    nombre: 'Centro Sur - Principal',
    estatus_activo: true,
    estado: 2,
    estado_nombre: 'Región Sur',
  },
  {
    id: 4,
    nombre: 'Centro Sur - Secundario',
    estatus_activo: true,
    estado: 2,
    estado_nombre: 'Región Sur',
  },
  {
    id: 5,
    nombre: 'Centro Este - Principal',
    estatus_activo: true,
    estado: 3,
    estado_nombre: 'Región Este',
  },
  {
    id: 6,
    nombre: 'Centro Oeste - Principal',
    estatus_activo: true,
    estado: 4,
    estado_nombre: 'Región Oeste',
  },
  {
    id: 7,
    nombre: 'Centro Central - Principal',
    estatus_activo: true,
    estado: 5,
    estado_nombre: 'Región Central',
  },
]
