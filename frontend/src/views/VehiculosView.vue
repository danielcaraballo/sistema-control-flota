<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { placaSeverity, estatusSeverity } from '@/utils/vehiculo'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import { ROL_NACIONAL } from '@/utils/roles'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'
import Button from 'primevue/button'
import Column from 'primevue/column'
import DataTable from 'primevue/datatable'
import Dialog from 'primevue/dialog'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import InputText from 'primevue/inputtext'
import Menu from 'primevue/menu'
import Message from 'primevue/message'
import Tag from 'primevue/tag'
import Skeleton from 'primevue/skeleton'
import Select from 'primevue/select'
import CompletitudKnob from '@/components/CompletitudKnob.vue'
import ConfirmDialog from '@/components/ConfirmDialog.vue'
import PageHeader from '@/components/PageHeader.vue'
import VehiculoFormStepper from '@/components/vehiculo/VehiculoFormStepper.vue'

const toast = useToast()
const auth = useAuthStore()
const route = useRoute()
const router = useRouter()

const vehiculos = ref([])
const marcas = ref([])
const modelos = ref([])
const tiposVehiculo = ref([])
const colores = ref([])
const coloresPlaca = ref([])
const tiposUso = ref([])
const estatusVehiculo = ref([])
const estados = ref([])
const gerencias = ref([])
const centrosServicio = ref([])
const clasesVehiculo = ref([])
const tiposCombustible = ref([])

const loading = ref(true)
const skeletonRows = computed(() => (loading.value ? [...Array(10)] : []))
const saving = ref(false)
const showDialog = ref(false)
const editingVehiculo = ref(null)
const submitted = ref(false)
const errorMessage = ref('')
const activeIndex = ref(0)
const catalogosCargados = ref(false)
const showConfirmClose = ref(false)
const formSnapshot = ref(null)

// Server-side pagination state
const totalRecords = ref(0)
const first = ref(0)
const rows = ref(10)
const searchQuery = ref('')
const searchDebounce = ref(null)
const filterEstadoId = ref(null)
const filterEstatusId = ref(null)
const sortField = ref('numero_economico')
const sortOrder = ref(1)

const formModificado = computed(() => {
  if (!formSnapshot.value) return false
  return JSON.stringify(form.value) !== JSON.stringify(formSnapshot.value)
})

const initialForm = () => ({
  numero_economico: '',
  vin: '',
  placa: '',
  color_placa_id: null,
  placa_intt: '',
  serial_motor: '',
  numero_unidad: '',
  categoria_id: null,
  marca_id: null,
  modelo_id: null,
  anio: null,
  color_id: null,
  tipo_uso_id: null,
  estatus_id: null,
  estado_id: null,
  gerencia_id: null,
  unidad_usuaria_id: null,
  emplazamiento_id: null,
  clase_id: null,
  tipo_combustible_id: null,
})

const form = ref(initialForm())

const isCreating = computed(() => !editingVehiculo.value)

const exportando = ref(false)
const exportMenu = ref(null)
const exportBtnRef = ref(null)
const exportBtnWidth = ref(140)

const exportMenuItems = [
  { label: 'CSV', command: () => exportarVehiculos('csv') },
  { label: 'XLSX', command: () => exportarVehiculos('xlsx') },
]

function toggleExportMenu(event) {
  exportMenu.value.toggle(event)
}

async function loadCatalogos() {
  const calls = [
    api
      .get('/catalogos/marcas/')
      .then((r) => {
        marcas.value = r.data
      })
      .catch(() => {}),
    api
      .get('/catalogos/modelos/')
      .then((r) => {
        modelos.value = r.data
      })
      .catch(() => {}),
    api
      .get('/catalogos/tipos-vehiculo/')
      .then((r) => {
        tiposVehiculo.value = r.data
      })
      .catch(() => {}),
    api
      .get('/catalogos/colores/')
      .then((r) => {
        colores.value = r.data
      })
      .catch(() => {}),
    api
      .get('/catalogos/colores-placa/')
      .then((r) => {
        coloresPlaca.value = r.data
      })
      .catch(() => {}),
    api
      .get('/catalogos/tipos-uso/')
      .then((r) => {
        tiposUso.value = r.data
      })
      .catch(() => {}),
    api
      .get('/catalogos/estatus-vehiculo/')
      .then((r) => {
        estatusVehiculo.value = r.data
      })
      .catch(() => {}),
    api
      .get('/organizacion/estados/')
      .then((r) => {
        estados.value = r.data
      })
      .catch(() => {}),
    api
      .get('/organizacion/gerencias/')
      .then((r) => {
        gerencias.value = r.data
      })
      .catch(() => {}),
    api
      .get('/organizacion/centros-servicio/')
      .then((r) => {
        centrosServicio.value = r.data
      })
      .catch(() => {}),
    api
      .get('/catalogos/clases-vehiculo/')
      .then((r) => {
        clasesVehiculo.value = r.data
      })
      .catch(() => {}),
    api
      .get('/catalogos/tipos-combustible/')
      .then((r) => {
        tiposCombustible.value = r.data
      })
      .catch(() => {}),
  ]
  await Promise.allSettled(calls)
}

async function loadVehiculos() {
  loading.value = true
  try {
    const params = new URLSearchParams()
    params.set('limit', String(rows.value))
    params.set('offset', String(first.value))
    params.set('sort_by', sortField.value)
    params.set('sort_order', sortOrder.value === 1 ? 'asc' : 'desc')
    if (searchQuery.value) params.set('search', searchQuery.value)
    if (filterEstadoId.value) params.set('estado_id', String(filterEstadoId.value))
    if (filterEstatusId.value) params.set('estatus_id', String(filterEstatusId.value))
    if (auth.tieneRol(ROL_NACIONAL)) params.set('incluir_inactivos', 'true')

    const { data } = await api.get('/vehiculos/?' + params.toString())
    vehiculos.value = data.items
    totalRecords.value = data.count
  } catch (err) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: err.response?.data?.detail || 'Error al cargar vehículos',
      life: 4000,
    })
  } finally {
    loading.value = false
  }
}

function onPage(event) {
  first.value = event.first
  rows.value = event.rows
  loadVehiculos()
}

function onSort(event) {
  sortField.value = event.sortField
  sortOrder.value = event.sortOrder
  first.value = 0
  loadVehiculos()
}

function onSearchInput(value) {
  if (searchDebounce.value) clearTimeout(searchDebounce.value)
  searchDebounce.value = setTimeout(() => {
    searchQuery.value = value
    first.value = 0
    loadVehiculos()
  }, 350)
}

function onFilterChange() {
  first.value = 0
  loadVehiculos()
}

function limpiarFiltros() {
  searchQuery.value = ''
  filterEstadoId.value = null
  filterEstatusId.value = null
  first.value = 0
  loadVehiculos()
}

async function exportarVehiculos(formato) {
  if (exportando.value) return
  exportando.value = true

  const params = new URLSearchParams()
  params.set('formato', formato)
  if (searchQuery.value) params.set('search', searchQuery.value)
  if (filterEstadoId.value) params.set('estado_id', String(filterEstadoId.value))
  if (filterEstatusId.value) params.set('estatus_id', String(filterEstatusId.value))
  if (auth.tieneRol(ROL_NACIONAL)) params.set('incluir_inactivos', 'true')

  try {
    const res = await api.get('/vehiculos/exportar?' + params.toString(), {
      responseType: 'blob',
    })
    const blob = new Blob([res.data])
    const filename = `vehiculos_${new Date().toISOString().slice(0, 10)}.${formato}`
    const sizeKB = (blob.size / 1024).toFixed(1)
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    a.click()
    URL.revokeObjectURL(url)

    toast.add({
      severity: 'success',
      summary: 'Exportación completada',
      detail: `${filename} — ${sizeKB} KB`,
      life: 4000,
    })
  } catch {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'No se pudo exportar el inventario',
      life: 4000,
    })
  } finally {
    exportando.value = false
  }
}

async function ensureCatalogos() {
  if (catalogosCargados.value) return
  await loadCatalogos()
  catalogosCargados.value = true
}

async function openNew() {
  editingVehiculo.value = null
  errorMessage.value = ''
  activeIndex.value = 0
  saving.value = false
  form.value = initialForm()
  formSnapshot.value = JSON.parse(JSON.stringify(form.value))
  submitted.value = false
  await ensureCatalogos()
  showDialog.value = true
}

async function openEdit(vehiculo) {
  editingVehiculo.value = vehiculo
  errorMessage.value = ''
  activeIndex.value = 0
  form.value = {
    numero_economico: vehiculo.numero_economico,
    vin: vehiculo.vin,
    placa: vehiculo.placa ?? '',
    color_placa_id: vehiculo.color_placa ?? null,
    placa_intt: vehiculo.placa_intt,
    serial_motor: vehiculo.serial_motor,
    numero_unidad: vehiculo.numero_unidad ?? '',
    categoria_id: vehiculo.categoria,
    marca_id: vehiculo.marca,
    modelo_id: vehiculo.modelo,
    anio: vehiculo.anio,
    color_id: vehiculo.color ?? null,
    tipo_uso_id: vehiculo.tipo_uso ?? null,
    estatus_id: vehiculo.estatus,
    estado_id: vehiculo.estado,
    gerencia_id: vehiculo.gerencia,
    unidad_usuaria_id: vehiculo.unidad_usuaria ?? null,
    emplazamiento_id: vehiculo.emplazamiento,
    clase_id: vehiculo.clase,
    tipo_combustible_id: vehiculo.tipo_combustible,
  }
  formSnapshot.value = JSON.parse(JSON.stringify(form.value))
  submitted.value = false
  await ensureCatalogos()
  showDialog.value = true
}

function validarFormulario(f) {
  const required = [
    ['numero_economico', 'El número económico es requerido'],
    ['vin', 'El serial de carrocería es requerido'],
    ['categoria_id', 'La categoría es requerida'],
    ['clase_id', 'La clase es requerida'],
    ['tipo_combustible_id', 'El tipo de combustible es requerido'],
    ['marca_id', 'La marca es requerida'],
    ['modelo_id', 'El modelo es requerido'],
    ['anio', 'El año es requerido'],
    ['estatus_id', 'El estatus es requerido'],
    ['estado_id', 'El estado es requerido'],
    ['gerencia_id', 'La gerencia es requerida'],
    ['emplazamiento_id', 'El emplazamiento es requerido'],
  ]
  for (const [field, msg] of required) {
    if (!f[field]) return msg
  }
  return null
}

async function saveVehiculo() {
  submitted.value = true
  saving.value = true
  errorMessage.value = ''

  const error = validarFormulario(form.value)
  if (error) {
    errorMessage.value = error
    saving.value = false
    return
  }

  const payload = {
    numero_economico: form.value.numero_economico,
    vin: form.value.vin,
    placa: form.value.placa || null,
    color_placa_id: form.value.color_placa_id,
    placa_intt: form.value.placa_intt || '',
    serial_motor: form.value.serial_motor || '',
    numero_unidad: form.value.numero_unidad || null,
    categoria_id: form.value.categoria_id,
    marca_id: form.value.marca_id,
    modelo_id: form.value.modelo_id,
    anio: form.value.anio,
    color_id: form.value.color_id,
    tipo_uso_id: form.value.tipo_uso_id || null,
    estatus_id: form.value.estatus_id,
    estado_id: form.value.estado_id,
    gerencia_id: form.value.gerencia_id,
    unidad_usuaria_id: form.value.unidad_usuaria_id || null,
    emplazamiento_id: form.value.emplazamiento_id,
    clase_id: form.value.clase_id,
    tipo_combustible_id: form.value.tipo_combustible_id,
  }

  try {
    const { data } = isCreating.value
      ? await api.post('/vehiculos/', payload)
      : await api.put(`/vehiculos/${editingVehiculo.value.id}`, payload)
    showDialog.value = false
    toast.add({
      severity: 'success',
      summary: isCreating.value ? 'Vehículo creado' : 'Vehículo actualizado',
      detail: `${data.numero_economico} — ${data.marca_nombre} ${data.modelo_nombre}`,
      life: 4000,
    })
    await loadVehiculos()
    if (isCreating.value) {
      router.push({ name: 'vehiculo-detalle', params: { id: data.id } })
    }
  } catch (err) {
    const data = err.response?.data
    errorMessage.value = Array.isArray(data)
      ? data.map((e) => e.msg).join('; ')
      : data?.detail || 'Error al guardar el vehículo'
  } finally {
    saving.value = false
  }
}

function verDetalle(v) {
  router.push({ name: 'vehiculo-detalle', params: { id: v.id } })
}

async function loadVehiculoForEdit(id) {
  try {
    const { data } = await api.get(`/vehiculos/${id}`)
    openEdit(data)
  } catch {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'No se pudo cargar el vehículo',
      life: 4000,
    })
  }
}

function onCancelarClick() {
  if (formModificado.value) {
    showConfirmClose.value = true
  } else {
    showDialog.value = false
  }
}

function cerrarDialog() {
  showConfirmClose.value = false
  showDialog.value = false
  formSnapshot.value = null
}

function onDialogClose(val) {
  if (val) return
  if (!showDialog.value) return
  if (formModificado.value) {
    showConfirmClose.value = true
  } else {
    showDialog.value = false
  }
}

async function loadCatalogoFiltros() {
  const calls = [
    api
      .get('/catalogos/estatus-vehiculo/')
      .then((r) => {
        estatusVehiculo.value = r.data
      })
      .catch(() => {}),
    api
      .get('/organizacion/estados/')
      .then((r) => {
        estados.value = r.data
      })
      .catch(() => {}),
  ]
  await Promise.allSettled(calls)
}

onMounted(async () => {
  await Promise.all([loadVehiculos(), loadCatalogoFiltros()])
  nextTick(() => {
    exportBtnWidth.value = exportBtnRef.value?.$el?.offsetWidth ?? 140
  })
  if (route.query.editar) {
    await loadVehiculoForEdit(route.query.editar)
  }
})
</script>

<template>
  <div class="w-full">
    <PageHeader
      title="Vehículos"
      subtitle="Gestión del inventario vehicular corporativo"
      icon="pi pi-truck"
    />

    <div class="border border-card-border rounded-md bg-card">
      <!-- Skeleton table during initial load -->
      <DataTable
        v-if="loading && vehiculos.length === 0"
        :value="skeletonRows"
        scrollable
        scrollHeight="flex"
        stripedRows
        :pt="{ pcPaginator: { class: 'opacity-0 pointer-events-none' } }"
      >
        <Column header="N° Económico">
          <template #body><Skeleton width="80%" height="1.25rem" /></template>
        </Column>
        <Column header="Placa">
          <template #body><Skeleton width="70%" height="1.25rem" /></template>
        </Column>
        <Column header="Marca / Modelo">
          <template #body><Skeleton width="60%" height="1.25rem" /></template>
        </Column>
        <Column header="Año">
          <template #body><Skeleton width="40%" height="1.25rem" /></template>
        </Column>
        <Column header="Estatus">
          <template #body><Skeleton width="5rem" height="1.5rem" borderRadius="6px" /></template>
        </Column>
        <Column header="Estado">
          <template #body><Skeleton width="65%" height="1.25rem" /></template>
        </Column>
        <Column header="Ficha">
          <template #body>
            <div class="flex justify-center">
              <Skeleton shape="circle" size="2.5rem" />
            </div>
          </template>
        </Column>
      </DataTable>

      <DataTable
        v-else
        :value="vehiculos"
        lazy
        :totalRecords="totalRecords"
        :first="first"
        :rows="rows"
        :loading="loading"
        :rowsPerPageOptions="[10, 25, 50]"
        scrollable
        scrollHeight="flex"
        stripedRows
        paginator
        @page="onPage"
        @sort="onSort"
        @row-click="verDetalle($event.data)"
        :pt="{
          bodyRow: ({ context }) => ({
            tabindex: '0',
            onKeydown: (event) => {
              if (event.key === 'Enter' && vehiculos[context.index]) {
                verDetalle(vehiculos[context.index])
              }
            },
          }),
          pcPaginator: {
            class: loading ? 'opacity-0 pointer-events-none' : '',
          },
        }"
      >
        <template #header>
          <div class="flex justify-between items-center gap-2 flex-wrap">
            <div class="flex items-center gap-2 flex-wrap">
              <IconField>
                <InputIcon class="pi pi-search" />
                <InputText
                  :modelValue="searchQuery"
                  @update:modelValue="onSearchInput"
                  placeholder="Buscar..."
                />
              </IconField>
              <Select
                v-model="filterEstadoId"
                :options="estados"
                optionValue="id"
                optionLabel="nombre"
                placeholder="Estado"
                class="w-40"
                clearable
                @update:modelValue="onFilterChange"
              />
              <Select
                v-model="filterEstatusId"
                :options="estatusVehiculo"
                optionValue="id"
                optionLabel="nombre"
                placeholder="Estatus"
                class="w-40"
                clearable
                @update:modelValue="onFilterChange"
              />
              <Button
                v-if="searchQuery || filterEstadoId || filterEstatusId"
                icon="pi pi-times"
                severity="secondary"
                variant="text"
                @click="limpiarFiltros"
                v-tooltip.top="'Limpiar filtros'"
              />
            </div>
            <div class="flex items-center gap-2">
              <Button
                v-if="auth.tieneRol(ROL_NACIONAL)"
                label="Agregar vehículo"
                icon="pi pi-plus"
                @click="openNew"
              />
              <Button
                ref="exportBtnRef"
                label="Exportar"
                icon="pi pi-download"
                iconPos="right"
                :loading="exportando"
                :disabled="exportando"
                @click="toggleExportMenu"
              />
              <Menu
                ref="exportMenu"
                :model="exportMenuItems"
                :popup="true"
                :pt="{ root: { style: `min-width: ${exportBtnWidth}px` } }"
              />
            </div>
          </div>
        </template>
        <template #empty>
          <div class="flex flex-col items-center justify-center py-12 text-muted-color">
            <i class="pi pi-truck text-4xl mb-3 opacity-40" />
            <p class="text-sm font-medium">No hay registros</p>
          </div>
        </template>

        <Column field="numero_economico" header="N° Económico" sortable />
        <Column field="placa" header="Placa" sortable>
          <template #body="{ data }">
            <div class="flex items-center gap-2">
              <span>{{ data.placa || '—' }}</span>
              <Tag
                v-if="data.color_placa_nombre"
                :value="data.color_placa_nombre"
                :severity="placaSeverity(data.color_placa_nombre)"
                class="!text-xs"
              />
            </div>
          </template>
        </Column>
        <Column field="marca_nombre" header="Marca / Modelo" sortable>
          <template #body="{ data }"> {{ data.marca_nombre }} {{ data.modelo_nombre }} </template>
        </Column>
        <Column field="anio" header="Año" sortable />
        <Column field="estatus_nombre" header="Estatus" sortable>
          <template #body="{ data }">
            <Tag :value="data.estatus_nombre" :severity="estatusSeverity(data.estatus_nombre)" />
          </template>
        </Column>
        <Column field="estado_nombre" header="Estado" sortable />
        <Column field="porcentaje_completado" header="Ficha">
          <template #body="{ data }">
            <CompletitudKnob
              :value="data.porcentaje_completado"
              :size="60"
              v-tooltip.top="`${data.porcentaje_completado ?? 0}% completo`"
            />
          </template>
        </Column>
      </DataTable>
    </div>

    <Dialog
      :visible="showDialog"
      @update:visible="onDialogClose"
      :header="isCreating ? 'Nuevo vehículo' : 'Editar vehículo'"
      :modal="true"
      :style="{ width: '780px', height: '580px' }"
      :closable="true"
      :draggable="false"
      :pt="{ content: { class: 'overflow-hidden' } }"
    >
      <VehiculoFormStepper
        v-model:active-index="activeIndex"
        v-model:submitted="submitted"
        v-model:form="form"
        :is-creating="isCreating"
        :saving="saving"
        :marcas="marcas"
        :modelos="modelos"
        :tipos-vehiculo="tiposVehiculo"
        :colores="colores"
        :colores-placa="coloresPlaca"
        :tipos-uso="tiposUso"
        :estatus-vehiculo="estatusVehiculo"
        :estados="estados"
        :gerencias="gerencias"
        :centros-servicio="centrosServicio"
        :clases-vehiculo="clasesVehiculo"
        :tipos-combustible="tiposCombustible"
        @save="saveVehiculo"
        @cancel="onCancelarClick"
      />
      <template #footer>
        <div class="flex flex-col w-full gap-2">
          <Message v-if="errorMessage" severity="error" :closable="false" class="!text-xs">
            {{ errorMessage }}
          </Message>
          <div class="flex justify-end w-full gap-2">
            <Button label="Cancelar" severity="secondary" @click="onCancelarClick" />
            <Button
              :label="isCreating ? 'Crear vehículo' : 'Guardar cambios'"
              icon="pi pi-check"
              :loading="saving"
              :disabled="saving"
              @click="saveVehiculo"
            />
          </div>
        </div>
      </template>
    </Dialog>

    <ConfirmDialog
      v-model:visible="showConfirmClose"
      header="Descartar cambios"
      message="Tienes cambios sin guardar. ¿Estás seguro de descartarlos?"
      confirmLabel="Descartar"
      confirmSeverity="danger"
      @confirm="cerrarDialog"
    />
  </div>
</template>

<style scoped>
:deep(.p-datatable-tbody) tr {
  transition:
    background-color 0.15s ease,
    filter 0.1s ease;
  outline-offset: -2px;
}
:deep(.p-datatable-tbody) tr:hover {
  background-color: var(--p-content-hover-background);
  cursor: pointer;
}
:deep(.p-datatable-tbody) tr:active {
  filter: brightness(0.92);
}
:deep(.p-datatable-tbody) tr:focus-visible {
  outline: 2px solid var(--p-primary-color);
}
:deep(.p-datatable-tbody) tr:focus-visible {
  outline: 2px solid var(--p-primary-color);
}
</style>
