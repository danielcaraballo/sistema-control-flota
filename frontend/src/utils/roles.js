export const ROL_MECANICO = 'mecanico'
export const ROL_ANALISTA = 'analista'
export const ROL_ESTATAL = 'estatal'
export const ROL_NACIONAL = 'nacional'

const JERARQUIA = [ROL_MECANICO, ROL_ANALISTA, ROL_ESTATAL, ROL_NACIONAL]

export const ROLES = [
  { label: 'Nacional', value: ROL_NACIONAL, estatal: false },
  { label: 'Estatal', value: ROL_ESTATAL, estatal: true },
  { label: 'Analista', value: ROL_ANALISTA, estatal: true },
  { label: 'Mecánico', value: ROL_MECANICO, estatal: true },
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
