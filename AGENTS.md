# SCF — Sistema de Control de Flota

Monorepo: `backend/` (Django 5.2 + Ninja) + `frontend/` (Vue 3.5 + Vite). No monorepo tool; each side runs independently.

## Commands

| Scope | Command (from its own directory) |
|---|---|
| Backend dev | `python manage.py runserver` |
| Backend test | `python manage.py test` (all apps) |
| Backend lint | `uv run ruff check .` |
| Backend format | `uv run ruff format .` |
| Frontend dev | `npm run dev` |
| Frontend lint | `npx eslint .` (flat config, Prettier integrated as rule) |
| Frontend format | `npx prettier --write .` |

## Backend conventions

- **API**: Django Ninja `Router` + `JWTAuth` + `@requiere_rol_minimo(Usuario.Rol.XXX)` decorator from `usuarios/roles.py`.
- **Schemas**: `ModelSchema` for reads, plain `Schema` for Create/Update payloads.
- **Tests**: `TestClient(api)` from `ninja.testing` + `django.test.TestCase`. Create user + login in `setUp`, reuse token via headers.
- **Soft-delete**: Every model has `estatus_activo = BooleanField(default=True)`. GET endpoints filter `.filter(estatus_activo=True)` by default; pass `?incluir_inactivos=true` to override.
- **Migrations**: `makemigrations` + `migrate` as usual. Seed/migration data goes in numbered migration files. Ruff ignores `*/migrations/*`.
- **Roles hierarchy**: `MECANICO < ANALISTA < ESTATAL < NACIONAL`. Defined in `usuarios/roles.py`.
- **Deps**: `uv sync` (not pip). Config in `backend/pyproject.toml`.

## Frontend conventions

- **Vue**: Composition API (`<script setup>`). Views under `src/views/`, components under `src/components/`.
- **PrimeVue 4**: Components imported individually. Theme: Aura preset with custom font override in `main.js`. Tooltip registered globally (`v-tooltip.top`).
- **View pattern**: `PageHeader` + border-wrapped `DataTable` (scrollable, stripedRows, paginator, globalFilter via `IconField` + `InputText`) + `Dialog` for CRUD + `ConfirmDialog` from `@/components/ConfirmDialog.vue`.
- **API client**: `@/services/api.js` — Axios with baseURL from `VITE_API_URL` env var (default `http://localhost:8000/api`). Bearer token from `localStorage.access_token`, auto-refresh on 401.
- **Router**: `src/router/index.js`. Guard `beforeEach` checks `requiresAuth` and `rolMinimo` meta. Routes use `meta: { rolMinimo: 'nacional' }` where applicable.
- **Sidebar**: Built dynamically in `DefaultLayout.vue` via `auth.tieneRol()`.
- **ESLint**: Flat config (`eslint.config.js`). No `vue/multi-word-component-names`. Prettier as plugin: no semi, single quotes, trailing commas, printWidth 100.
- **Styling**: Tailwind v4 (`@import 'tailwindcss'` in `main.css`, no config file). `tailwindcss-primeui` plugin bridges PrimeVue + Tailwind.

## Repo-level

- No Makefile, no CI, no pre-commit hooks. No `.env` files tracked (`.env.example` in each directory).
- Docs in `docs/architecture.md` (C4 diagrams, DER, ADRs).
- `openforce.json` does not exist. No custom AGENTS.md previously.
