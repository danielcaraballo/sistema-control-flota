<script setup>
import { ref, computed, onMounted } from 'vue'
import { placaSeverity, estatusSeverity } from '@/utils/vehiculo'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'
import Button from 'primevue/button'
import Column from 'primevue/column'
import DataTable from 'primevue/datatable'
import Dialog from 'primevue/dialog'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import InputText from 'primevue/inputtext'
import Tag from 'primevue/tag'
import Skeleton from 'primevue/skeleton'
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

const loading = ref(true)
const saving = ref(false)
const showDialog = ref(false)
const editingVehiculo = ref(null)
const submitted = ref(false)
const errorMessage = ref('')
const activeStep = ref(1)
const filters = ref({ global: { value: null, matchMode: 'contains' } })
const catalogosCargados = ref(false)
const showConfirmClose = ref(false)
const formSnapshot = ref(null)

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
})

const form = ref(initialForm())

const isCreating = computed(() => !editingVehiculo.value)

async function loadCatalogos() {
  const calls = [
    api
      .get('/catalogos/marcas/')
      .then((r) => {
        marcas.value = r.data
      })
      .catch(() => {
        toast.add({
          severity: 'warn',
          summary: 'Catálogo',
          detail: 'Error al cargar marcas',
          life: 4000,
        })
      }),
    api
      .get('/catalogos/modelos/')
      .then((r) => {
        modelos.value = r.data
      })
      .catch(() => {
        toast.add({
          severity: 'warn',
          summary: 'Catálogo',
          detail: 'Error al cargar modelos',
          life: 4000,
        })
      }),
    api
      .get('/catalogos/tipos-vehiculo/')
      .then((r) => {
        tiposVehiculo.value = r.data
      })
      .catch(() => {
        toast.add({
          severity: 'warn',
          summary: 'Catálogo',
          detail: 'Error al cargar tipos de vehículo',
          life: 4000,
        })
      }),
    api
      .get('/catalogos/colores/')
      .then((r) => {
        colores.value = r.data
      })
      .catch(() => {
        toast.add({
          severity: 'warn',
          summary: 'Catálogo',
          detail: 'Error al cargar colores',
          life: 4000,
        })
      }),
    api
      .get('/catalogos/colores-placa/')
      .then((r) => {
        coloresPlaca.value = r.data
      })
      .catch(() => {
        toast.add({
          severity: 'warn',
          summary: 'Catálogo',
          detail: 'Error al cargar colores de placa',
          life: 4000,
        })
      }),
    api
      .get('/catalogos/tipos-uso/')
      .then((r) => {
        tiposUso.value = r.data
      })
      .catch(() => {
        toast.add({
          severity: 'warn',
          summary: 'Catálogo',
          detail: 'Error al cargar tipos de uso',
          life: 4000,
        })
      }),
    api
      .get('/catalogos/estatus-vehiculo/')
      .then((r) => {
        estatusVehiculo.value = r.data
      })
      .catch(() => {
        toast.add({
          severity: 'warn',
          summary: 'Catálogo',
          detail: 'Error al cargar estatus de vehículo',
          life: 4000,
        })
      }),
    api
      .get('/organizacion/estados/')
      .then((r) => {
        estados.value = r.data
      })
      .catch(() => {
        toast.add({
          severity: 'warn',
          summary: 'Catálogo',
          detail: 'Error al cargar estados',
          life: 4000,
        })
      }),
    api
      .get('/organizacion/gerencias/')
      .then((r) => {
        gerencias.value = r.data
      })
      .catch(() => {
        toast.add({
          severity: 'warn',
          summary: 'Catálogo',
          detail: 'Error al cargar gerencias',
          life: 4000,
        })
      }),
    api
      .get('/organizacion/centros-servicio/')
      .then((r) => {
        centrosServicio.value = r.data
      })
      .catch(() => {
        toast.add({
          severity: 'warn',
          summary: 'Catálogo',
          detail: 'Error al cargar centros de servicio',
          life: 4000,
        })
      }),
  ]
  await Promise.allSettled(calls)
}

async function loadVehiculos() {
  loading.value = true
  try {
    const params = auth.tieneRol('nacional') ? '?incluir_inactivos=true' : ''
    const { data } = await api.get('/vehiculos/' + params)
    vehiculos.value = data
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

async function ensureCatalogos() {
  if (catalogosCargados.value) return
  await loadCatalogos()
  catalogosCargados.value = true
}

async function openNew() {
  editingVehiculo.value = null
  errorMessage.value = ''
  activeStep.value = 1
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
  activeStep.value = 1
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
  }
  formSnapshot.value = JSON.parse(JSON.stringify(form.value))
  submitted.value = false
  await ensureCatalogos()
  showDialog.value = true
}

async function saveVehiculo() {
  submitted.value = true
  saving.value = true
  errorMessage.value = ''

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

onMounted(async () => {
  await loadVehiculos()
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
      <DataTable
        :value="vehiculos"
        v-model:filters="filters"
        :globalFilterFields="[
          'numero_economico',
          'marca_nombre',
          'modelo_nombre',
          'placa',
          'color_placa_nombre',
          'anio',
          'vin',
          'estado_nombre',
          'gerencia_nombre',
          'estatus_nombre',
        ]"
        :loading="loading"
        scrollable
        stripedRows
        paginator
        :rows="10"
        :rowsPerPageOptions="[10, 25, 50]"
        sortField="numero_economico"
        :sortOrder="1"
        @row-click="verDetalle($event.data)"
      >
        <template #header>
          <div class="flex justify-between items-center gap-2 flex-wrap">
            <IconField>
              <InputIcon class="pi pi-search" />
              <InputText v-model="filters.global.value" placeholder="Buscar vehículos..." />
            </IconField>
            <Button
              v-if="auth.tieneRol('nacional')"
              label="Agregar vehículo"
              icon="pi pi-plus"
              @click="openNew"
            />
          </div>
        </template>
        <template #empty>
          <div class="flex flex-col items-center justify-center py-12 text-muted-color">
            <i class="pi pi-truck text-4xl mb-3 opacity-40" />
            <p class="text-sm font-medium">No hay vehículos registrados</p>
          </div>
        </template>
        <template #loading>
          <div v-for="n in 5" :key="n" class="flex items-center gap-4 p-2">
            <Skeleton width="12%" height="1rem" />
            <Skeleton width="16%" height="1rem" />
            <Skeleton width="8%" height="1rem" />
            <Skeleton width="8%" height="1rem" />
            <Skeleton width="14%" height="1rem" />
            <Skeleton width="8%" height="1rem" />
            <Skeleton width="10%" height="1rem" />
            <Skeleton width="12%" height="1rem" />
            <Skeleton width="8%" height="1rem" />
          </div>
        </template>

        <Column field="numero_economico" header="N° Económico" sortable />
        <Column field="marca_nombre" header="Marca / Modelo" sortable>
          <template #body="{ data }"> {{ data.marca_nombre }} {{ data.modelo_nombre }} </template>
        </Column>
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
        <Column field="anio" header="Año" sortable />
        <Column field="vin" header="Serial carrocería" sortable>
          <template #body="{ data }">
            <span class="font-mono text-xs">{{ data.vin?.substring(0, 11) }}...</span>
          </template>
        </Column>
        <Column field="estatus_nombre" header="Estatus" sortable>
          <template #body="{ data }">
            <Tag :value="data.estatus_nombre" :severity="estatusSeverity(data.estatus_nombre)" />
          </template>
        </Column>
        <Column field="estado_nombre" header="Estado" sortable />
        <Column field="gerencia_nombre" header="Gerencia" sortable />
        <Column field="estatus_activo" header="Activo" sortable>
          <template #body="{ data }">
            <Tag
              :value="data.estatus_activo ? 'Activo' : 'Inactivo'"
              :severity="data.estatus_activo ? 'success' : 'danger'"
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
      :style="{ width: '780px', height: '620px' }"
      :closable="true"
      :draggable="false"
    >
      <VehiculoFormStepper
        v-model:active-step="activeStep"
        v-model:submitted="submitted"
        v-model:form="form"
        :error-message="errorMessage"
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
        @save="saveVehiculo"
        @cancel="onCancelarClick"
      />
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
.p-datatable-tbody tr {
  transition: background-color 0.15s ease;
}
.p-datatable-tbody tr:hover {
  background-color: var(--p-card-hover);
  cursor: pointer;
}
</style>
