const JERARQUIA = ['mecanico', 'analista', 'estatal', 'nacional']

export const ROLES = [
  { label: 'Nacional', value: 'nacional', estatal: false },
  { label: 'Estatal', value: 'estatal', estatal: true },
  { label: 'Analista', value: 'analista', estatal: true },
  { label: 'Mecánico', value: 'mecanico', estatal: true },
]

export const ESTATAL_ROLES = ROLES.filter((r) => r.estatal).map((r) => r.value)

export function tieneRolMinimo(rol, rolMinimo) {
  return JERARQUIA.indexOf(rol) >= JERARQUIA.indexOf(rolMinimo)
}

export function esEstatal(rol) {
  return ESTATAL_ROLES.includes(rol)
}

export function rolLabel(rol) {
  const found = ROLES.find((r) => r.value === rol)
  return found?.label || rol
}

export function rolSeverity(rol) {
  return (
    {
      nacional: 'danger',
      estatal: 'warn',
      analista: 'info',
      mecanico: 'success',
    }[rol] || 'info'
  )
}
