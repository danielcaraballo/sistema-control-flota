export const demoUser = {
  id: 1,
  username: 'demo',
  email: 'demo@scf.gob.ve',
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
    email: 'analista@scf.gob.ve',
    first_name: 'Analista',
    last_name: 'Demo',
    rol: 'analista',
    is_active: true,
    estado: 1,
    estado_nombre: 'Distrito Capital',
  },
  {
    id: 3,
    username: 'mecanico.demo',
    email: 'mecanico@scf.gob.ve',
    first_name: 'Mecánico',
    last_name: 'Demo',
    rol: 'mecanico',
    is_active: true,
    estado: 2,
    estado_nombre: 'Miranda',
  },
]
