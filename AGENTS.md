# SCF — AI Agent Instructions

> Para humanos: ver [`CONTRIBUTING.md`](CONTRIBUTING.md).

Monorepo: `backend/` (Django 5.2 + Ninja) + `frontend/` (Vue 3.5 + Vite). No monorepo tool; each side runs independently.

## Commands

| Scope | Command (from its own directory) |
|---|---|
| Backend dev | `uv run python manage.py runserver` |
| Backend test | `uv run python manage.py test` (all apps) |
| Backend shell | `uv run python manage.py shell` |
| Backend lint | `uv run ruff check .` |
| Backend format | `uv run ruff format .` |
| Frontend dev | `npm run dev` |
| Frontend lint | `npx eslint .` (flat config, Prettier integrated as rule) |
| Backend backfill QR | `uv run python manage.py backfill_qr` |
| Frontend format | `npx prettier --write .` |

## Backend conventions

- **API**: Django Ninja `Router` + `JWTAuth` + `@requiere_rol_minimo(Usuario.Rol.XXX)` decorator from `usuarios/roles.py`.
- **Schemas**: `ModelSchema` for reads, plain `Schema` for Create/Update payloads.
- **Tests**: `TestClient(api)` from `ninja.testing` + `django.test.TestCase`. Create user + login in `setUp`, reuse token via headers.
- **Soft-delete**: Most models have `estatus_activo = BooleanField(default=True)`. GET endpoints filter `.filter(estatus_activo=True)` by default; pass `?incluir_inactivos=true` to override. Exception: `Usuario` inherits `is_active` from `AbstractUser` instead.
- **Migrations**: `makemigrations` + `migrate` as usual. Ruff ignores `*/migrations/*` (via `exclude` + `per-file-ignores = ["ALL"]` in `pyproject.toml`).
- **Roles hierarchy**: `MECANICO < ANALISTA < ESTATAL < NACIONAL`. Defined in `usuarios/roles.py`. The `acotar_por_estado()` helper exists but is unused; vehiculos uses inline filtering instead.
- **Deps**: `uv sync` (not pip). Config in `backend/pyproject.toml`.
- **Apps**: `config` (settings/urls/api root), `usuarios` (User model + auth), `organizacion` (Estado, Gerencia, CentroDeServicio), `catalogos` (Marca, Modelo, TipoVehiculo, TipoUso, Color, SistemaAfectado, EstatusVehiculo, ColorPlaca, TipoFalla), `vehiculos` (Vehiculo CRUD with QR code generation), `dashboard` (Unfold dashboard callback with KPIs/charts).
- **Errores API**: Usar `HttpError(código, mensaje)` de Ninja para errores controlados. En `crud_factory.py` se usa `HttpError(409)` para duplicados y `HttpError(400)` para validación de FK.
- **on_delete**: Usar `RESTRICT` como regla general. Excepciones conocidas: `Modelo.marca` usa `CASCADE` (relación padre-hijo natural), `Usuario.estado` usa `SET_NULL` (preservar usuarios al eliminar estado).
- **API Vehículos** (`vehiculos/api.py`): Endpoint `GET /vehiculos/` con paginación server-side (`limit`/`offset`, max 100), ordenamiento vía `sort_by`/`sort_order` con whitelist `SORT_FIELD_MAP` (evita SQL injection en `order_by`), búsqueda sobre 6 campos (`numero_economico`, `vin`, `placa`, `placa_intt`, `serial_motor`, `numero_unidad` via `__icontains`), filtros por `estado_id`/`estatus_id`/`gerencia_id`, y auto-scope al estado del usuario autenticado. Endpoint `GET /vehiculos/exportar` con soporte CSV/XLSX. Usar `filter_activos(qs, request)` para soft-delete (acepta QuerySet, no Model).

### Agregar un nuevo modelo al admin de Django + Unfold

Cada vez que se crea un nuevo modelo de catálogo (o cualquier modelo que deba aparecer en el admin):

1. **Definir el modelo** en `backend/<app>/models.py` — incluir `estatus_activo`, `Meta.ordering`, `UniqueConstraint` condicional y `__str__`. Excepción: `Usuario` hereda de `AbstractUser` y no sigue este patrón.
2. **Crear migración** con `makemigrations`.
3. **Registrar el modelo** en `backend/<app>/admin.py` con `@admin.register(Modelo)` heredando de `unfold.admin.ModelAdmin`, definiendo `list_display`, `search_fields` y `list_filter`.
4. **Agregar entrada en el sidebar** de Unfold en `backend/config/settings.py`, dentro del diccionario `UNFOLD['SIDEBAR']['navigation']`, en la sección correspondiente. Cada entrada tiene la forma:
   ```python
   {
       "title": "Nombre Visible",
       "icon": "icon_name",  # https://fonts.google.com/icons
       "link": reverse_lazy("admin:<app_label>_<model_name>_changelist"),
   }
   ```
   El `reverse_lazy` sigue el patrón `admin:{app_label}_{modelo}_changelist` (minúsculas).
5. **Opcional — CRUD API:** Si el modelo necesita endpoints REST, crear schemas en `schemas.py` y usar la fábrica de CRUD en `api.py`:

   ```python
   from utils.crud_factory import CrudConfig, register_crud

   cfg = CrudConfig(
       prefix="tipo-falla",                    # parte de la URL
       model=TipoFalla,                        # modelo Django
       read_schema=TipoFallaRead,              # schema de respuesta
       create_schema=TipoFallaCreate,          # schema de creación
       update_schema=TipoFallaUpdate,          # schema de actualización
       display_name="tipo de falla",           # nombre legible (minúscula)
       article="un",                           # artículo para mensajes ("un"/"una")
       unique_field="nombre",                  # campo único para detección de duplicados
       unique_field_label="nombre",            # etiqueta del campo único
       rol_list=Usuario.Rol.MECANICO,          # rol mínimo para listar/ver
       rol_mutate=Usuario.Rol.NACIONAL,        # rol mínimo para crear/editar/eliminar
       select_related=None,                    # lista de FKs a prefetch
       response_builder=None,                  # callable para transformar respuesta
       fk_validations=[],                      # validaciones de FK activas
   )
   register_crud(router, cfg)
   ```

   La fábrica genera 5 endpoints automáticos: `GET /{prefix}/` (lista), `GET /{prefix}/{id}` (detalle), `POST /{prefix}/` (crear), `PUT /{prefix}/{id}` (actualizar), `DELETE /{prefix}/{id}` (desactivar). Importar el router en `config/api.py`.

## Agregar una nueva entidad con CRUD completo (backend + frontend)

Cuando se necesita una entidad nueva con CRUD completo (no solo admin), seguir este flujo:

1. **Modelo + migración** en `backend/<app>/models.py` — incluir `estatus_activo`, `Meta.ordering`, `UniqueConstraint` condicional y `__str__`. Excepción: `Usuario` hereda de `AbstractUser` y no sigue este patrón. Ejecutar `makemigrations` + `migrate`.
2. **Schemas Ninja** en `backend/<app>/schemas.py` — `ModelSchema` para lectura, `Schema` plano para Create/Update.
3. **API CRUD** en `backend/<app>/api.py` — usar `CrudConfig` + `register_crud` (ver paso 5 arriba) o endpoints manuales si la lógica lo requiere. Importar el router en `config/api.py`.
4. **Admin Unfold** en `backend/<app>/admin.py` — registrar con `@admin.register(Modelo)` heredando de `unfold.admin.ModelAdmin`, agregar al sidebar en `config/settings.py`.
5. **Vista Vue** en `frontend/src/views/` — seguir patrón existente (DataTable + Dialog para listado, o detalle si aplica). Agregar ruta en `frontend/src/router/index.js` con `meta: { rolMinimo }`.
6. **Sidebar frontend** en `frontend/src/layouts/DefaultLayout.vue` — agregar entrada en el menú dinámico según rol.
7. **Opcional — MSW handlers** en `frontend/src/mocks/handlers/` — si la entidad debe funcionar en demo mode, agregar handler y datos de ejemplo.

## Frontend conventions

- **Vue**: Composition API (`<script setup>`). Views under `src/views/`, components under `src/components/`.
- **PrimeVue 4**: Components imported individually. Theme: Aura preset with custom font override in `main.js`. Tooltip registered globally (`v-tooltip.top`). Ripple enabled.
- **View patterns**:
  - **CRUD table views** (`UsuariosView`, `VehiculosView`): `PageHeader` + border-wrapped `DataTable` (scrollable, stripedRows, paginator, globalFilter via `IconField` + `InputText`) + `Dialog` for CRUD + `ConfirmDialog` from `@/components/ConfirmDialog.vue`. Estado consistente: skeleton loading (`v-if="loading"`), empty state (`v-if="!loading && !items.length"`), error handling via Toast (`life: 4000`, `bottom-right`). Formularios con snapshot + dirty checking: clonar `form` al abrir, comparar en `save`, confirmación al cerrar si hay cambios sin guardar.
  - **Tabbed catalog views** (`OrganizacionView`, `CatalogosView`): `TabView` + `TabPanel` reusing `CatalogoTabContent` component which handles generic CRUD (DataTable, Dialog, soft-delete/reactivate, skeleton loading). Cada pestaña recibe un prop `config` con el contrato descrito abajo.
  - **Detail view** (`VehiculoDetalleView`): Ficha técnica with QR code, 3 sections (Identificación, Características, Asignación), actions for edit/deactivate.
  - **CatalogoTabContent config contract**: Cada `TabPanel` recibe `:config="{ key, label, endpoint, icon, field, filterField }"` donde `key` identifica el tipo (ej: `'modelos'`, `'tiposFalla'`), `label` es el header de columna, `endpoint` es la URL base de la API, `icon` es la clase PrimeIcon para empty state, `field` es el campo principal del modelo, y `filterField` es el campo para globalFilter del DataTable. Opcional: `:fkCatalogs="{ marcas, sistemas, estados }"` para Dropdowns de FK.
- **API client**: `@/services/api.js` — Axios with baseURL from `VITE_API_URL` env var (default `http://localhost:8000/api`). Bearer token from `localStorage.access_token`, auto-refresh on 401 con patrón singleton (`refreshPromise`) para evitar refrescos concurrentes. Errores no-401 se rechazan para manejo local con Toast.
- **Router**: `src/router/index.js`. Guard `beforeEach` checks `requiresAuth` and `rolMinimo` meta. Routes use `meta: { rolMinimo: ROL_NACIONAL }` where applicable. `rolMinimo` values from `@/utils/roles` (`ROL_NACIONAL`, `ROL_ANALISTA`). Integración con `NProgress` (`start` en beforeEach, `done` en afterEach/onError). Gate de `auth.initialized` promise si el store está en `loading`. Redirect query param (`?redirect=`) para post-login.
- **Sidebar**: Built dynamically in `DefaultLayout.vue` via `auth.tieneRol()`. Items: Dashboard (all), Vehiculos (all), Taller (all), Reportes (ANALISTA+), Usuarios/Organización/Catálogos (NACIONAL only). Modo mobile con overlay (`fixed md:relative`, backdrop semitransparente). Colapso en desktop (`w-[260px]` ↔ `w-[64px]`), secciones agrupadas (principal + "Administración"), active highlight via `route.path === item.path || route.path.startsWith(item.path + '/')`.
- **ESLint**: Flat config (`eslint.config.js`). No `vue/multi-word-component-names`. Prettier as plugin: no semi, single quotes, trailing commas, printWidth 100.
- **Styling**: Tailwind v4 (`@import 'tailwindcss'` in `main.css`, no config file). `tailwindcss-primeui` plugin bridges PrimeVue + Tailwind. Custom CSS variables for sidebar dimensions and page background in `main.css`.
- **Theme**: Light/dark/system toggle in `UserDropdown.vue`, managed by `@/composables/useTheme.js`. Dark class (`p-dark`) applied to `<html>`.
- **Role utils**: `@/utils/roles.js` exports `ROL_MECANICO`, `ROL_ANALISTA`, `ROL_ESTATAL`, `ROL_NACIONAL`, `tieneRolMinimo()`, `esEstatal()`, `rolLabel()`, `rolSeverity()`, and `ROLES`/`ESTATAL_ROLES` arrays.
- **Pinia stores**: Composition API (`defineStore('name', () => {...})`) en `src/stores/`. Store único actual: `auth.js` con patrón `initialized` promise gate para autenticación. No crear stores globales sin coordinación.
- **Composables**: Archivos en `src/composables/`. Pueden ser singleton (estado a nivel de módulo, ej: `useTheme.js`) o por instancia. Preferir singletons para config global, instancia para lógica de componentes.
- **Demo mode**: Activado con `VITE_DEMO_MODE=true`. Usa MSW (Mock Service Worker) para interceptar peticiones. Handlers en `src/mocks/handlers/`, datos en `src/mocks/data/`. Agregar handler por cada nuevo endpoint que deba funcionar en demo.

## Commits

Formato [Conventional Commits](https://www.conventionalcommits.org/).

- `tipo: mensaje en español` (minúscula, sin punto final)
- Tipos: `feat`, `fix`, `refactor`, `perf`, `style`, `docs`, `test`, `chore`
- Alcance opcional entre paréntesis: `fix(vehiculos): descripción`
- Máximo 72 caracteres. Cuerpo opcional para explicar qué y porqué

## Repo-level

- No CI, no pre-commit hooks. No `.env` files tracked (`.env.example` in each directory). Makefile en la raíz para comandos comunes (`make dev`, `make test`, `make lint`, etc.).
- Docs in `docs/architecture.md` (C4, stack, ADRs, NFRs) and `docs/database.md` (DER, data dictionary, RBAC).

## Environment variables

### Backend (`backend/.env`)

| Variable | Descripción |
|---|---|
| `SECRET_KEY` | Clave secreta de Django |
| `DEBUG` | Modo debug (True/False) |
| `DATABASE_URL` | URL de conexión a PostgreSQL |
| `ALLOWED_HOSTS` | Hosts permitidos (coma separada) |
| `CORS_ALLOWED_ORIGINS` | Orígenes CORS permitidos (coma separada) |

### Frontend (`frontend/.env`)

| Variable | Descripción | Default |
|---|---|---|
| `VITE_API_URL` | URL base de la API | `/api` |
| `VITE_DEMO_MODE` | Activar MSW mocks (demo) | `false` |

## Asesor Experto

Cuando el usuario plantee una funcionalidad, corrección o mejora sin especificar el **cómo**, actúa como **asesor experto en desarrollo de software** antes de escribir código:

1. **Analiza** el problema y el contexto del proyecto (stack, patrones existentes, arquitectura actual).
2. **Propón** 1–2 enfoques viables con sus trade-offs (ej: "Opción A: signals de Django es más simple pero menos explícito; Opción B: service layer es más testeable y sigue el patrón que ya usan en `vehiculos/").
3. **Recomienda** la opción que mejor se alinee con las convenciones del proyecto y mantenibilidad general.
4. **Advierte** si el enfoque que plantea el usuario (o incluso la opción recomendada) incurre en **malas prácticas** comunes del stack (ej: consultas N+1 en Django, mutación directa de props en Vue, lógica de negocio en vistas, etc.).
5. **Pregunta** al usuario si quiere proceder con la recomendación o prefiere otro enfoque.

> No aplica cuando el usuario ya indica explícitamente qué hacer y cómo hacerlo; en ese caso solo ejecuta. Tampoco apliques principios específicos como SOLID, DRY, KISS a menos que el usuario los mencione.

## Documentation rules

- **`docs/database.md`** is the source of truth for models, DER, business rules, and RBAC matrix. UPDATE whenever a model changes (new field, new app, new constraint).
- **`docs/architecture.md`** is the source of truth for C4 diagrams, stack versions, and ADRs. UPDATE when stack or architectural decisions change.
- **`CHANGELOG.md`** is version history. UPDATE on each meaningful change (new feature, breaking change, milestone).
- **README.md** must reflect current structure and commands. UPDATE when directory structure or dev workflow changes.

## Reglas de sanitización (nunca más)

Este es un producto de propósito general. Prohibido introducir vínculos a un cliente específico:

- **Sin marca institucional**: no incluir nombres, siglas, logotipos o unidades organizativas reales de ninguna empresa/organización. Usar placeholders neutros (`EnergyCompany`, `Client`, `DemoCo`).
- **Sin PII**: prohibido versionar cédulas, correos reales, teléfonos, placas/seriales reales ni inventarios reales. Identificadores de demo = series sintéticas (`SCF-1001`).
- **Geografías ficticias**: usar regiones genéricas (Norte/Sur/Este/Oeste/Central) o nombres inventados; nunca estados/ciudades reales de un cliente.
- **Solo mock data**: los datos de demostración (CSV, JSON, dumps, fixtures, MSW) deben ser ficticios y generados para el repo.
- **Sin secretos ni endpoints**: no versionar contraseñas, tokens, API keys, credenciales de BD ni URLs privadas. Únicamente CDNs públicos necesarios.
- **Copyright y localización neutros**: sin nombres personales salvo decisión del propietario; locales genéricos (`es`, `en`) y no atados a un país cliente.
- **Revisión pre-commit/PR**: correr un grep de referencia antes de commitear:
  ```bash
  grep -rniE "gob\.ve|@scf|corpoelec|\bSAP\b|\bCaraballo\b" --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=.venv .
  ```
  Si hay coincidencias (fuera de esta sección de reglas), sanitizar antes de commitear.
