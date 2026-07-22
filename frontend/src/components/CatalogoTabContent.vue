<script setup>
import { ref, computed, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import { ROL_NACIONAL } from '@/utils/roles'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'
import Button from 'primevue/button'
import Column from 'primevue/column'
import DataTable from 'primevue/datatable'
import Dialog from 'primevue/dialog'
import Dropdown from 'primevue/dropdown'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import InputText from 'primevue/inputtext'
import Message from 'primevue/message'
import Skeleton from 'primevue/skeleton'
import Tag from 'primevue/tag'
import ConfirmDialog from '@/components/ConfirmDialog.vue'

const props = defineProps({
  config: { type: Object, required: true },
  fkCatalogs: { type: Object, default: () => ({}) },
})

const toast = useToast()
const auth = useAuthStore()

const items = ref([])
const loading = ref(true)
const filters = ref({ global: { value: null, matchMode: 'contains' } })
const skeletonRows = computed(() => (loading.value ? [...Array(10)] : []))
const showDialog = ref(false)
const editingItem = ref(null)
const submitted = ref(false)
const errorMessage = ref('')
const form = ref({})
const showDeactivateDialog = ref(false)
const showActivateDialog = ref(false)
const itemToToggle = ref(null)

function resetForm() {
  form.value = {}
  submitted.value = false
  errorMessage.value = ''
}

function openNew() {
  editingItem.value = null
  resetForm()
  showDialog.value = true
}

function openEdit(item) {
  editingItem.value = item
  resetForm()
  form.value = { ...item }
  showDialog.value = true
}

async function loadItems() {
  loading.value = true
  try {
    const { data } = await api.get(props.config.endpoint + '?incluir_inactivos=true')
    items.value = data
  } catch (err) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: err.response?.data?.detail || 'Error al cargar datos',
      life: 4000,
    })
  } finally {
    loading.value = false
  }
}

function buildPayload() {
  const key = props.config.key
  const payload = {}

  if (key === 'modelos') {
    if (form.value.nombre) payload.nombre = form.value.nombre
    if (form.value.marca) payload.marca_id = form.value.marca
  } else if (key === 'tiposFalla') {
    if (form.value.descripcion) payload.descripcion = form.value.descripcion
    if (form.value.sistema_afectado) payload.sistema_afectado_id = form.value.sistema_afectado
  } else if (key === 'centrosServicio') {
    if (form.value.nombre) payload.nombre = form.value.nombre
    if (form.value.estado) payload.estado_id = form.value.estado
  } else {
    if (form.value[props.config.field]) payload[props.config.field] = form.value[props.config.field]
  }
  return payload
}

async function saveItem() {
  submitted.value = true
  errorMessage.value = ''

  const payload = buildPayload()
  if (Object.keys(payload).length === 0) {
    errorMessage.value = 'Completa al menos un campo antes de guardar'
    return
  }

  try {
    if (editingItem.value) {
      await api.put(`${props.config.endpoint}${editingItem.value.id}`, payload)
      toast.add({
        severity: 'success',
        summary: 'Actualizado',
        detail: 'Elemento actualizado exitosamente',
        life: 3000,
      })
    } else {
      await api.post(props.config.endpoint, payload)
      toast.add({
        severity: 'success',
        summary: 'Creado',
        detail: 'Elemento creado exitosamente',
        life: 3000,
      })
    }
    showDialog.value = false
    await loadItems()
  } catch (err) {
    const errData = err.response?.data
    errorMessage.value = Array.isArray(errData)
      ? errData.map((e) => e.msg).join('; ')
      : errData?.detail || 'Error al guardar'
  }
}

function confirmDeactivate(item) {
  itemToToggle.value = item
  showDeactivateDialog.value = true
}

function confirmActivate(item) {
  itemToToggle.value = item
  showActivateDialog.value = true
}

async function deactivateItem() {
  const item = itemToToggle.value
  if (!item) return
  try {
    await api.delete(`${props.config.endpoint}${item.id}`)
    const idx = items.value.findIndex((i) => i.id === item.id)
    if (idx !== -1) items.value[idx] = { ...items.value[idx], estatus_activo: false }
    showDeactivateDialog.value = false
    toast.add({
      severity: 'success',
      summary: 'Desactivado',
      detail: 'Elemento desactivado',
      life: 3000,
    })
    itemToToggle.value = null
  } catch (err) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: err.response?.data?.detail || 'Error al desactivar',
      life: 4000,
    })
  }
}

async function activateItem() {
  const item = itemToToggle.value
  if (!item) return
  try {
    await api.put(`${props.config.endpoint}${item.id}`, { estatus_activo: true })
    const idx = items.value.findIndex((i) => i.id === item.id)
    if (idx !== -1) items.value[idx] = { ...items.value[idx], estatus_activo: true }
    showActivateDialog.value = false
    toast.add({
      severity: 'success',
      summary: 'Reactivado',
      detail: 'Elemento reactivado',
      life: 3000,
    })
    itemToToggle.value = null
  } catch (err) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: err.response?.data?.detail || 'Error al reactivar',
      life: 4000,
    })
  }
}

onMounted(loadItems)
</script>

<template>
  <div>
    <DataTable
      :value="loading ? skeletonRows : items"
      v-model:filters="filters"
      :globalFilterFields="[config.filterField]"
      :loading="loading"
      scrollable
      scrollHeight="flex"
      stripedRows
      paginator
      :rows="10"
      :rowsPerPageOptions="[10, 25, 50]"
    >
      <template #header>
        <div class="flex justify-between items-center gap-2 flex-wrap">
          <IconField>
            <InputIcon class="pi pi-search" />
            <InputText v-model="filters.global.value" placeholder="Buscar..." />
          </IconField>
          <Button
            v-if="auth.tieneRol(ROL_NACIONAL)"
            label="Agregar"
            icon="pi pi-plus"
            @click="openNew"
          />
        </div>
      </template>
      <template #empty>
        <div class="flex flex-col items-center justify-center py-12 text-muted-color">
          <i :class="config.icon + ' text-4xl mb-3 opacity-40'" />
          <p class="text-sm font-medium">No hay registros</p>
        </div>
      </template>

      <Column v-if="config.key === 'modelos'" field="marca_nombre" header="Marca" sortable>
        <template #body="{ data }">
          <Skeleton v-if="loading" width="50%" height="1.25rem" />
          <template v-else>{{ data.marca_nombre }}</template>
        </template>
      </Column>
      <Column
        v-if="config.key === 'tiposFalla'"
        field="sistema_afectado_nombre"
        header="Sistema Afectado"
        sortable
      >
        <template #body="{ data }">
          <Skeleton v-if="loading" width="50%" height="1.25rem" />
          <template v-else>{{ data.sistema_afectado_nombre }}</template>
        </template>
      </Column>
      <Column
        v-if="config.key === 'centrosServicio'"
        field="estado_nombre"
        header="Estado"
        sortable
      >
        <template #body="{ data }">
          <Skeleton v-if="loading" width="50%" height="1.25rem" />
          <template v-else>{{ data.estado_nombre }}</template>
        </template>
      </Column>
      <Column :field="config.field" :header="config.label" sortable>
        <template #body="{ data }">
          <Skeleton v-if="loading" width="55%" height="1.25rem" />
          <template v-else>{{ data[config.field] }}</template>
        </template>
      </Column>

      <Column field="estatus_activo" header="Activo" sortable style="width: 7rem">
        <template #body="{ data }">
          <Skeleton v-if="loading" width="5rem" height="1.5rem" borderRadius="6px" />
          <Tag
            v-else
            :value="data.estatus_activo ? 'Activo' : 'Inactivo'"
            :severity="data.estatus_activo ? 'success' : 'danger'"
          />
        </template>
      </Column>

      <Column header="Acciones" style="width: 8rem">
        <template #body="{ data }">
          <Skeleton v-if="loading" width="6rem" height="1.5rem" borderRadius="6px" />
          <template v-else>
            <Button
              icon="pi pi-pencil"
              severity="secondary"
              text
              rounded
              @click="openEdit(data)"
              v-tooltip.top="'Editar'"
            />
            <Button
              v-if="data.estatus_activo"
              icon="pi pi-ban"
              severity="danger"
              text
              rounded
              @click="confirmDeactivate(data)"
              v-tooltip.top="'Desactivar'"
            />
            <Button
              v-if="!data.estatus_activo"
              icon="pi pi-check-circle"
              severity="success"
              text
              rounded
              @click="confirmActivate(data)"
              v-tooltip.top="'Reactivar'"
            />
          </template>
        </template>
      </Column>
    </DataTable>

    <Dialog
      v-model:visible="showDialog"
      :header="editingItem ? 'Editar' : 'Nuevo'"
      :modal="true"
      :style="{ width: 'min(450px, calc(100vw - 2rem))' }"
      :closable="true"
      :draggable="false"
    >
      <Message v-if="errorMessage" severity="error" :closable="false" class="!mb-4 !text-xs">
        {{ errorMessage }}
      </Message>

      <div class="flex flex-col gap-4">
        <div v-if="config.key === 'modelos'" class="flex flex-col gap-1.5">
          <label class="text-sm font-semibold">Marca</label>
          <Dropdown
            v-model="form.marca"
            :options="fkCatalogs.marcas"
            optionLabel="nombre"
            optionValue="id"
            placeholder="Seleccionar marca"
            class="w-full"
          />
        </div>

        <div v-if="config.key === 'tiposFalla'" class="flex flex-col gap-1.5">
          <label class="text-sm font-semibold">Sistema afectado</label>
          <Dropdown
            v-model="form.sistema_afectado"
            :options="fkCatalogs.sistemas"
            optionLabel="nombre"
            optionValue="id"
            placeholder="Seleccionar sistema"
            class="w-full"
          />
        </div>

        <div v-if="config.key === 'centrosServicio'" class="flex flex-col gap-1.5">
          <label class="text-sm font-semibold">Estado</label>
          <Dropdown
            v-model="form.estado"
            :options="fkCatalogs.estados"
            optionLabel="nombre"
            optionValue="id"
            placeholder="Seleccionar estado"
            class="w-full"
          />
        </div>

        <div class="flex flex-col gap-1.5">
          <label class="text-sm font-semibold">
            {{ config.key === 'tiposFalla' ? 'Descripción' : 'Nombre' }}
          </label>
          <InputText v-model="form[config.field]" class="w-full" />
        </div>
      </div>

      <template #footer>
        <Button label="Cancelar" severity="secondary" @click="showDialog = false" />
        <Button label="Guardar" @click="saveItem" />
      </template>
    </Dialog>

    <ConfirmDialog
      v-model:visible="showDeactivateDialog"
      header="Desactivar"
      message="¿Estás seguro de desactivar este elemento?"
      confirmLabel="Desactivar"
      confirmSeverity="danger"
      @confirm="deactivateItem"
    />
    <ConfirmDialog
      v-model:visible="showActivateDialog"
      header="Reactivar"
      message="¿Estás seguro de reactivar este elemento?"
      confirmLabel="Reactivar"
      confirmSeverity="success"
      @confirm="activateItem"
    />
  </div>
</template>

<style scoped></style>
