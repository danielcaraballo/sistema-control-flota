# Contribuir a SCF

## Inicio rápido

Ver [`README.md`](README.md) para requisitos e instalación.

## Comandos

### Backend

| Acción | Comando (desde `backend/`) |
|---|---|
| Servidor dev | `uv run python manage.py runserver` |
| Tests | `uv run python manage.py test` |
| Linting | `uv run ruff check .` |
| Formateo | `uv run ruff format .` |
| Migraciones | `uv run python manage.py makemigrations` |
| Migrar | `uv run python manage.py migrate` |

### Frontend

| Acción | Comando (desde `frontend/`) |
|---|---|
| Servidor dev | `npm run dev` |
| Build | `npm run build` |
| Linting | `npm run lint` |
| Formateo | `npm run format` |

## Convenciones de estilo

### Backend

- **API**: Django Ninja `Router` + `JWTAuth` + `@requiere_rol_minimo(Usuario.Rol.XXX)`
- **Schemas**: `ModelSchema` para lecturas, `Schema` plano para Create/Update
- **Tests**: `TestClient(api)` de `ninja.testing` + `django.test.TestCase`. Crear usuario + login en `setUp`, reutilizar token vía headers
- **Soft-delete**: Todo modelo tiene `estatus_activo = BooleanField(default=True)`. GET endpoints filtran `.filter(estatus_activo=True)` por defecto; `?incluir_inactivos=true` para anular
- **Roles**: `MECANICO < ANALISTA < ESTATAL < NACIONAL` definido en `usuarios/roles.py`
- **Deps**: `uv sync` (no pip). Config en `backend/pyproject.toml`

### Frontend

- **Vue**: Composition API (`<script setup>`). Vistas en `src/views/`, componentes en `src/components/`
- **PrimeVue 4**: Componentes importados individualmente. Tema: Aura preset en `main.js`
- **API client**: `@/services/api.js` — Axios con `VITE_API_URL`, Bearer token desde `localStorage.access_token`, auto-refresh en 401
- **Router**: `src/router/index.js` con guard `beforeEach` que verifica `requiresAuth` y `rolMinimo`
- **Sidebar**: Dinámica en `DefaultLayout.vue` según rol del usuario
- **ESLint**: Flat config (`eslint.config.js`). Prettier integrado: sin semicolon, single quotes, trailing commas, printWidth 100
- **Styling**: Tailwind v4 (`@import 'tailwindcss'` en `main.css`, sin archivo de configuración)
- **Tema**: Claro/oscuro/sistema vía `UserDropdown.vue` + `@/composables/useTheme.js`

## Commits

Formato [Conventional Commits](https://www.conventionalcommits.org/):

```
tipo: mensaje en español
```

- `tipo` en minúscula, sin punto final
- Tipos: `feat`, `fix`, `refactor`, `perf`, `style`, `docs`, `test`, `chore`
- Alcance opcional entre paréntesis: `fix(vehiculos): descripción`
- Máximo 72 caracteres. Cuerpo opcional para explicar qué y porqué

## Documentación

Mantener actualizada cuando se hagan cambios significativos:

- **`docs/database.md`** — modelos, DER, reglas de negocio, matriz RBAC
- **`docs/architecture.md`** — diagramas C4, stack, ADRs, NFRs
- **`CHANGELOG.md`** — historial de versiones
- **`README.md`** — estructura del proyecto y comandos
