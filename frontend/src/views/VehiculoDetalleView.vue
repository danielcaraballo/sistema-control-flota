<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'
import Button from 'primevue/button'
import Tag from 'primevue/tag'
import Skeleton from 'primevue/skeleton'
import ConfirmDialog from '@/components/ConfirmDialog.vue'
import PageHeader from '@/components/PageHeader.vue'

const route = useRoute()
const router = useRouter()
const toast = useToast()
const auth = useAuthStore()

const vehiculo = ref(null)
const loading = ref(true)
const showDeactivateDialog = ref(false)
const showActivateDialog = ref(false)

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

async function loadVehiculo() {
  loading.value = true
  try {
    const { data } = await api.get(`/vehiculos/${route.params.id}`)
    vehiculo.value = data
  } catch (err) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: err.response?.data?.detail || 'Error al cargar el vehículo',
      life: 4000,
    })
  } finally {
    loading.value = false
  }
}

function volver() {
  router.push({ name: 'vehiculos' })
}

function editar() {
  router.push({ name: 'vehiculos', query: { editar: route.params.id } })
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
  <div class="w-full max-w-[900px]">
    <div class="flex items-center gap-3 mb-6">
      <Button
        icon="pi pi-arrow-left"
        severity="secondary"
        text
        rounded
        @click="volver"
        v-tooltip.top="'Volver al listado'"
      />
      <PageHeader
        v-if="vehiculo"
        :title="`${vehiculo.numero_economico} — ${vehiculo.marca_nombre} ${vehiculo.modelo_nombre}`"
        subtitle="Ficha técnica del vehículo"
        icon="pi pi-truck"
      />
      <div v-else class="flex-1" />
      <div v-if="auth.tieneRol('nacional')" class="flex gap-2 shrink-0">
        <Button label="Editar" icon="pi pi-pencil" severity="secondary" @click="editar" />
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
        <div class="grid grid-cols-2 gap-4 mt-6">
          <Skeleton v-for="n in 8" :key="n" height="1rem" />
        </div>
      </div>
    </template>

    <template v-else-if="vehiculo">
      <div class="border border-card-border rounded-md bg-card overflow-hidden">
        <div class="flex flex-col md:flex-row gap-6 p-6">
          <div class="shrink-0 flex flex-col items-center gap-2">
            <img
              v-if="vehiculo.codigo_qr"
              :src="vehiculo.codigo_qr"
              alt="QR del vehículo"
              class="w-44 h-44 border border-card-border rounded-md"
            />
            <span class="text-xs text-muted-color">Código QR</span>
          </div>

          <div class="flex-1 min-w-0 space-y-6">
            <div>
              <h2 class="text-sm font-semibold text-color flex items-center gap-2 mb-3">
                <i class="pi pi-id-card text-primary" /> Identificación
              </h2>
              <div class="grid grid-cols-2 md:grid-cols-3 gap-x-6 gap-y-2.5 text-sm">
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
              <h2 class="text-sm font-semibold text-color flex items-center gap-2 mb-3">
                <i class="pi pi-cog text-primary" /> Características
              </h2>
              <div class="grid grid-cols-2 md:grid-cols-3 gap-x-6 gap-y-2.5 text-sm">
                <span class="text-muted-color">Categoría</span>
                <span class="font-medium col-span-2">{{ vehiculo.categoria_nombre }}</span>
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
              <h2 class="text-sm font-semibold text-color flex items-center gap-2 mb-3">
                <i class="pi pi-map-marker text-primary" /> Asignación
              </h2>
              <div class="grid grid-cols-2 md:grid-cols-3 gap-x-6 gap-y-2.5 text-sm">
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
  </div>
</template>
