# Arquitectura del Sistema — SCF

## 1. Diagrama de Contexto (C1)

```mermaid
graph TD
    Mecanico["Mecánico (Tablet PWA)"] -->|Escanea QR, registra diagnóstico| SCF["SCF - Sistema de Control de Flota"]
    Analista["Analista Nacional"] -->|Cotiza órdenes| SCF
    Gerente["Gerente / Admin Nacional"] -->|Dashboard, reportes, gestión| SCF
    SCF -->|Almacena datos| DB[("PostgreSQL")]
    SCF -->|Autenticación JWT| Auth[JWT Tokens]
```

## 2. Diagrama de Contenedores (C2)

```mermaid
graph LR
    subgraph "Cliente Web (PWA)"
        Vue[Vue 3 + Vite]
        PWA[Service Worker]
        Pinia[Pinia Store]
    end
    subgraph "Servidor API"
        Django[Django 5.2]
        Ninja[Ninja API]
        JWT[JWTAuth]
    end
    subgraph "Base de Datos"
        PG[(PostgreSQL)]
    end

    Vue -->|HTTP/JSON| Ninja
    Ninja --> JWT
    Ninja --> Django
    Django --> PG
    PWA -->|Cache offline| Vue
    Pinia -->|Estado reactivo| Vue
```

### Stack Tecnológico

| Capa | Tecnología | Versión |
|---|---|---|
| Backend | Python / Django + Ninja | 3.11+ / 5.2 |
| Autenticación | django-ninja-jwt | 5.4.4 |
| Frontend | Vue 3 + Pinia + Vue Router | 3.5 / 3.0 / 5.1 |
| UI | PrimeVue 4 + PrimeIcons | 4.5 / 7.0 |
| PWA | vite-plugin-pwa | 1.3 |
| BD Producción | PostgreSQL | 15+ |
| BD Desarrollo | SQLite (fallback) | — |
| Linting | Ruff (backend) + ESLint/Prettier (frontend) | — |

## 3. Diagrama Entidad-Relación (DER)

### 3.1 Modelo Actual

```mermaid
erDiagram
    ESTADO ||--o{ USUARIO : ""
    GERENCIA ||--o{ USUARIO : pertenece

    ESTADO {
        int id PK
        string nombre UK
        bool estatus_activo
    }

    GERENCIA {
        int id PK
        string nombre UK
        bool estatus_activo
    }

    USUARIO {
        int id PK
        string username UK
        string email UK
        string password
        string first_name
        string last_name
        string rol "gerente_nacional | analista_nacional | responsable_estatal | mecanico"
        int gerencia_id FK
        int estado_id FK
        bool is_active
    }
```

### 3.2 Modelo Completo (Actual + Planificado)

```mermaid
erDiagram
    ESTADO ||--o{ USUARIO : ""
    GERENCIA ||--o{ USUARIO : pertenece
    GERENCIA ||--o{ VEHICULO : posee
    CATEGORIA_VEHICULO ||--o{ VEHICULO : clasifica
    MARCA ||--o{ VEHICULO : ""
    VEHICULO ||--o{ ORDEN_SERVICIO : recibe
    ORDEN_SERVICIO ||--o{ DETALLE_ORDEN : contiene
    TIPO_FALLA ||--o{ DETALLE_ORDEN : clasifica
    USUARIO ||--o{ ORDEN_SERVICIO : "crea | aprueba"

    ESTADO {
        int id PK
        string nombre UK
        bool estatus_activo
    }

    GERENCIA {
        int id PK
        string nombre UK
        bool estatus_activo
    }

    USUARIO {
        int id PK
        string username UK
        string email UK
        string password
        string first_name
        string last_name
        string rol
        int gerencia_id FK
        int estado_id FK
        bool is_active
    }

    VEHICULO {
        int id PK
        string numero_economico UK
        string vin UK
        string placa
        string estatus "OPERATIVO | EN_TALLER | INACTIVO"
        int kilometraje_actual
        int gerencia_id FK
        int categoria_id FK
        int marca_id FK
    }

    ORDEN_SERVICIO {
        int id PK
        int vehiculo_id FK
        int mecanico_creador_id FK
        int aprobador_id FK
        string estatus_orden "DIAGNOSTICO | REVISADO | APROBADO | FINALIZADO"
        decimal costo_estimado
        datetime fecha_ingreso
    }

    DETALLE_ORDEN {
        int id PK
        int orden_servicio_id FK
        int tipo_falla_id FK
        string comentario_extra
    }

    MARCA {
        int id PK
        string nombre UK
        bool estatus_activo
    }

    CATEGORIA_VEHICULO {
        int id PK
        string nombre UK
        int km_alerta_preventivo
        int meses_alerta_preventivo
    }

    TIPO_FALLA {
        int id PK
        string descripcion UK
        string sistema_afectado
    }
```

### 3.3 Estatus de Implementación

| Entidad | Estado | App |
|---|---|---|
| `Estado` | ✅ Implementado | organizacion |
| `Gerencia` | ✅ Implementado | organizacion |
| `Usuario` | ✅ Implementado | usuarios |
| `Vehiculo` | 🚧 Planificado | — |
| `OrdenServicio` | 🚧 Planificado | — |
| `DetalleOrden` | 🚧 Planificado | — |
| `Marca` | 🚧 Planificado | — |
| `CategoriaVehiculo` | 🚧 Planificado | — |
| `TipoFalla` | 🚧 Planificado | — |

## 4. APIs

| Ruta | Método | Descripción | Auth |
|---|---|---|---|
| `/api/auth/login` | POST | Inicio de sesión (username o email) | None |
| `/api/auth/refresh` | POST | Renovar access token | None |
| `/api/auth/me` | GET | Perfil del usuario autenticado | JWT |
| `/api/usuarios/` | GET | Listar usuarios | JWT + gerente_nacional |
| `/api/usuarios/` | POST | Crear usuario | JWT + gerente_nacional |
| `/api/usuarios/{id}` | PUT | Actualizar usuario | JWT + gerente_nacional |
| `/api/usuarios/{id}` | DELETE | Desactivar usuario | JWT + gerente_nacional |
| `/api/organizacion/estados/` | GET | Listar estados activos | JWT |
| `/api/organizacion/gerencias/` | GET | Listar gerencias activas | JWT |

Documentación interactiva: `/api/docs` (Swagger UI, generado por Django Ninja).

## 5. Decisiones Técnicas (ADRs)

| # | Decisión | Opciones | Elegido | Contexto |
|---|---|---|---|---|
| 1 | Framework API | DRF vs **Django Ninja** | Django Ninja | Tipado nativo con Pydantic, OpenAPI automático, mejor rendimiento |
| 2 | Autenticación JWT | Custom vs **django-ninja-jwt** | django-ninja-jwt | Elimina código manual de JWT, refresh tokens, mantenido oficialmente |
| 3 | Config BD | Regex manual vs **dj-database-url** | dj-database-url | Estandariza el parsing de DATABASE_URL, menos propenso a errores |
| 4 | Frontend Framework | Options API vs **Composition API** | Composition API | Mejor tree-shaking, reutilización de lógica con composables |
| 5 | UI Components | Bootstrap vs **PrimeVue** | PrimeVue | Componentes específicos para DataTable, menús, formularios corporativos |
| 6 | Estado Global | Vuex vs **Pinia** | Pinia | Oficial para Vue 3, mejor soporte TypeScript, setup stores |
| 7 | Linting Backend | flake8 + black vs **Ruff** | Ruff | 10-100x más rápido, unifica lint + formato, compatible con pyproject.toml |
| 8 | Gestión de Dependencias | pip + requirements.txt vs **uv** | uv | Resolución 10-100x más rápida, lockfile determinista (`uv.lock`) |
