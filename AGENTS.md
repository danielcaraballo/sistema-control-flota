# SCF — AI Agent Instructions

> Para humanos: ver [`CONTRIBUTING.md`](CONTRIBUTING.md).

Monorepo: `backend/` (Django 5.2 + Ninja) + `frontend/` (Vue 3.5 + Vite). No monorepo tool; each side runs independently.

## Commands

| Scope | Command (from its own directory) |
|---|---|
| Backend dev | `uv run python manage.py runserver` |
| Backend test | `uv run python manage.py test` (all apps) |
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
- **Roles hierarchy**: `MECANICO < ANALISTA < ESTATAL < NACIONAL`. Defined in `usuarios/roles.py`. The `acotar_por_estado()` helper exists but is unused; vehiculos uses inline filtering instead.
- **Deps**: `uv sync` (not pip). Config in `backend/pyproject.toml`.
- **Apps**: `config` (settings/urls/api root), `usuarios` (User model + auth), `organizacion` (Estado, Gerencia, CentroDeServicio), `catalogos` (Marca, Modelo, TipoVehiculo, TipoUso, Color, SistemaAfectado, EstatusVehiculo, ColorPlaca, TipoFalla), `vehiculos` (Vehiculo CRUD with QR code generation), `dashboard` (Unfold dashboard callback with KPIs/charts).

## Frontend conventions

- **Vue**: Composition API (`<script setup>`). Views under `src/views/`, components under `src/components/`.
- **PrimeVue 4**: Components imported individually. Theme: Aura preset with custom font override in `main.js`. Tooltip registered globally (`v-tooltip.top`). Ripple enabled.
- **View patterns**:
  - **CRUD table views** (`UsuariosView`, `VehiculosView`): `PageHeader` + border-wrapped `DataTable` (scrollable, stripedRows, paginator, globalFilter via `IconField` + `InputText`) + `Dialog` for CRUD + `ConfirmDialog` from `@/components/ConfirmDialog.vue`.
  - **Tabbed catalog views** (`OrganizacionView`, `CatalogosView`): `TabView` + `TabPanel` reusing `CatalogoTabContent` component which handles generic CRUD (DataTable, Dialog, soft-delete/reactivate, skeleton loading).
  - **Detail view** (`VehiculoDetalleView`): Ficha técnica with QR code, 3 sections (Identificación, Características, Asignación), actions for edit/deactivate.
- **API client**: `@/services/api.js` — Axios with baseURL from `VITE_API_URL` env var (default `http://localhost:8000/api`). Bearer token from `localStorage.access_token`, auto-refresh on 401.
- **Router**: `src/router/index.js`. Guard `beforeEach` checks `requiresAuth` and `rolMinimo` meta. Routes use `meta: { rolMinimo: ROL_NACIONAL }` where applicable. `rolMinimo` values from `@/utils/roles` (`ROL_NACIONAL`, `ROL_ANALISTA`).
- **Sidebar**: Built dynamically in `DefaultLayout.vue` via `auth.tieneRol()`. Items: Dashboard (all), Vehiculos (all), Taller (all), Reportes (ANALISTA+), Usuarios/Organización/Catálogos (NACIONAL only).
- **ESLint**: Flat config (`eslint.config.js`). No `vue/multi-word-component-names`. Prettier as plugin: no semi, single quotes, trailing commas, printWidth 100.
- **Styling**: Tailwind v4 (`@import 'tailwindcss'` in `main.css`, no config file). `tailwindcss-primeui` plugin bridges PrimeVue + Tailwind. Custom CSS variables for sidebar dimensions and page background in `main.css`.
- **Theme**: Light/dark/system toggle in `UserDropdown.vue`, managed by `@/composables/useTheme.js`. Dark class (`p-dark`) applied to `<html>`.
- **Role utils**: `@/utils/roles.js` exports `ROL_MECANICO`, `ROL_ANALISTA`, `ROL_ESTATAL`, `ROL_NACIONAL`, `tieneRolMinimo()`, `esEstatal()`, `rolLabel()`, `rolSeverity()`, and `ROLES`/`ESTATAL_ROLES` arrays.

## Commits

- Formato [Conventional Commits](https://www.conventionalcommits.org/).
- `tipo: mensaje en español` (minúscula, sin punto final).
- Tipos: `feat`, `fix`, `refactor`, `perf`, `style`, `docs`, `test`, `chore`.
- Alcance opcional entre paréntesis: `fix(vehiculos): descripción`.
- Máximo 72 caracteres. Cuerpo si se necesita explicar el qué y el porqué.

## Repo-level

- No Makefile, no CI, no pre-commit hooks. No `.env` files tracked (`.env.example` in each directory).
- Docs in `docs/architecture.md` (C4, stack, ADRs, NFRs) and `docs/database.md` (DER, data dictionary, RBAC).

## Documentation rules

- **`docs/database.md`** is the source of truth for models, DER, business rules, and RBAC matrix. UPDATE whenever a model changes (new field, new app, new constraint).
- **`docs/architecture.md`** is the source of truth for C4 diagrams, stack versions, and ADRs. UPDATE when stack or architectural decisions change.
- **`CHANGELOG.md`** is version history. UPDATE on each meaningful change (new feature, breaking change, milestone).
- **README.md** must reflect current structure and commands. UPDATE when directory structure or dev workflow changes.
