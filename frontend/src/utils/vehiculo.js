export function placaSeverity(nombre) {
  const map = {
    Amarilla: 'warn',
    Verde: 'success',
    Azul: 'info',
    Blanca: 'secondary',
    Roja: 'danger',
    Plateada: 'contrast',
  }
  return map[nombre] || 'info'
}

export function estatusSeverity(nombre) {
  const map = {
    Operativo: 'success',
    'En taller': 'warn',
    'Fuera de servicio': 'danger',
  }
  return map[nombre] || 'info'
}
