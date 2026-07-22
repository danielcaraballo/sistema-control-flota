# Changelog

## v0.11.0 — 2026-07-22

### Changed
- README reescrito: descripción factual, funcionalidades actuales sin roadmap, estructura movida a `docs/structure.md`
- CONTRIBUTING.md: documentado flujo GitHub Flow y proceso de releases
- docs/architecture.md: agregados ADR #11 (scope v1) y #12 (GitHub Flow); NFRs etiquetados como v2

### Removed
- `AGENTS.md` del control de versiones (`.gitignore` + `git rm --cached`)

### Docs
- Creado `docs/structure.md` con el árbol completo del proyecto

Tests: 121

## v0.10.0 — 2026-07-20

### Added
- `Vehiculo.porcentaje_completado` como propiedad calculada sobre 20 campos
- Campo de completitud en `VehiculoSchema` y `VehiculoListItemSchema`
- Knob de PrimeVue en detalle del vehículo con colores según rango (rojo <50%, amarillo 50-79%, verde ≥80%)
- Columna ordenable "Ficha" con Knob en lista de vehículos

Tests: 121

## v0.9.0 — 2026-07-16

### Removed
- `backend/seeds/` por completo (management command, loaders, JSONs)

### Docs
- `AGENTS.md`: removidas referencias a seed_data
- README: actualizado con opciones de población de BD

## v0.8.0 — 2026-07-08

### Added
- Paginación server-side en `GET /vehiculos/` con `limit`/`offset`
- Filtros server-side: `search`, `estado_id`, `estatus_id`, `gerencia_id`
- Índices compuestos en migración 0005: `(estatus_activo, estado_id)`, `(estatus_id)`, `(gerencia_id)`

### Changed
- DataTable convertido a modo `lazy` — carga solo la página actual desde el servidor
- Búsqueda con debounce de 350ms y filtros rápidos por Estado y Estatus

Tests: 18

## v0.7.0 — 2026-07-08

### Added
- FK de `CentroDeServicio` a `Estado` (no-nullable, on_delete=RESTRICT). Dropdown de Estado en CRUD frontend
- FK nullable de `TipoUso` en `Vehiculo`. Dropdown en formulario y display en detalle
- KPIs de vehículos en dashboard callback (`total_vehiculos`, `vehiculos_activos`)

### Changed
- Reportes cambiado de `ROL_ANALISTA` a `ROL_NACIONAL` (router + sidebar)
- String literal `'nacional'` reemplazado por constante `ROL_NACIONAL` en `VehiculosView.vue`

### Docs
- NFR-02 marcado con 🚧 para restricción de texto libre en taller

Tests: 113

## v0.6.2 — 2026-07-05

### Fixed
- Import dinámico inefectivo en `api.js`: reemplazado por import estático para eliminar warning `INEFFECTIVE_DYNAMIC_IMPORT` de Vite

### Docs
- Convención de commits (español, Conventional Commits) documentada en `AGENTS.md`

Tests: 113

## v0.6.1 — 2026-07-05

### Added
- Helpers compartidos en `utils/api_helpers.py`: `filter_activos`, `get_object_or_404`, `check_duplicate`, `check_duplicate_composite` (eliminan ~100 líneas duplicadas)
- `register_crud()` + `CrudConfig` en `utils/crud_factory.py` para generar endpoints CRUD de catálogos y organización (elimina ~435 líneas duplicadas)

### Changed
- `catalogos/api.py`: 531 → 78 líneas (9 entidades via factory)
- `organizacion/api.py`: 160 → 34 líneas (3 entidades via factory)
- Modelos migrados de `unique_together` a `UniqueConstraint(condition=Q(estatus_activo=True))` — permite reciclar nombres soft-deleteados sin IntegrityError
- `numero_economico` y `vin` mantienen `unique=True` (identificadores reales, únicos permanentemente)

Tests: 113

## v0.6.0 — 2026-07-05

### Added
- Frontend completo de vehículos: DataTable con filtros, formulario tipo stepper, vista detalle con QR y ficha técnica
- Backend: CRUD de vehículos con 17 campos, QR autogenerado, filtro por estado del usuario
- `EstatusVehiculo` y `ColorPlaca` como catálogos independientes
- Soporte de reactivación en `VehiculoUpdate` (estatus_activo)
- Admin: vehículos y estatus_vehiculo en Unfold sidebar

### Changed
- Hover en filas DataTable, dialogs sin scroll, stepper alineado a la izquierda

Tests: 154

## v0.5.2 — 2026-07-03

### Added
- Tema oscuro con tokens compuestos de PrimeVue Aura
- Variables SCF para `bg-card`/`border-card` adaptables a modo oscuro
- Flash prevention en `index.html`

## v0.5.1 — 2026-07-03

### Added
- Endpoint `POST /auth/change-password` con validación de contraseña actual
- `UserDropdown` (Popover) con theme switcher (claro/oscuro/sistema), cambio de contraseña y logout
- `useTheme.js` refactorizado para 3 modos con listener `matchMedia`
- Sidebar footer como trigger del dropdown con chevron animado

## v0.5.0 — 2026-07-02/03

### Added
- Modelo `CentroDeServicio` con CRUD completo y admin Unfold
- Auto-refresh token con serialización de peticiones concurrentes
- Login con FloatLabel, validación cliente, redirect post-login
- Skeleton loading para eliminar parpadeo en catálogos
- Botón "Agregar" estandarizado en todos los CRUDs

### Fixed
- Race condition en startup: auth initialization await

### Changed
- Sidebar separa Usuarios/Organización/Catálogos bajo sección "Administración"

## v0.4.0 — 2026-07-02

### Added
- Nueva app `catalogos` con 7 modelos: Marca, Modelo, TipoVehiculo, TipoUso, Color, SistemaAfectado, TipoFalla
- CRUD API con soft-delete y filtro `?incluir_inactivos=true`
- `CatalogoTabContent.vue`: componente reutilizable para CRUD de catálogos
- `CatalogosView` con TabView de 7 pestañas

Tests: 35

## v0.3.0 — 2026-06-20/22

### Added
- Integración django-unfold con dashboard de KPIs y charts
- CRUD completo de usuarios con reset de contraseña
- Endpoint `POST /usuarios/{id}/reset-password`

Tests: 31

## v0.2.0 — 2026-06-18/20

### Added
- Migración a django-ninja-jwt (JWTAuth, RefreshToken)
- dj-database-url en vez de parsing manual de `DATABASE_URL`
- Migración a uv + ruff (reemplaza pip + flake8 + black)

### Docs
- `docs/architecture.md` con C4, DER, APIs, ADRs
- README con badges, estructura, tabla de features
- ESLint + Prettier config en frontend

Tests: 16

## v0.1.1 — 2026-06-17

### Added
- Integración PrimeVue 4 con tema Aura
- Migración de vistas a DataTable, Card, Dialog, etc.
- Fuente Poppins (Google Fonts) con override en componentes

## v0.1.0 — 2026-06-17

### Added
- Setup Django 5.2 + Ninja + Vue 3 + Vite
- Modelos: Estado, Gerencia, Usuario (AbstractUser con roles)
- Autenticación JWT: login, refresh, me
- CRUD de usuarios con permisos por rol
- Sidebar dinámico según rol del usuario
- LoginView, UsuariosView, DashboardView (skeleton)

---

**Tests acumulados:** 121 · **Linter:** 0 warnings (Ruff)
