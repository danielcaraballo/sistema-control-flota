# Estructura del proyecto

```
sistema-control-flota/
├── backend/
│   ├── config/                    # Configuración Django
│   │   ├── settings.py            #   Settings + Unfold sidebar
│   │   ├── urls.py                #   URLs raíz
│   │   └── api.py                 #   NinjaAPI root + routers
│   ├── utils/
│   │   ├── api_helpers.py         #   filter_activos, get_object_or_404, check_duplicate
│   │   └── crud_factory.py        #   register_crud + CrudConfig genérico
│   ├── usuarios/                  # App: Usuario, Auth, CRUD
│   │   ├── auth_api.py            #   Login, refresh, /me, change-password
│   │   ├── usuarios_api.py        #   CRUD + reset password
│   │   ├── models.py              #   Usuario con roles RBAC
│   │   ├── schemas.py             #   Esquemas Ninja
│   │   ├── roles.py               #   Jerarquía de roles y decoradores
│   │   └── tests.py
│   ├── organizacion/              # App: Estado, Gerencia, CentroDeServicio
│   │   ├── api.py                 #   CRUD via factory
│   │   ├── models.py
│   │   └── tests.py
│   ├── catalogos/                 # App: 11 tablas maestras
│   │   ├── api.py                 #   CRUD via factory
│   │   ├── models.py
│   │   └── tests.py
│   ├── vehiculos/                 # App: Vehiculo CRUD + QR
│   │   ├── api.py                 #   CRUD con filtros, paginación, exportación
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── tests.py
│   ├── dashboard/                 # Dashboard para Unfold admin
│   │   └── callbacks.py
│   ├── manage.py
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── layouts/               # DefaultLayout (sidebar dinámico por rol)
│   │   ├── views/                 # Dashboard, Login, Usuarios, Vehículos, etc.
│   │   ├── components/            # PageHeader, ConfirmDialog, CatalogoTabContent, etc.
│   │   ├── composables/           # useTheme (dark/light/system)
│   │   ├── stores/                # Pinia store (auth)
│   │   ├── services/              # Axios client + interceptors
│   │   ├── utils/                 # roles.js (constantes + helpers)
│   │   └── router/                # Vue Router + guards
│   └── package.json
├── docs/
│   ├── architecture.md            # C4, stack, ADRs, NFRs
│   ├── database.md                # DER, data dictionary, RBAC
│   └── structure.md               # Este archivo
├── CHANGELOG.md
├── CONTRIBUTING.md
└── README.md
```
