export function placaSeverity(nombre) {
  const map = {
    Azul: 'info',
    Naranja: 'warn',
  }
  return map[nombre] || 'info'
}

export function estatusSeverity(nombre) {
  const map = {
    Operativo: 'success',
    'En reparacion': 'info',
    Inoperativo: 'danger',
  }
  return map[nombre] || 'info'
}
