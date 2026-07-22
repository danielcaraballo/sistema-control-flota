# SCF — Sistema de Control de Flota

<p>
  <img src="https://img.shields.io/badge/python-3.11-blue?logo=python" alt="Python 3.11">
  <img src="https://img.shields.io/badge/django-5.2-green?logo=django" alt="Django 5.2">
  <img src="https://img.shields.io/badge/vue-3.5-brightgreen?logo=vue.js" alt="Vue 3.5">
  <img src="https://img.shields.io/badge/license-MIT-yellow" alt="License MIT">
</p>

Sistema web para la gestión centralizada del inventario de flota vehicular. Permite registrar, consultar y mantener fichas técnicas de vehículos con generación de códigos QR, control de acceso por roles (RBAC), catálogos configurables y estructura organizativa jerárquica por estados y gerencias.

> 🚧 **Estado del proyecto:** SCF se encuentra en una fase temprana de desarrollo activo. La arquitectura, API y flujos de trabajo pueden experimentar cambios significativos mientras evolucionamos hacia una versión estable.

## Stack

| Capa | Tecnología |
|---|---|
| Backend | Python + Django + Ninja |
| Frontend | Vue 3 + Pinia + Vite |
| UI | PrimeVue 4 + Tailwind CSS 4 |
| Base de datos | PostgreSQL 15+ (SQLite en desarrollo) |

Versiones exactas y dependencias adicionales en [`docs/architecture.md`](docs/architecture.md).

## Funcionalidades actuales (v0.10.0)

- Autenticación JWT (login, refresh, perfil, cambio de contraseña)
- CRUD de usuarios con 4 roles jerárquicos (RBAC) y asignación por estado
- Catálogos auxiliares configurables (11 tablas maestras)
- Organización jerárquica (Estados, Gerencias, Centros de Servicio)
- Gestión de vehículos con 20 campos, códigos QR e indicador de completitud
- Dashboard administrativo en Unfold con KPIs y charts
- 121 tests, 0 warnings de linter

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
uv run python manage.py createsuperuser
uv run python manage.py runserver

# Población de datos: para usar el sistema necesitas cargar datos de
# referencia (catálogos, organización). Puedes hacerlo de tres formas:
#   1. Cargar fixtures externos: uv run python manage.py loaddata fixtures/*.json
#   2. Admin de Django:          navegar a /admin/ y crear los registros
#   3. Frontend/API:             una vez logueado, usar el módulo Catálogos

# ── Frontend (otra terminal) ──
cd frontend
cp .env.example .env
npm install
npm run dev
```

## Estructura del proyecto

```
sistema-control-flota/
├── backend/    # Django 5.2 + Ninja API
├── frontend/   # Vue 3 + Vite
└── docs/       # Arquitectura, DER, estructura
```

📂 Vista completa: [`docs/structure.md`](docs/structure.md)

## Comandos útiles

```bash
# Backend
uv run python manage.py runserver      # Iniciar servidor de desarrollo
uv run python manage.py test           # Ejecutar tests
uv run python manage.py migrate        # Aplicar migraciones
uv run python manage.py makemigrations # Crear migraciones
uv run ruff check .                    # Linting
uv run ruff format .                   # Formateo
uv run python manage.py backfill_qr    # Generar QR para vehículos sin código QR

# Frontend
npm run dev                            # Servidor de desarrollo
npm run build                          # Build producción
npm run lint                           # Linting (ESLint)
npm run format                         # Formateo (Prettier)
```

## Documentación

- **Arquitectura:** [`docs/architecture.md`](docs/architecture.md)
- **Base de datos y DER:** [`docs/database.md`](docs/database.md)
- **Estructura del proyecto:** [`docs/structure.md`](docs/structure.md)
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

---

© 2026 Daniel Caraballo. Licencia MIT.

¿Te gusta el proyecto? Dale una ⭐ en [GitHub](https://github.com/danielcaraballo/sistema-control-flota)
