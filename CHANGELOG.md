# Changelog

## v0.6.0 — Frontend Vehículos + CRUD completo (2026-07-05)

- Frontend completo de vehículos: DataTable con filtros, stepper vertical de 4 pasos para crear/editar, vista detalle con QR y ficha técnica
- Backend: Vehiculo CRUD con 17 campos, QR autogenerado, filtro por estado del usuario
- EstatusVehiculo y ColorPlaca como catálogos independientes
- VehiculoUpdate soporta reactivación (estatus_activo)
- Hover en filas DataTable, dialogs sin scroll, stepper alineado a la izquierda
- Admin: vehículos y estatus_vehiculo en Unfold sidebar
- 154 tests

## v0.5.2 — Dark mode homogéneo (2026-07-03)

- Tema oscuro con tokens compuestos de PrimeVue Aura (--p-content-background, etc.)
- Variables SCF para bg-card/border-card adaptables a modo oscuro
- Flash prevention en index.html

## v0.5.1 — UserDropdown + cambio de contraseña (2026-07-03)

- POST /auth/change-password con validación de contraseña actual
- UserDropdown (Popover) con theme switcher (claro/oscuro/sistema), cambio de contraseña y logout
- useTheme.js refactorizado para 3 modos con listener matchMedia
- Sidebar footer como trigger del dropdown con chevron animado

## v0.5.0 — CentroDeServicio + Login mejorado (2026-07-02/03)

- Modelo CentroDeServicio con CRUD completo + admin Unfold
- Sidebar separa Usuarios/Organización/Catálogos bajo "Administración"
- Fix race condition en startup: auth initialization await
- Auto-refresh token: serialización de peticiones concurrentes
- Login con FloatLabel, validación cliente, redirect post-login
- Eliminación de parpadeo en catálogos con Skeleton loading
- Estandarización de botón "Agregar" en CRUDs
- Dashboard sin mock data

## v0.4.0 — Catálogos (tablas maestras) (2026-07-02)

- Nueva app `catalogos` con 7 modelos: Marca, Modelo, TipoVehiculo, TipoUso, Color, SistemaAfectado, TipoFalla
- CRUD API con soft-delete y filtro `?incluir_inactivos=true`
- `CatalogoTabContent.vue`: componente reutilizable para CRUD de catálogos
- CatalogosView con TabView de 7 pestañas
- Seed data: 15 marcas, ~45 modelos, 10 colores, 12 tipos vehículo, 5 usos, 15 fallas, 9 sistemas
- 35 tests

## v0.3.0 — Unfold admin + usuarios completo (2026-06-20/22)

- Integración django-unfold con dashboard de KPIs/charts
- CRUD completo de usuarios con reset de contraseña
- Endpoint POST /usuarios/{id}/reset-password
- 31 tests

## v0.2.0 — JWT estándar + tests + documentación (2026-06-18/20)

- Migración a django-ninja-jwt (JWTAuth, RefreshToken)
- dj-database-url en vez de parsing manual
- Migración a uv + ruff (reemplaza pip + flake8 + black)
- docs/architecture.md con C4, DER, APIs, ADRs
- README con badges, estructura, tabla de features
- ESLint + Prettier config en frontend
- 16 tests

## v0.1.1 — PrimeVue + Poppins (2026-06-17)

- Integración PrimeVue 4 con tema Aura
- Migración de vistas a DataTable, Card, Dialog, etc.
- Fuente Poppins (Google Fonts) con override en componentes

## v0.1.0 — Setup inicial + RBAC (2026-06-17)

- Setup Django 5.2 + Ninja + Vue 3 + Vite
- Modelos: Estado, Gerencia, Usuario (AbstractUser con roles)
- JWT auth: login, refresh, me (custom, antes de django-ninja-jwt)
- CRUD de usuarios con permisos por rol
- Sidebar dinámico según rol del usuario
- LoginView, UsuariosView, DashboardView (skeleton)
