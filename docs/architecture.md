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

## 3. Modelo de Datos

El DER, diccionario de datos, reglas de negocio y matriz RBAC se encuentran en [`docs/database.md`](database.md).

Documentación interactiva de la API: `/api/docs` (Swagger UI, generado por Django Ninja).

## 4. Decisiones Técnicas (ADRs)

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
