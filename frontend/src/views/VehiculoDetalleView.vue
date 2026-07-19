<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { placaSeverity, estatusSeverity } from '@/utils/vehiculo'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import { useAuthStore } from '@/stores/auth'
import { ROL_NACIONAL } from '@/utils/roles'
import api from '@/services/api'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import Message from 'primevue/message'
import Tag from 'primevue/tag'
import Skeleton from 'primevue/skeleton'
import ConfirmDialog from '@/components/ConfirmDialog.vue'
import PageHeader from '@/components/PageHeader.vue'
import VehiculoFormStepper from '@/components/vehiculo/VehiculoFormStepper.vue'

const route = useRoute()
const router = useRouter()
const toast = useToast()
const auth = useAuthStore()

const vehiculo = ref(null)
const loading = ref(true)
const notFound = ref(false)
const showDeactivateDialog = ref(false)
const showActivateDialog = ref(false)
const regenerandoQR = ref(false)

// Edit dialog state
const showEditDialog = ref(false)
const editForm = ref(initialEditForm())
const editSubmitted = ref(false)
const editActiveIndex = ref(0)
const editErrorMessage = ref('')
const editSaving = ref(false)
const editIsCreating = computed(() => false)
const editFormSnapshot = ref(null)
const showConfirmClose = ref(false)

const editFormModificado = computed(() => {
  if (!editFormSnapshot.value) return false
  return JSON.stringify(editForm.value) !== JSON.stringify(editFormSnapshot.value)
})

// Catalogs loaded for edit dialog
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
const catalogosCargados = ref(false)

function initialEditForm() {
  return {
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
  }
}

async function loadVehiculo() {
  loading.value = true
  notFound.value = false
  try {
    const { data } = await api.get(`/vehiculos/${route.params.id}`)
    vehiculo.value = data
  } catch (err) {
    if (err.response?.status === 404) {
      notFound.value = true
    } else {
      toast.add({
        severity: 'error',
        summary: 'Error',
        detail: err.response?.data?.detail || 'Error al cargar el vehículo',
        life: 4000,
      })
    }
  } finally {
    loading.value = false
  }
}

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
    api
      .get('/catalogos/clases-vehiculo/')
      .then((r) => {
        clasesVehiculo.value = r.data
      })
      .catch(() => {
        toast.add({
          severity: 'warn',
          summary: 'Catálogo',
          detail: 'Error al cargar clases de vehículo',
          life: 4000,
        })
      }),
    api
      .get('/catalogos/tipos-combustible/')
      .then((r) => {
        tiposCombustible.value = r.data
      })
      .catch(() => {
        toast.add({
          severity: 'warn',
          summary: 'Catálogo',
          detail: 'Error al cargar tipos de combustible',
          life: 4000,
        })
      }),
  ]
  await Promise.allSettled(calls)
}

function volver() {
  router.push({ name: 'vehiculos' })
}

async function ensureCatalogos() {
  if (catalogosCargados.value) return
  await loadCatalogos()
  catalogosCargados.value = true
}

async function abrirEdicion() {
  if (!vehiculo.value) return
  editErrorMessage.value = ''
  editActiveIndex.value = 0
  editSubmitted.value = false
  editSaving.value = false
  const v = vehiculo.value
  editForm.value = {
    numero_economico: v.numero_economico,
    vin: v.vin,
    placa: v.placa ?? '',
    color_placa_id: v.color_placa ?? null,
    placa_intt: v.placa_intt,
    serial_motor: v.serial_motor,
    numero_unidad: v.numero_unidad ?? '',
    categoria_id: v.categoria,
    marca_id: v.marca,
    modelo_id: v.modelo,
    anio: v.anio,
    color_id: v.color ?? null,
    tipo_uso_id: v.tipo_uso ?? null,
    estatus_id: v.estatus,
    estado_id: v.estado,
    gerencia_id: v.gerencia,
    unidad_usuaria_id: v.unidad_usuaria ?? null,
    emplazamiento_id: v.emplazamiento,
    clase_id: v.clase,
    tipo_combustible_id: v.tipo_combustible,
  }
  editFormSnapshot.value = JSON.parse(JSON.stringify(editForm.value))
  await ensureCatalogos()
  showEditDialog.value = true
}

function onCancelarEdicion() {
  if (editFormModificado.value) {
    showConfirmClose.value = true
  } else {
    showEditDialog.value = false
  }
}

function cerrarDialogEditar() {
  showConfirmClose.value = false
  showEditDialog.value = false
  editFormSnapshot.value = null
}

function onDialogEditarClose(val) {
  if (val) return
  if (!showEditDialog.value) return
  if (editFormModificado.value) {
    showConfirmClose.value = true
  } else {
    showEditDialog.value = false
  }
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

async function actualizarVehiculo() {
  if (!vehiculo.value) return
  editSubmitted.value = true
  editSaving.value = true
  editErrorMessage.value = ''

  const error = validarFormulario(editForm.value)
  if (error) {
    editErrorMessage.value = error
    editSaving.value = false
    return
  }

  const payload = {
    numero_economico: editForm.value.numero_economico,
    vin: editForm.value.vin,
    placa: editForm.value.placa || null,
    color_placa_id: editForm.value.color_placa_id,
    placa_intt: editForm.value.placa_intt || '',
    serial_motor: editForm.value.serial_motor || '',
    numero_unidad: editForm.value.numero_unidad || null,
    categoria_id: editForm.value.categoria_id,
    marca_id: editForm.value.marca_id,
    modelo_id: editForm.value.modelo_id,
    anio: editForm.value.anio,
    color_id: editForm.value.color_id,
    tipo_uso_id: editForm.value.tipo_uso_id || null,
    estatus_id: editForm.value.estatus_id,
    estado_id: editForm.value.estado_id,
    gerencia_id: editForm.value.gerencia_id,
    unidad_usuaria_id: editForm.value.unidad_usuaria_id || null,
    emplazamiento_id: editForm.value.emplazamiento_id,
    clase_id: editForm.value.clase_id,
    tipo_combustible_id: editForm.value.tipo_combustible_id,
  }

  try {
    const { data } = await api.put(`/vehiculos/${vehiculo.value.id}`, payload)
    showEditDialog.value = false
    vehiculo.value = data
    toast.add({
      severity: 'success',
      summary: 'Vehículo actualizado',
      detail: `${data.numero_economico} — ${data.marca_nombre} ${data.modelo_nombre}`,
      life: 4000,
    })
  } catch (err) {
    const data = err.response?.data
    editErrorMessage.value = Array.isArray(data)
      ? data.map((e) => e.msg).join('; ')
      : data?.detail || 'Error al guardar el vehículo'
  } finally {
    editSaving.value = false
  }
}

function descargarQR() {
  if (!vehiculo.value?.codigo_qr) return
  const link = document.createElement('a')
  link.href = vehiculo.value.codigo_qr
  link.download = `${vehiculo.value.numero_economico}_qr.png`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

function imprimirQR() {
  if (!vehiculo.value?.codigo_qr) return
  const win = window.open('', '_blank')
  win.document.write(
    `<!DOCTYPE html><html><head><title>QR ${vehiculo.value.numero_economico}</title><style>body{display:flex;justify-content:center;align-items:center;height:100vh;margin:0}img{max-width:90vw;max-height:90vh}</style></head><body><img src="${vehiculo.value.codigo_qr}" /></body></html>`,
  )
  win.document.close()
  win.focus()
  setTimeout(() => win.print(), 300)
}

async function regenerarQR() {
  if (!vehiculo.value?.id) return
  regenerandoQR.value = true
  try {
    const { data } = await api.post(`/vehiculos/${vehiculo.value.id}/regenerar-qr`)
    vehiculo.value.codigo_qr = data.codigo_qr
    toast.add({
      severity: 'success',
      summary: 'QR regenerado',
      detail: 'Código QR actualizado correctamente',
      life: 3000,
    })
  } catch (err) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: err.response?.data?.detail || 'Error al regenerar QR',
      life: 4000,
    })
  } finally {
    regenerandoQR.value = false
  }
}

function confirmDesactivar() {
  showDeactivateDialog.value = true
}

function confirmActivar() {
  showActivateDialog.value = true
}

async function desactivar() {
  if (!vehiculo.value) return
  try {
    await api.delete(`/vehiculos/${vehiculo.value.id}`)
    vehiculo.value.estatus_activo = false
    showDeactivateDialog.value = false
    toast.add({
      severity: 'success',
      summary: 'Vehículo desactivado',
      detail: `${vehiculo.value.numero_economico} desactivado`,
      life: 4000,
    })
  } catch (err) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: err.response?.data?.detail || 'Error al desactivar',
      life: 4000,
    })
  }
}

async function activar() {
  if (!vehiculo.value) return
  try {
    await api.put(`/vehiculos/${vehiculo.value.id}`, { estatus_activo: true })
    vehiculo.value.estatus_activo = true
    showActivateDialog.value = false
    toast.add({
      severity: 'success',
      summary: 'Vehículo reactivado',
      detail: `${vehiculo.value.numero_economico} reactivado`,
      life: 4000,
    })
  } catch (err) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: err.response?.data?.detail || 'Error al reactivar',
      life: 4000,
    })
  }
}

onMounted(loadVehiculo)
watch(() => route.params.id, loadVehiculo)
</script>

<template>
  <div class="w-full">
    <div class="flex items-center gap-3 mb-6">
      <Button
        icon="pi pi-arrow-left"
        severity="secondary"
        text
        rounded
        @click="volver"
        v-tooltip.top="'Volver al listado'"
        aria-label="Volver al listado"
      />
      <div v-if="vehiculo" class="flex-1 min-w-0">
        <PageHeader
          :title="`${vehiculo.numero_economico} — ${vehiculo.marca_nombre} ${vehiculo.modelo_nombre}`"
          subtitle="Ficha técnica del vehículo"
          icon="pi pi-truck"
        />
      </div>
      <div v-else class="flex-1" />
      <div v-if="auth.tieneRol(ROL_NACIONAL)" class="flex gap-2 shrink-0">
        <Button label="Editar" icon="pi pi-pencil" @click="abrirEdicion" />
        <Button
          v-if="vehiculo?.estatus_activo"
          label="Desactivar"
          icon="pi pi-ban"
          severity="danger"
          @click="confirmDesactivar"
        />
        <Button
          v-else
          label="Reactivar"
          icon="pi pi-check-circle"
          severity="success"
          @click="confirmActivar"
        />
      </div>
    </div>

    <template v-if="loading">
      <div class="border border-card-border rounded-md bg-card p-6 space-y-4">
        <Skeleton width="60%" height="1.5rem" />
        <Skeleton width="40%" height="1rem" />
        <div class="grid grid-cols-3 gap-4 mt-6">
          <Skeleton v-for="n in 8" :key="n" height="1rem" />
        </div>
      </div>
    </template>

    <template v-else-if="notFound">
      <Message severity="warn" :closable="false" class="!mb-4">
        <div class="flex flex-col items-center gap-2 py-4">
          <i class="pi pi-exclamation-triangle text-3xl opacity-60" />
          <p class="text-base font-medium">Vehículo no encontrado</p>
          <p class="text-sm text-muted-color">
            El vehículo que buscas no existe o ha sido eliminado.
          </p>
          <Button
            label="Volver a vehículos"
            icon="pi pi-arrow-left"
            severity="secondary"
            @click="volver"
            class="mt-2"
          />
        </div>
      </Message>
    </template>

    <template v-else-if="vehiculo">
      <div class="border border-card-border rounded-md bg-card p-6 flex flex-col md:flex-row gap-6">
        <div class="flex-1 min-w-0 space-y-6">
          <div>
            <h2 class="text-base font-semibold text-color flex items-center gap-2 mb-3">
              <i class="pi pi-id-card text-primary" /> Identificación
            </h2>
            <div class="grid grid-cols-2 md:grid-cols-3 gap-x-6 gap-y-3 text-base">
              <span class="text-muted-color">N° Económico</span>
              <span class="font-medium col-span-2">{{ vehiculo.numero_economico }}</span>
              <span class="text-muted-color">Serial de carrocería</span>
              <span class="font-medium font-mono col-span-2">{{ vehiculo.vin }}</span>
              <span class="text-muted-color">Placa</span>
              <span class="font-medium col-span-2">
                <div class="flex items-center gap-2">
                  <span>{{ vehiculo.placa || '—' }}</span>
                  <Tag
                    v-if="vehiculo.color_placa_nombre"
                    :value="vehiculo.color_placa_nombre"
                    :severity="placaSeverity(vehiculo.color_placa_nombre)"
                    class="!text-xs"
                  />
                </div>
              </span>
              <span class="text-muted-color">Placa INTT</span>
              <span class="font-medium col-span-2">{{ vehiculo.placa_intt || '—' }}</span>
              <span class="text-muted-color">Serial del motor</span>
              <span class="font-medium col-span-2">{{ vehiculo.serial_motor || '—' }}</span>
              <span class="text-muted-color">N° Unidad</span>
              <span class="font-medium col-span-2">{{ vehiculo.numero_unidad || '—' }}</span>
            </div>
          </div>

          <hr class="border-card-border" />

          <div>
            <h2 class="text-base font-semibold text-color flex items-center gap-2 mb-3">
              <i class="pi pi-cog text-primary" /> Características
            </h2>
            <div class="grid grid-cols-2 md:grid-cols-3 gap-x-6 gap-y-3 text-base">
              <span class="text-muted-color">Categoría</span>
              <span class="font-medium col-span-2">{{ vehiculo.categoria_nombre }}</span>
              <span class="text-muted-color">Clase</span>
              <span class="font-medium col-span-2">{{ vehiculo.clase_nombre }}</span>
              <span class="text-muted-color">Tipo de combustible</span>
              <span class="font-medium col-span-2">{{ vehiculo.tipo_combustible_nombre }}</span>
              <span class="text-muted-color">Tipo de uso</span>
              <span class="font-medium col-span-2">{{ vehiculo.tipo_uso_nombre || '—' }}</span>
              <span class="text-muted-color">Marca</span>
              <span class="font-medium col-span-2">{{ vehiculo.marca_nombre }}</span>
              <span class="text-muted-color">Modelo</span>
              <span class="font-medium col-span-2">{{ vehiculo.modelo_nombre }}</span>
              <span class="text-muted-color">Año</span>
              <span class="font-medium col-span-2">{{ vehiculo.anio }}</span>
              <span class="text-muted-color">Color</span>
              <span class="font-medium col-span-2">{{ vehiculo.color_nombre || '—' }}</span>
              <span class="text-muted-color">Estatus</span>
              <span class="font-medium col-span-2">
                <Tag
                  :value="vehiculo.estatus_nombre"
                  :severity="estatusSeverity(vehiculo.estatus_nombre)"
                />
              </span>
            </div>
          </div>

          <hr class="border-card-border" />

          <div>
            <h2 class="text-base font-semibold text-color flex items-center gap-2 mb-3">
              <i class="pi pi-map-marker text-primary" /> Asignación
            </h2>
            <div class="grid grid-cols-2 md:grid-cols-3 gap-x-6 gap-y-3 text-base">
              <span class="text-muted-color">Estado</span>
              <span class="font-medium col-span-2">{{ vehiculo.estado_nombre }}</span>
              <span class="text-muted-color">Gerencia</span>
              <span class="font-medium col-span-2">{{ vehiculo.gerencia_nombre }}</span>
              <span class="text-muted-color">Unidad usuaria</span>
              <span class="font-medium col-span-2">{{
                vehiculo.unidad_usuaria_nombre || '—'
              }}</span>
              <span class="text-muted-color">Emplazamiento</span>
              <span class="font-medium col-span-2">{{ vehiculo.emplazamiento_nombre }}</span>
            </div>
          </div>
        </div>

        <div class="shrink-0 flex flex-col items-center gap-2">
          <img
            v-if="vehiculo.codigo_qr"
            :src="vehiculo.codigo_qr"
            alt="QR del vehículo"
            class="w-52 h-52 border border-card-border rounded-md"
          />
          <span class="text-sm text-muted-color">Código QR</span>
          <div v-if="vehiculo.codigo_qr" class="flex gap-1">
            <Button
              icon="pi pi-download"
              text
              size="small"
              v-tooltip.top="'Descargar QR'"
              @click="descargarQR"
            />
            <Button
              icon="pi pi-print"
              text
              size="small"
              v-tooltip.top="'Imprimir QR'"
              @click="imprimirQR"
            />
            <Button
              icon="pi pi-refresh"
              text
              size="small"
              :loading="regenerandoQR"
              v-tooltip.top="'Regenerar QR'"
              v-if="auth.tieneRol(ROL_NACIONAL)"
              @click="regenerarQR"
            />
          </div>
        </div>
      </div>
    </template>

    <ConfirmDialog
      v-model:visible="showDeactivateDialog"
      header="Desactivar vehículo"
      :message="`¿Estás seguro de desactivar el vehículo ${vehiculo?.numero_economico} (${vehiculo?.marca_nombre} ${vehiculo?.modelo_nombre})?`"
      confirmLabel="Desactivar"
      confirmSeverity="danger"
      @confirm="desactivar"
    />
    <ConfirmDialog
      v-model:visible="showActivateDialog"
      header="Reactivar vehículo"
      :message="`¿Estás seguro de reactivar el vehículo ${vehiculo?.numero_economico} (${vehiculo?.marca_nombre} ${vehiculo?.modelo_nombre})?`"
      confirmLabel="Reactivar"
      confirmSeverity="success"
      @confirm="activar"
    />

    <ConfirmDialog
      v-model:visible="showConfirmClose"
      header="Descartar cambios"
      message="Tienes cambios sin guardar. ¿Estás seguro de descartarlos?"
      confirmLabel="Descartar"
      confirmSeverity="danger"
      @confirm="cerrarDialogEditar"
    />

    <Dialog
      :visible="showEditDialog"
      @update:visible="onDialogEditarClose"
      header="Editar vehículo"
      :modal="true"
      :style="{ width: '780px', height: '580px' }"
      :closable="true"
      :draggable="false"
      :pt="{ content: { class: 'overflow-hidden' } }"
    >
      <VehiculoFormStepper
        v-model:active-index="editActiveIndex"
        v-model:submitted="editSubmitted"
        v-model:form="editForm"
        :is-creating="editIsCreating"
        :saving="editSaving"
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
        @save="actualizarVehiculo"
        @cancel="onCancelarEdicion"
      />
      <template #footer>
        <div class="flex flex-col w-full gap-2">
          <Message v-if="editErrorMessage" severity="error" :closable="false" class="!text-xs">
            {{ editErrorMessage }}
          </Message>
          <div class="flex justify-end w-full gap-2">
            <Button label="Cancelar" severity="secondary" @click="onCancelarEdicion" />
            <Button
              label="Guardar cambios"
              icon="pi pi-check"
              :loading="editSaving"
              :disabled="editSaving"
              @click="actualizarVehiculo"
            />
          </div>
        </div>
      </template>
    </Dialog>
  </div>
</template>
