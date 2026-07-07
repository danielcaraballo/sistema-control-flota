# SCF — Sistema de Control de Flota

<p>
  <img src="https://img.shields.io/badge/python-3.11-blue?logo=python" alt="Python 3.11">
  <img src="https://img.shields.io/badge/django-5.2-green?logo=django" alt="Django 5.2">
  <img src="https://img.shields.io/badge/vue-3.5-brightgreen?logo=vue.js" alt="Vue 3.5">
  <img src="https://img.shields.io/badge/license-MIT-yellow" alt="License MIT">
</p>

Sistema corporativo para la gestión integral de flota vehicular. Centraliza el inventario nacional, automatiza mantenimientos preventivos y garantiza la trazabilidad de datos desde el taller hasta la gerencia.

## Stack

| Capa | Tecnología |
|---|---|
| Backend | Python + Django + Ninja |
| Frontend | Vue 3 + Pinia + Vite |
| UI | PrimeVue 4 + Tailwind CSS 4 |
| Base de datos | PostgreSQL 15+ (SQLite en desarrollo) |

Versiones exactas y dependencias adicionales en [`docs/architecture.md`](docs/architecture.md).

## Requisitos

- Python 3.11+
- Node.js 18+
- [uv](https://docs.astral.sh/uv/) (gestor de paquetes Python)
- PostgreSQL 15+ (opcional, fallback a SQLite)

## Inicio rápido

```bash
# ── Backend ──
cd backend
cp .env.example .env
uv sync
uv run python manage.py migrate
uv run python manage.py runserver

# ── Frontend (otra terminal) ──
cd frontend
cp .env.example .env
npm install
npm run dev
```

## Estructura del proyecto

```
sistema-control-flota/
├── backend/
│   ├── config/              # Configuración Django (settings, urls, api root)
│   │   └── api.py           #   NinjaAPI root + routers
│   ├── utils/               # Helpers compartidos
│   │   ├── api_helpers.py   #   filter_activos, get_object_or_404, check_duplicate
│   │   └── crud_factory.py  #   register_crud + CrudConfig genérico
│   ├── usuarios/            # App: Usuario (AbstractUser), Auth, CRUD usuarios
│   │   ├── auth_api.py      #   Login, refresh, /me, change-password
│   │   ├── usuarios_api.py  #   CRUD usuarios + reset password
│   │   ├── models.py        #   Usuario con roles RBAC
│   │   ├── schemas.py       #   Esquemas Ninja
│   │   ├── roles.py         #   Jerarquía de roles y decoradores
│   │   └── tests.py         #   Tests
│   ├── organizacion/        # App: Estado, Gerencia, CentroDeServicio
│   │   ├── api.py           #   CRUD endpoints
│   │   ├── models.py        #   Modelos ORM
│   │   └── tests.py         #   Tests
│   ├── catalogos/           # App: Marcas, Modelos, Tipos, Colores, etc.
│   │   ├── api.py           #   CRUD para 9 catálogos
│   │   ├── models.py        #   9 modelos de catálogo
│   │   └── tests.py         #   Tests
│   ├── vehiculos/           # App: Vehiculo CRUD + QR
│   │   ├── api.py           #   CRUD con filtro por estado y QR
│   │   ├── models.py        #   Vehiculo (17 campos)
│   │   └── tests.py         #   Tests
│   ├── dashboard/           # Unfold dashboard callback
│   │   └── callbacks.py     #   KPIs, charts, tabla usuarios
│   ├── manage.py
│   └── pyproject.toml       # Dependencias + Ruff config
├── frontend/
│   ├── src/
│   │   ├── layouts/         # DefaultLayout (sidebar dinámico por rol)
│   │   ├── views/           # Dashboard, Login, Usuarios, Vehículos, etc.
│   │   ├── components/      # PageHeader, ConfirmDialog, CatalogoTabContent, etc.
│   │   ├── composables/     # useTheme (dark/light/system)
│   │   ├── stores/          # Pinia store (auth)
│   │   ├── services/        # Axios client + interceptors
│   │   ├── utils/           # roles.js (constantes + helpers)
│   │   └── router/          # Vue Router + guards
│   └── package.json
├── docs/
│   ├── architecture.md      # C4, stack, ADRs, NFRs
│   └── database.md          # DER, data dictionary, RBAC
└── README.md
```

## Funcionalidades

| Módulo | Estado |
|---|---|
| Autenticación JWT (login/refresh/me/change-password) | ✅ |
| CRUD de usuarios con roles (RBAC) | ✅ |
| Catálogos (Marcas, Modelos, Tipos, Colores, Fallas, etc.) | ✅ |
| Organización (Estados, Gerencias, Centros de Servicio) | ✅ |
| Gestión de Vehículos con QR | ✅ |
| Dashboard con KPIs | 🟡 Skeleton |
| Módulo de Taller | 🚧 Planificado |
| Mantenimiento Preventivo | 🚧 Planificado |
| Reportes y analítica | 🚧 Planificado |

## Comandos útiles

```bash
# Backend
uv run python manage.py runserver      # Iniciar servidor de desarrollo
uv run python manage.py test           # Ejecutar tests
uv run python manage.py migrate        # Aplicar migraciones
uv run python manage.py makemigrations # Crear migraciones
uv run ruff check .                    # Linting
uv run ruff format .                   # Formateo

# Frontend
npm run dev                            # Servidor de desarrollo
npm run build                          # Build producción
npm run lint                           # Linting (ESLint)
npm run format                         # Formateo (Prettier)
```

## Documentación

- **Arquitectura:** [`docs/architecture.md`](docs/architecture.md)
- **Base de datos y DER:** [`docs/database.md`](docs/database.md)
- **API (Swagger):** `/api/docs` (servidor backend corriendo)

## Pruebas

```bash
cd backend && uv run python manage.py test
```

## Linting

```bash
# Backend
cd backend && uv run ruff check .

# Frontend
cd frontend && npm run lint
```
