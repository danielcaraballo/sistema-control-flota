export const demoUser = {
  id: 1,
  username: 'demo',
  email: 'demo@demo.flota',
  first_name: 'Usuario',
  last_name: 'Demo',
  rol: 'nacional',
  is_active: true,
  estado: null,
  estado_nombre: null,
}

export const demoUsers = [
  demoUser,
  {
    id: 2,
    username: 'analista.demo',
    email: 'analista@demo.flota',
    first_name: 'Analista',
    last_name: 'Demo',
    rol: 'analista',
    is_active: true,
    estado: 1,
    estado_nombre: 'Región Norte',
  },
  {
    id: 3,
    username: 'mecanico.demo',
    email: 'mecanico@demo.flota',
    first_name: 'Mecánico',
    last_name: 'Demo',
    rol: 'mecanico',
    is_active: true,
    estado: 2,
    estado_nombre: 'Región Sur',
  },
]
