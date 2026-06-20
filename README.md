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
| Backend | Python 3.11+ · Django 5.2 · Django Ninja |
| Autenticación | django-ninja-jwt (access + refresh tokens) |
| Frontend | Vue 3.5 · Pinia · Vue Router 5 |
| UI | PrimeVue 4 · PrimeIcons |
| PWA | vite-plugin-pwa (offline-first) |
| Base de datos | PostgreSQL 15+ (SQLite en desarrollo) |
| Linting | Ruff (backend) · ESLint + Prettier (frontend) |
| Gestión de deps | uv (backend) · npm (frontend) |

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
python manage.py migrate
python manage.py runserver

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
│   ├── config/              # Configuración Django (settings, urls, api)
│   ├── organizacion/        # App: Estado, Gerencia
│   │   ├── api.py           #   Endpoints públicos
│   │   ├── models.py        #   Modelos ORM
│   │   └── tests.py         #   Tests
│   ├── usuarios/            # App: Usuario, Auth
│   │   ├── auth_api.py      #   Login, refresh, /me
│   │   ├── usuarios_api.py  #   CRUD usuarios
│   │   ├── models.py        #   Usuario (AbstractUser)
│   │   ├── schemas.py       #   Esquemas Ninja
│   │   └── tests.py         #   Tests
│   ├── manage.py
│   └── pyproject.toml       # Dependencias + Ruff config
├── frontend/
│   ├── src/
│   │   ├── layouts/         # AuthLayout, DefaultLayout
│   │   ├── views/           # Dashboard, Usuarios, Vehículos, Taller...
│   │   ├── stores/          # Pinia stores (auth)
│   │   ├── services/        # Axios client + interceptors
│   │   └── router/          # Vue Router + guards
│   └── package.json
├── docs/
│   └── architecture.md      # C4, DER, APIs, ADRs
└── README.md
```

## Funcionalidades

| Módulo | Estado |
|---|---|
| Autenticación JWT (login/refresh/me) | ✅ |
| CRUD de usuarios con roles (RBAC) | ✅ |
| Catálogo de Estados y Gerencias | ✅ |
| Dashboard con KPIs | 🟡 Skeleton |
| Gestión de Vehículos | 🚧 Planificado |
| Módulo de Taller | 🚧 Planificado |
| Mantenimiento Preventivo | 🚧 Planificado |
| Reportes y analítica | 🚧 Planificado |

## Comandos útiles

```bash
# Backend
python manage.py runserver     # Iniciar servidor de desarrollo
python manage.py test          # Ejecutar tests
python manage.py migrate       # Aplicar migraciones
python manage.py makemigrations# Crear migraciones
uv run ruff check .            # Linting
uv run ruff format .           # Formateo

# Frontend
npm run dev                    # Servidor de desarrollo
npm run build                  # Build producción
npx eslint .                   # Linting
npx prettier --write .         # Formateo
```

## Documentación

- **Arquitectura y DER:** [`docs/architecture.md`](docs/architecture.md)
- **API (Swagger):** `/api/docs` (servidor backend corriendo)

## Pruebas

```bash
cd backend
python manage.py test
```

## Linting

```bash
# Backend
cd backend && uv run ruff check .

# Frontend
cd frontend && npx eslint .
```
