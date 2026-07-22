# Sistema de Diseño — SCF

## Tipografía

### Familia

| Rol | Familia | Origen |
|---|---|---|
| **Sans-serif (principal)** | `'Poppins', sans-serif` | Google Fonts (wght 300–700) |
| **Monoespaciada** | `'JetBrains Mono', 'Fira Code', 'Cascadia Code', ui-monospace, SFMono-Regular, monospace` | Tailwind `font-mono` |

### Jerarquía

| Elemento | Clase Tailwind | Tamaño | Peso |
|---|---|---|---|
| Page title (h1) | `text-2xl` | 24px / 1.5rem | `font-semibold` |
| Page header icon | `text-xl` | 20px / 1.25rem | — |
| Section heading (h2) | `text-lg` | 18px / 1.125rem | `font-semibold` |
| KPI value | `text-xl` | 20px / 1.25rem | `font-bold` |
| Tabla de catálogos (DataTable small) | `text-sm` | 14px / 0.875rem | — |
| Form labels | `text-sm` | 14px / 0.875rem | `font-semibold` |
| Body / table content | `text-sm` | 14px / 0.875rem | `font-medium` en valores |
| Botones principales | `text-sm` (default) | 14px / 0.875rem | — |
| Botones de acción (tabla) | `text-sm` (small) | 12px / 0.75rem | — |
| Secondary / muted | `text-xs` | 12px / 0.75rem | — |
| Validation errors | `text-xs` | 12px / 0.75rem | — |
| KPI label / trend | `text-xs` | 12px / 0.75rem | `font-semibold` |
| Empty state icon | `text-4xl` | 36px / 2.25rem | — |
| Empty state text | `text-sm` | 14px / 0.875rem | `font-medium` |
| Login heading | `text-2xl` | 24px / 1.5rem | `font-bold` |

## Componentes

### DataTable

| Prop | Valor |
|---|---|
| `size` | `"small"` |
| `scrollHeight` | `"flex"` |
| `stripedRows` | `true` |
| `paginator` | `true` |
| `rows` | `10` |
| `rowsPerPageOptions` | `[10, 25, 50]` |

### Botones

| Contexto | `size` | Uso |
|---|---|---|
| Acción principal (Agregar, Guardar, Crear, Iniciar sesión) | default (`"normal"`) | Botones con label + icon |
| Acción secundaria (Cancelar) | default | `severity="secondary"` |
| Acciones de fila en tabla (editar, desactivar, reactivar) | `"small"` | `text` + `rounded` |
| Limpiar filtros | `"small"` | `variant="text"` |

### Inputs

| Contexto | `size` | Uso |
|---|---|---|
| Búsqueda en tabla (InputText) | `"small"` | Dentro de `IconField` |
| Filtros (Select) | `"small"` | `class="w-40"` + `size="small"` |
| Formularios en Dialog (InputText) | default | `class="w-full"` |

### Diálogos (Dialog)

| Propósito | Ancho | Alto |
|---|---|---|
| CRUD catálogos | `min(450px, calc(100vw - 2rem))` | auto |
| Usuario (crear) | `550px` | auto |
| Vehículo (crear/editar) | `780px` | `580px` |
| Confirmación | `ConfirmDialog` component | auto |

### Tags

- Usar `class="!text-xs"` para Tags dentro de DataTable.
- Severities según semántica: `success`, `info`, `warn`, `danger`, `secondary`.

## Paleta de colores

### Primario (Sky)

```css
--p-primary-50:  {sky.50}
--p-primary-100: {sky.100}
/* ... hasta */
--p-primary-950: {sky.950}
```

### Superficie (Slate)

```css
--p-surface-50:  {slate.50}
--p-surface-100: {slate.100}
/* ... hasta */
--p-surface-950: {slate.950}
```

### Semánticos

| Uso | Clase |
|---|---|
| Éxito / Activo | `success` (green) |
| Advertencia | `warn` (orange) |
| Peligro / Inactivo | `danger` (red) |
| Información | `info` (cyan/blue) |
| Secundario | `secondary` |

## Spacing

| Contexto | Clase |
|---|---|
| Page header bottom | `mb-6` |
| Card padding | `p-5` |
| DataTable wrapper | `border border-card-border rounded-md bg-card` |
| Gap entre botones de acción | `gap-2` |
| Gap entre icono y label | `gap-2` |

## Temas

- **Modo oscuro**: clase `.p-dark` en `<html>`, manejado por `useTheme.js`.
- **Fondo de página**:
  - Light: `var(--p-surface-50)`
  - Dark: `var(--p-surface-950)`
- **Cards**: `var(--p-content-background)` con borde `var(--p-content-border-color)`.
- **Sidebar**: ancho `260px`, colapsado `64px`, z-index `100`.

## Convenciones

1. **No usar valores arbitrarios de font-size** (`text-[...]`). Usar siempre tokens de Tailwind.
2. **No usar inline `font-family`** en templates. Usar `font-sans` (Poppins global) o `font-mono`.
3. **No usar inline `font-weight`** salvo que sea dinámico (ej. `CompletitudKnob` fontSize).
4. **Form labels**: siempre `text-sm font-semibold`.
5. **Validation errors**: siempre `text-xs text-red-500 dark:text-red-400` (o `!text-xs` en Message).
6. **Empty states**: `text-4xl` icon + `text-sm font-medium` text.
7. **DataTable**: usar `size="small"` y `scrollHeight="flex"` siempre.
8. **Filtros y búsqueda**: usar `size="small"` en InputText y Select.
9. **Botones de acción en tabla**: usar `size="small"` con `text` + `rounded`.
