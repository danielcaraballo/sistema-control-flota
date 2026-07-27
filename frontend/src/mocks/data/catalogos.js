export const marcas = [
  { id: 1, nombre: 'Toyota', estatus_activo: true },
  { id: 2, nombre: 'Ford', estatus_activo: true },
  { id: 3, nombre: 'Chevrolet', estatus_activo: true },
  { id: 4, nombre: 'Hyundai', estatus_activo: true },
  { id: 5, nombre: 'Mitsubishi', estatus_activo: true },
]

export const modelos = [
  { id: 1, nombre: 'Corolla', estatus_activo: true, marca: 1, marca_nombre: 'Toyota' },
  { id: 2, nombre: 'Fortuner', estatus_activo: true, marca: 1, marca_nombre: 'Toyota' },
  { id: 3, nombre: 'Ranger', estatus_activo: true, marca: 2, marca_nombre: 'Ford' },
  { id: 4, nombre: 'Explorer', estatus_activo: true, marca: 2, marca_nombre: 'Ford' },
  { id: 5, nombre: 'Silverado', estatus_activo: true, marca: 3, marca_nombre: 'Chevrolet' },
  { id: 6, nombre: 'Tucson', estatus_activo: true, marca: 4, marca_nombre: 'Hyundai' },
  { id: 7, nombre: 'L200', estatus_activo: true, marca: 5, marca_nombre: 'Mitsubishi' },
]

export const tiposVehiculo = [
  { id: 1, nombre: 'Automóvil', estatus_activo: true },
  { id: 2, nombre: 'Camioneta', estatus_activo: true },
  { id: 3, nombre: 'Camión', estatus_activo: true },
  { id: 4, nombre: 'Moto', estatus_activo: true },
]

export const tiposUso = [
  { id: 1, nombre: 'Administrativo', estatus_activo: true },
  { id: 2, nombre: 'Operativo', estatus_activo: true },
  { id: 3, nombre: 'Especial', estatus_activo: true },
]

export const colores = [
  { id: 1, nombre: 'Blanco', estatus_activo: true },
  { id: 2, nombre: 'Negro', estatus_activo: true },
  { id: 3, nombre: 'Rojo', estatus_activo: true },
  { id: 4, nombre: 'Azul', estatus_activo: true },
  { id: 5, nombre: 'Plateado', estatus_activo: true },
]

export const coloresPlaca = [
  { id: 1, nombre: 'Blanco', estatus_activo: true },
  { id: 2, nombre: 'Amarillo', estatus_activo: true },
  { id: 3, nombre: 'Azul', estatus_activo: true },
  { id: 4, nombre: 'Rojo', estatus_activo: true },
]

export const sistemasAfectados = [
  { id: 1, nombre: 'Motor', estatus_activo: true },
  { id: 2, nombre: 'Transmisión', estatus_activo: true },
  { id: 3, nombre: 'Suspensión', estatus_activo: true },
  { id: 4, nombre: 'Sistema Eléctrico', estatus_activo: true },
  { id: 5, nombre: 'Frenos', estatus_activo: true },
]

export const tiposFalla = [
  {
    id: 1,
    descripcion: 'Sobrecalentamiento',
    estatus_activo: true,
    sistema_afectado: 1,
    sistema_afectado_nombre: 'Motor',
  },
  {
    id: 2,
    descripcion: 'Ruido extraño en motor',
    estatus_activo: true,
    sistema_afectado: 1,
    sistema_afectado_nombre: 'Motor',
  },
  {
    id: 3,
    descripcion: 'No enciende',
    estatus_activo: true,
    sistema_afectado: 1,
    sistema_afectado_nombre: 'Motor',
  },
  {
    id: 4,
    descripcion: 'Fuga de aceite',
    estatus_activo: true,
    sistema_afectado: 1,
    sistema_afectado_nombre: 'Motor',
  },
  {
    id: 5,
    descripcion: 'Caja no engrana',
    estatus_activo: true,
    sistema_afectado: 2,
    sistema_afectado_nombre: 'Transmisión',
  },
  {
    id: 6,
    descripcion: 'Batería descargada',
    estatus_activo: true,
    sistema_afectado: 4,
    sistema_afectado_nombre: 'Sistema Eléctrico',
  },
]

export const estatusVehiculo = [
  { id: 1, nombre: 'Operativo', estatus_activo: true },
  { id: 2, nombre: 'En taller', estatus_activo: true },
  { id: 3, nombre: 'Inactivo', estatus_activo: true },
  { id: 4, nombre: 'Asignado', estatus_activo: true },
]

export const clasesVehiculo = [
  { id: 1, nombre: 'Sedán', estatus_activo: true },
  { id: 2, nombre: 'SUV', estatus_activo: true },
  { id: 3, nombre: 'Pickup', estatus_activo: true },
  { id: 4, nombre: 'Carga', estatus_activo: true },
]

export const tiposCombustible = [
  { id: 1, nombre: 'Gasolina', estatus_activo: true },
  { id: 2, nombre: 'Diesel', estatus_activo: true },
  { id: 3, nombre: 'Gas', estatus_activo: true },
]

export const allCatalogData = {
  marcas,
  modelos,
  'tipos-vehiculo': tiposVehiculo,
  'tipos-uso': tiposUso,
  colores,
  'colores-placa': coloresPlaca,
  'sistemas-afectados': sistemasAfectados,
  'tipos-falla': tiposFalla,
  'estatus-vehiculo': estatusVehiculo,
  'clases-vehiculo': clasesVehiculo,
  'tipos-combustible': tiposCombustible,
}
