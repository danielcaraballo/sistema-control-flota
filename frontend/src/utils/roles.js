export const ROLES = [
  { label: 'Gerente Nacional', value: 'gerente_nacional' },
  { label: 'Analista Nacional', value: 'analista_nacional' },
  { label: 'Responsable Estatal', value: 'responsable_estatal' },
  { label: 'Mecánico', value: 'mecanico' },
]

export const ESTATAL_ROLES = ['responsable_estatal', 'mecanico']

export function rolLabel(rol) {
  return (
    {
      gerente_nacional: 'Gerente Nacional',
      analista_nacional: 'Analista Nacional',
      responsable_estatal: 'Responsable Estatal',
      mecanico: 'Mecánico',
    }[rol] || rol
  )
}

export function rolSeverity(rol) {
  return (
    {
      gerente_nacional: 'danger',
      analista_nacional: 'warn',
      responsable_estatal: 'info',
      mecanico: 'success',
    }[rol] || 'info'
  )
}
