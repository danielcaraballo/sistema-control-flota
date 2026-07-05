<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'
import Button from 'primevue/button'
import Column from 'primevue/column'
import DataTable from 'primevue/datatable'
import Dialog from 'primevue/dialog'
import Dropdown from 'primevue/dropdown'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import InputNumber from 'primevue/inputnumber'
import InputText from 'primevue/inputtext'
import Message from 'primevue/message'
import Stepper from 'primevue/stepper'
import StepList from 'primevue/steplist'
import StepPanels from 'primevue/steppanels'
import Step from 'primevue/step'
import StepPanel from 'primevue/steppanel'
import Tag from 'primevue/tag'
import PageHeader from '@/components/PageHeader.vue'

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
const estatusVehiculo = ref([])
const estados = ref([])
const gerencias = ref([])
const centrosServicio = ref([])

const loading = ref(true)
const showDialog = ref(false)
const editingVehiculo = ref(null)
const submitted = ref(false)
const errorMessage = ref('')
const activeStep = ref(1)
const filters = ref({ global: { value: null, matchMode: 'contains' } })

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
  estatus_id: null,
  estado_id: null,
  gerencia_id: null,
  unidad_usuaria_id: null,
  emplazamiento_id: null,
})

const form = ref(initialForm())

const isCreating = computed(() => !editingVehiculo.value)

const filteredModelos = computed(() => {
  if (!form.value.marca_id) return []
  return modelos.value.filter((m) => m.marca === form.value.marca_id)
})

function placaSeverity(nombre) {
  const map = {
    Amarilla: 'warn',
    Verde: 'success',
    Azul: 'info',
    Blanca: 'secondary',
    Roja: 'danger',
    Plateada: 'contrast',
  }
  return map[nombre] || 'info'
}

function estatusSeverity(nombre) {
  const map = {
    Operativo: 'success',
    'En taller': 'warn',
    'Fuera de servicio': 'danger',
  }
  return map[nombre] || 'info'
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

function openNew() {
  editingVehiculo.value = null
  errorMessage.value = ''
  activeStep.value = 1
  form.value = initialForm()
  submitted.value = false
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
    estatus_id: vehiculo.estatus,
    estado_id: vehiculo.estado,
    gerencia_id: vehiculo.gerencia,
    unidad_usuaria_id: vehiculo.unidad_usuaria ?? null,
    emplazamiento_id: vehiculo.emplazamiento,
  }
  submitted.value = false
  showDialog.value = true
}

function validateStep(step) {
  const f = form.value
  if (step === 1) return f.numero_economico && f.vin
  if (step === 2) return f.categoria_id && f.marca_id && f.modelo_id && f.anio && f.estatus_id
  if (step === 3) return f.estado_id && f.gerencia_id && f.emplazamiento_id
  return true
}

function goToStep(step) {
  submitted.value = true
  errorMessage.value = ''
  if (!validateStep(activeStep.value)) return
  activeStep.value = step
}

function goBack() {
  activeStep.value = activeStep.value - 1
}

async function saveVehiculo() {
  submitted.value = true
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
    errorMessage.value = err.response?.data?.detail || 'Error al guardar el vehículo'
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

onMounted(async () => {
  await Promise.all([loadVehiculos(), loadCatalogos()])
  if (route.query.editar) {
    await loadVehiculoForEdit(route.query.editar)
  }
})

function label(id, list) {
  return list.find((i) => i.id === id)?.nombre ?? ''
}
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
      v-model:visible="showDialog"
      :header="isCreating ? 'Nuevo vehículo' : 'Editar vehículo'"
      :modal="true"
      :style="{ width: '780px', height: '620px' }"
      :closable="true"
      :draggable="false"
    >
      <Message v-if="errorMessage" severity="error" :closable="false" class="!mb-4 !text-xs">
        {{ errorMessage }}
      </Message>

      <Stepper :value="activeStep" :linear="isCreating" class="h-full flex flex-col">
        <div class="flex gap-4 flex-1 min-h-0">
          <StepList class="flex-col w-44 shrink-0 border-r border-card-border pr-4">
            <Step :value="1">Identificación</Step>
            <Step :value="2">Características</Step>
            <Step :value="3">Asignación</Step>
            <Step :value="4">Confirmar</Step>
          </StepList>
          <StepPanels class="flex-1">
            <StepPanel :value="1">
              <div class="grid grid-cols-2 gap-x-4 gap-y-2">
                <div class="flex flex-col gap-1 col-span-2">
                  <label class="text-sm font-semibold">Número económico</label>
                  <InputText
                    v-model="form.numero_economico"
                    class="w-full"
                    :class="{ 'p-invalid': submitted && !form.numero_economico }"
                  />
                  <small v-if="submitted && !form.numero_economico" class="text-xs text-red-500">
                    El número económico es requerido
                  </small>
                </div>
                <div class="flex flex-col gap-1 col-span-2">
                  <label class="text-sm font-semibold">Serial de carrocería</label>
                  <InputText
                    v-model="form.vin"
                    class="w-full"
                    maxlength="17"
                    :class="{ 'p-invalid': submitted && !form.vin }"
                  />
                  <small v-if="submitted && !form.vin" class="text-xs text-red-500">
                    El serial de carrocería es requerido
                  </small>
                </div>
                <div class="flex flex-col gap-1">
                  <label class="text-sm font-semibold">Placa</label>
                  <InputText v-model="form.placa" class="w-full" />
                </div>
                <div class="flex flex-col gap-1">
                  <label class="text-sm font-semibold">Color de placa</label>
                  <Dropdown
                    v-model="form.color_placa_id"
                    :options="coloresPlaca"
                    optionLabel="nombre"
                    optionValue="id"
                    placeholder="Seleccionar"
                    class="w-full"
                    showClear
                  />
                </div>
                <div class="flex flex-col gap-1">
                  <label class="text-sm font-semibold">Placa INTT</label>
                  <InputText v-model="form.placa_intt" class="w-full" />
                </div>
                <div class="flex flex-col gap-1">
                  <label class="text-sm font-semibold">Serial del motor</label>
                  <InputText v-model="form.serial_motor" class="w-full" />
                </div>
                <div class="flex flex-col gap-1 col-span-2">
                  <label class="text-sm font-semibold">N° Unidad</label>
                  <InputText v-model="form.numero_unidad" class="w-full" />
                </div>
              </div>
            </StepPanel>

            <StepPanel :value="2">
              <div class="grid grid-cols-2 gap-x-4 gap-y-2">
                <div class="flex flex-col gap-1">
                  <label class="text-sm font-semibold">Categoría</label>
                  <Dropdown
                    v-model="form.categoria_id"
                    :options="tiposVehiculo"
                    optionLabel="nombre"
                    optionValue="id"
                    placeholder="Seleccionar"
                    class="w-full"
                    :class="{ 'p-invalid': submitted && !form.categoria_id }"
                  />
                  <small v-if="submitted && !form.categoria_id" class="text-xs text-red-500">
                    La categoría es requerida
                  </small>
                </div>
                <div class="flex flex-col gap-1">
                  <label class="text-sm font-semibold">Marca</label>
                  <Dropdown
                    v-model="form.marca_id"
                    :options="marcas"
                    optionLabel="nombre"
                    optionValue="id"
                    placeholder="Seleccionar"
                    class="w-full"
                    :class="{ 'p-invalid': submitted && !form.marca_id }"
                  />
                  <small v-if="submitted && !form.marca_id" class="text-xs text-red-500">
                    La marca es requerida
                  </small>
                </div>
                <div class="flex flex-col gap-1">
                  <label class="text-sm font-semibold">Modelo</label>
                  <Dropdown
                    v-model="form.modelo_id"
                    :options="filteredModelos"
                    optionLabel="nombre"
                    optionValue="id"
                    placeholder="Primero selecciona una marca"
                    class="w-full"
                    :disabled="!form.marca_id"
                    :class="{ 'p-invalid': submitted && !form.modelo_id }"
                  />
                  <small v-if="submitted && !form.modelo_id" class="text-xs text-red-500">
                    El modelo es requerido
                  </small>
                </div>
                <div class="flex flex-col gap-1">
                  <label class="text-sm font-semibold">Año</label>
                  <InputNumber
                    v-model="form.anio"
                    class="w-full"
                    :useGrouping="false"
                    :min="1900"
                    :max="2099"
                    :class="{ 'p-invalid': submitted && !form.anio }"
                  />
                  <small v-if="submitted && !form.anio" class="text-xs text-red-500">
                    El año es requerido
                  </small>
                </div>
                <div class="flex flex-col gap-1">
                  <label class="text-sm font-semibold">Color</label>
                  <Dropdown
                    v-model="form.color_id"
                    :options="colores"
                    optionLabel="nombre"
                    optionValue="id"
                    placeholder="Seleccionar"
                    class="w-full"
                    showClear
                  />
                </div>
                <div class="flex flex-col gap-1">
                  <label class="text-sm font-semibold">Estatus</label>
                  <Dropdown
                    v-model="form.estatus_id"
                    :options="estatusVehiculo"
                    optionLabel="nombre"
                    optionValue="id"
                    placeholder="Seleccionar"
                    class="w-full"
                    :class="{ 'p-invalid': submitted && !form.estatus_id }"
                  />
                  <small v-if="submitted && !form.estatus_id" class="text-xs text-red-500">
                    El estatus es requerido
                  </small>
                </div>
              </div>
            </StepPanel>

            <StepPanel :value="3">
              <div class="grid grid-cols-2 gap-x-4 gap-y-2">
                <div class="flex flex-col gap-1">
                  <label class="text-sm font-semibold">Estado</label>
                  <Dropdown
                    v-model="form.estado_id"
                    :options="estados"
                    optionLabel="nombre"
                    optionValue="id"
                    placeholder="Seleccionar"
                    class="w-full"
                    :class="{ 'p-invalid': submitted && !form.estado_id }"
                  />
                  <small v-if="submitted && !form.estado_id" class="text-xs text-red-500">
                    El estado es requerido
                  </small>
                </div>
                <div class="flex flex-col gap-1">
                  <label class="text-sm font-semibold">Gerencia</label>
                  <Dropdown
                    v-model="form.gerencia_id"
                    :options="gerencias"
                    optionLabel="nombre"
                    optionValue="id"
                    placeholder="Seleccionar"
                    class="w-full"
                    :class="{ 'p-invalid': submitted && !form.gerencia_id }"
                  />
                  <small v-if="submitted && !form.gerencia_id" class="text-xs text-red-500">
                    La gerencia es requerida
                  </small>
                </div>
                <div class="flex flex-col gap-1">
                  <label class="text-sm font-semibold">Unidad usuaria</label>
                  <Dropdown
                    v-model="form.unidad_usuaria_id"
                    :options="gerencias"
                    optionLabel="nombre"
                    optionValue="id"
                    placeholder="Seleccionar"
                    class="w-full"
                    showClear
                  />
                </div>
                <div class="flex flex-col gap-1">
                  <label class="text-sm font-semibold">Emplazamiento</label>
                  <Dropdown
                    v-model="form.emplazamiento_id"
                    :options="centrosServicio"
                    optionLabel="nombre"
                    optionValue="id"
                    placeholder="Seleccionar"
                    class="w-full"
                    :class="{ 'p-invalid': submitted && !form.emplazamiento_id }"
                  />
                  <small v-if="submitted && !form.emplazamiento_id" class="text-xs text-red-500">
                    El emplazamiento es requerido
                  </small>
                </div>
              </div>
            </StepPanel>

            <StepPanel :value="4">
              <div class="space-y-2">
                <p class="text-sm text-muted-color font-semibold mb-2">
                  Revisa los datos antes de {{ isCreating ? 'crear' : 'guardar' }}:
                </p>

                <div class="text-sm font-semibold text-color mb-2 flex items-center gap-2">
                  <i class="pi pi-id-card text-primary" /> Identificación
                </div>
                <div class="grid grid-cols-2 gap-x-4 gap-y-1 mb-2">
                  <span class="text-muted-color text-sm">N° Económico</span>
                  <span class="text-sm font-medium">{{ form.numero_economico }}</span>
                  <span class="text-muted-color text-sm">Serial carrocería</span>
                  <span class="text-sm font-medium font-mono">{{ form.vin }}</span>
                  <span class="text-muted-color text-sm">Placa</span>
                  <span class="text-sm font-medium">{{ form.placa || '—' }}</span>
                  <span class="text-muted-color text-sm">Placa INTT</span>
                  <span class="text-sm font-medium">{{ form.placa_intt || '—' }}</span>
                  <span class="text-muted-color text-sm">Serial del motor</span>
                  <span class="text-sm font-medium">{{ form.serial_motor || '—' }}</span>
                  <span class="text-muted-color text-sm">N° Unidad</span>
                  <span class="text-sm font-medium">{{ form.numero_unidad || '—' }}</span>
                </div>

                <div class="text-sm font-semibold text-color mb-2 flex items-center gap-2">
                  <i class="pi pi-cog text-primary" /> Características
                </div>
                <div class="grid grid-cols-2 gap-x-4 gap-y-1 mb-2">
                  <span class="text-muted-color text-sm">Categoría</span>
                  <span class="text-sm font-medium">{{
                    label(form.categoria_id, tiposVehiculo)
                  }}</span>
                  <span class="text-muted-color text-sm">Marca</span>
                  <span class="text-sm font-medium">{{ label(form.marca_id, marcas) }}</span>
                  <span class="text-muted-color text-sm">Modelo</span>
                  <span class="text-sm font-medium">{{ label(form.modelo_id, modelos) }}</span>
                  <span class="text-muted-color text-sm">Año</span>
                  <span class="text-sm font-medium">{{ form.anio }}</span>
                  <span class="text-muted-color text-sm">Color</span>
                  <span class="text-sm font-medium">{{
                    label(form.color_id, colores) || '—'
                  }}</span>
                  <span class="text-muted-color text-sm">Estatus</span>
                  <span class="text-sm font-medium">{{
                    label(form.estatus_id, estatusVehiculo)
                  }}</span>
                </div>

                <div class="text-sm font-semibold text-color mb-2 flex items-center gap-2">
                  <i class="pi pi-map-marker text-primary" /> Asignación
                </div>
                <div class="grid grid-cols-2 gap-x-4 gap-y-1">
                  <span class="text-muted-color text-sm">Estado</span>
                  <span class="text-sm font-medium">{{ label(form.estado_id, estados) }}</span>
                  <span class="text-muted-color text-sm">Gerencia</span>
                  <span class="text-sm font-medium">{{ label(form.gerencia_id, gerencias) }}</span>
                  <span class="text-muted-color text-sm">Unidad usuaria</span>
                  <span class="text-sm font-medium">{{
                    label(form.unidad_usuaria_id, gerencias) || '—'
                  }}</span>
                  <span class="text-muted-color text-sm">Emplazamiento</span>
                  <span class="text-sm font-medium">{{
                    label(form.emplazamiento_id, centrosServicio)
                  }}</span>
                </div>
              </div>
            </StepPanel>
          </StepPanels>
        </div>
      </Stepper>

      <template #footer>
        <div class="flex justify-between w-full">
          <div>
            <Button
              v-if="activeStep > 1"
              label="Atrás"
              severity="secondary"
              icon="pi pi-arrow-left"
              @click="goBack"
            />
          </div>
          <div class="flex gap-2">
            <Button
              v-if="activeStep < 4"
              label="Cancelar"
              severity="secondary"
              @click="showDialog = false"
            />
            <Button
              v-if="activeStep < 4"
              label="Siguiente"
              icon="pi pi-arrow-right"
              iconPos="right"
              @click="goToStep(activeStep + 1)"
            />
            <Button
              v-if="activeStep === 4"
              :label="isCreating ? 'Crear vehículo' : 'Guardar cambios'"
              icon="pi pi-check"
              @click="saveVehiculo"
            />
          </div>
        </div>
      </template>
    </Dialog>
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
.p-steplist .p-step {
  justify-content: flex-start;
  text-align: left;
}
</style>
