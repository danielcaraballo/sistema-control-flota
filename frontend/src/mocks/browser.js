import { setupWorker } from 'msw/browser'
import { authHandlers } from './handlers/auth'
import { vehiculosHandlers } from './handlers/vehiculos'
import { catalogosHandlers } from './handlers/catalogos'
import { organizacionHandlers } from './handlers/organizacion'
import { usuariosHandlers } from './handlers/usuarios'
import { dashboardHandlers } from './handlers/dashboard'

export const worker = setupWorker(
  ...authHandlers,
  ...vehiculosHandlers,
  ...catalogosHandlers,
  ...organizacionHandlers,
  ...usuariosHandlers,
  ...dashboardHandlers,
)
