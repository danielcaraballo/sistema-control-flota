<script setup>
import { ref, computed, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'
import { ROLES, ESTATAL_ROLES, ROL_NACIONAL, rolLabel, rolSeverity } from '@/utils/roles'
import Button from 'primevue/button'
import Column from 'primevue/column'
import DataTable from 'primevue/datatable'
import Dialog from 'primevue/dialog'
import Dropdown from 'primevue/dropdown'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import InputText from 'primevue/inputtext'
import Message from 'primevue/message'
import Stepper from 'primevue/stepper'
import StepList from 'primevue/steplist'
import StepPanels from 'primevue/steppanels'
import Step from 'primevue/step'
import StepPanel from 'primevue/steppanel'
import Skeleton from 'primevue/skeleton'
import Tag from 'primevue/tag'
import ConfirmDialog from '@/components/ConfirmDialog.vue'
import CredentialModal from '@/components/CredentialModal.vue'
import PageHeader from '@/components/PageHeader.vue'

function extractError(err) {
  const data = err.response?.data
  if (Array.isArray(data)) return data.map((e) => e.msg).join('; ')
  if (data?.detail) return data.detail
  return null
}

const toast = useToast()
const auth = useAuthStore()
const usuarios = ref([])
const estados = ref([])
const loading = ref(true)
const skeletonRows = computed(() => (loading.value ? [...Array(10)] : []))
const showDialog = ref(false)
const editingUser = ref(null)
const submitted = ref(false)
const errorMessage = ref('')
const activeStep = ref(1)
const showCredentialsDialog = ref(false)
const createdCredentials = ref({ firstName: '', lastName: '', username: '', password: '' })
const showDeactivateDialog = ref(false)
const showActivateDialog = ref(false)
const userToToggle = ref(null)
const filters = ref({ global: { value: null, matchMode: 'contains' } })
const showResetConfirmDialog = ref(false)
const showResetCredentialsDialog = ref(false)
const userToReset = ref(null)
const resetResult = ref('')

const form = ref({
  username: '',
  email: '',
  password: '',
  first_name: '',
  last_name: '',
  rol: null,
  estado_id: null,
})

async function loadEstados() {
  try {
    const { data } = await api.get('/organizacion/estados/')
    estados.value = data
  } catch (err) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: err.response?.data?.detail || 'Error al cargar los estados',
      life: 4000,
    })
  }
}

async function loadUsuarios() {
  loading.value = true
  try {
    const { data } = await api.get('/usuarios/')
    usuarios.value = data
  } catch (err) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: err.response?.data?.detail || 'Error al cargar los usuarios',
      life: 4000,
    })
  } finally {
    loading.value = false
  }
}

const isCreating = computed(() => !editingUser.value)

function openNew() {
  editingUser.value = null
  errorMessage.value = ''
  activeStep.value = 1
  form.value = {
    username: '',
    email: '',
    password: '',
    first_name: '',
    last_name: '',
    rol: null,
    estado_id: null,
  }
  submitted.value = false
  showDialog.value = true
}

function openEdit(user) {
  editingUser.value = user
  errorMessage.value = ''
  activeStep.value = 1
  form.value = {
    username: user.username,
    email: user.email,
    password: '',
    first_name: user.first_name,
    last_name: user.last_name,
    rol: user.rol,
    estado_id: user.estado?.id ?? user.estado ?? null,
  }
  submitted.value = false
  showDialog.value = true
}

function isEstatal(rol) {
  return ESTATAL_ROLES.includes(rol)
}

function validateStep1() {
  return (
    form.value.first_name &&
    form.value.last_name &&
    form.value.email &&
    form.value.rol &&
    (!isEstatal(form.value.rol) || form.value.estado_id)
  )
}

function goToStep2() {
  submitted.value = true
  errorMessage.value = ''
  if (!validateStep1()) return
  activeStep.value = 2
}

async function createUser() {
  submitted.value = true
  errorMessage.value = ''

  try {
    const { data } = await api.post('/usuarios/', {
      first_name: form.value.first_name,
      last_name: form.value.last_name,
      email: form.value.email,
      rol: form.value.rol,
      estado_id: form.value.estado_id || null,
    })
    showDialog.value = false
    createdCredentials.value = {
      firstName: data.user.first_name,
      lastName: data.user.last_name,
      username: data.user.username,
      password: data.password,
    }
    showCredentialsDialog.value = true
    toast.add({
      severity: 'success',
      summary: 'Usuario creado',
      detail: `${data.user.first_name} ${data.user.last_name} creado exitosamente`,
      life: 4000,
    })
    await loadUsuarios()
  } catch (err) {
    errorMessage.value = extractError(err) || 'Error al crear el usuario'
  }
}

function validateEditForm() {
  return form.value.email && form.value.first_name && form.value.last_name
}

async function updateUser() {
  submitted.value = true
  errorMessage.value = ''

  if (!validateEditForm()) return

  try {
    const payload = {
      email: form.value.email,
      first_name: form.value.first_name,
      last_name: form.value.last_name,
      rol: form.value.rol,
      estado_id: form.value.estado_id,
    }
    await api.put(`/usuarios/${editingUser.value.id}`, payload)
    showDialog.value = false
    toast.add({
      severity: 'success',
      summary: 'Usuario actualizado',
      detail: `${form.value.first_name} ${form.value.last_name} actualizado exitosamente`,
      life: 4000,
    })
    await loadUsuarios()
  } catch (err) {
    errorMessage.value = extractError(err) || 'Error al guardar el usuario'
  }
}

function confirmDeactivate(user) {
  userToToggle.value = user
  showDeactivateDialog.value = true
}

function confirmActivate(user) {
  userToToggle.value = user
  showActivateDialog.value = true
}

async function deactivateUser() {
  if (!userToToggle.value) return
  try {
    await api.delete(`/usuarios/${userToToggle.value.id}`)
    const idx = usuarios.value.findIndex((u) => u.id === userToToggle.value.id)
    if (idx !== -1) usuarios.value[idx] = { ...usuarios.value[idx], is_active: false }
    showDeactivateDialog.value = false
    toast.add({
      severity: 'success',
      summary: 'Usuario desactivado',
      detail: `${userToToggle.value.first_name} ${userToToggle.value.last_name} desactivado`,
      life: 4000,
    })
    userToToggle.value = null
  } catch (err) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: err.response?.data?.detail || 'Error al desactivar el usuario',
      life: 4000,
    })
  }
}

async function activateUser() {
  if (!userToToggle.value) return
  try {
    await api.put(`/usuarios/${userToToggle.value.id}`, { is_active: true })
    const idx = usuarios.value.findIndex((u) => u.id === userToToggle.value.id)
    if (idx !== -1) usuarios.value[idx] = { ...usuarios.value[idx], is_active: true }
    showActivateDialog.value = false
    toast.add({
      severity: 'success',
      summary: 'Usuario reactivado',
      detail: `${userToToggle.value.first_name} ${userToToggle.value.last_name} reactivado`,
      life: 4000,
    })
    userToToggle.value = null
  } catch (err) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: err.response?.data?.detail || 'Error al reactivar el usuario',
      life: 4000,
    })
  }
}

function confirmResetPassword(user) {
  userToReset.value = user
  showResetConfirmDialog.value = true
}

async function resetPassword() {
  if (!userToReset.value) return
  try {
    const { data } = await api.post(`/usuarios/${userToReset.value.id}/reset-password`)
    resetResult.value = data.password
    showResetConfirmDialog.value = false
    showResetCredentialsDialog.value = true
    toast.add({
      severity: 'success',
      summary: 'Contraseña reseteada',
      detail: `Contraseña de ${userToReset.value.first_name} ${userToReset.value.last_name} restablecida`,
      life: 4000,
    })
  } catch (err) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: err.response?.data?.detail || 'Error al resetear la contraseña',
      life: 4000,
    })
  }
}

const createCopyText = computed(() => {
  const c = createdCredentials.value
  return `¡Bienvenido al Sistema de Control de Flota!

Hola ${c.firstName} ${c.lastName}, estas son tus credenciales de acceso:

  Usuario: ${c.username}
  Contraseña: ${c.password}

Se recomienda cambiar la contraseña desde la opción en tu perfil.`
})

const resetCopyText = computed(() => {
  if (!userToReset.value || !resetResult.value) return ''
  return `Se ha restablecido la contraseña de ${userToReset.value.first_name} ${userToReset.value.last_name}.

  Usuario: ${userToReset.value.username}
  Nueva contraseña: ${resetResult.value}`
})

const rolLabelForm = computed(() => {
  if (!form.value.rol) return ''
  return ROLES.find((r) => r.value === form.value.rol)?.label || form.value.rol
})

const estadoNombreForm = computed(() => {
  if (!form.value.estado_id) return ''
  return estados.value.find((e) => e.id === form.value.estado_id)?.nombre || ''
})

onMounted(() => {
  loadUsuarios()
  loadEstados()
})
</script>

<template>
  <div class="w-full">
    <PageHeader title="Usuarios" subtitle="Gestión de usuarios del sistema" icon="pi pi-users" />

    <div class="border border-card-border rounded-md bg-card px-4">
      <DataTable
        :value="loading ? skeletonRows : usuarios"
        v-model:filters="filters"
        :globalFilterFields="[
          'username',
          'first_name',
          'last_name',
          'email',
          'rol',
          'estado_nombre',
        ]"
        :loading="loading"
        size="small"
        scrollable
        scrollHeight="flex"
        stripedRows
        paginator
        :rows="10"
        :rowsPerPageOptions="[10, 25, 50]"
        sortField="username"
        :sortOrder="1"
      >
        <template #header>
          <div class="flex justify-between items-center gap-2 flex-wrap">
            <IconField>
              <InputIcon class="pi pi-search" />
              <InputText v-model="filters.global.value" placeholder="Buscar..." size="small" />
            </IconField>
            <Button
              v-if="auth.tieneRol(ROL_NACIONAL)"
              label="Agregar usuario"
              icon="pi pi-plus"
              size="small"
              @click="openNew"
            />
          </div>
        </template>
        <template #empty>
          <div class="flex flex-col items-center justify-center py-12 text-muted-color">
            <i class="pi pi-users text-4xl mb-3 opacity-40" />
            <p class="text-sm font-medium">No hay registros</p>
          </div>
        </template>
        <Column field="username" header="Usuario" sortable>
          <template #body="{ data }">
            <Skeleton v-if="loading" width="60%" height="1.25rem" />
            <template v-else>{{ data.username }}</template>
          </template>
        </Column>
        <Column field="first_name" header="Nombre" sortable>
          <template #body="{ data }">
            <Skeleton v-if="loading" width="50%" height="1.25rem" />
            <template v-else>{{ data.first_name }} {{ data.last_name }}</template>
          </template>
        </Column>
        <Column field="email" header="Correo" sortable>
          <template #body="{ data }">
            <Skeleton v-if="loading" width="70%" height="1.25rem" />
            <template v-else>{{ data.email }}</template>
          </template>
        </Column>
        <Column field="rol" header="Rol" sortable>
          <template #body="{ data }">
            <Skeleton v-if="loading" width="5rem" height="1.5rem" borderRadius="6px" />
            <Tag v-else :value="rolLabel(data.rol)" :severity="rolSeverity(data.rol)" />
          </template>
        </Column>
        <Column field="estado_nombre" header="Estado" sortable>
          <template #body="{ data }">
            <Skeleton v-if="loading" width="55%" height="1.25rem" />
            <template v-else>{{ data.estado_nombre || 'Nacional' }}</template>
          </template>
        </Column>
        <Column field="is_active" header="Activo" sortable>
          <template #body="{ data }">
            <Skeleton v-if="loading" width="5rem" height="1.5rem" borderRadius="6px" />
            <Tag
              v-else
              :value="data.is_active ? 'Activo' : 'Inactivo'"
              :severity="data.is_active ? 'success' : 'danger'"
            />
          </template>
        </Column>
        <Column v-if="auth.tieneRol(ROL_NACIONAL)" header="Acciones" style="width: 10rem">
          <template #body="{ data }">
            <Skeleton v-if="loading" width="8rem" height="1.5rem" borderRadius="6px" />
            <template v-else>
              <Button
                icon="pi pi-pencil"
                severity="secondary"
                text
                rounded
                size="small"
                @click="openEdit(data)"
                v-tooltip.top="'Editar'"
              />
              <Button
                v-if="data.is_active"
                icon="pi pi-ban"
                severity="danger"
                text
                rounded
                size="small"
                @click="confirmDeactivate(data)"
                v-tooltip.top="'Desactivar'"
              />
              <Button
                v-if="!data.is_active"
                icon="pi pi-check-circle"
                severity="success"
                text
                rounded
                size="small"
                @click="confirmActivate(data)"
                v-tooltip.top="'Reactivar'"
              />
              <Button
                icon="pi pi-key"
                severity="info"
                text
                rounded
                size="small"
                @click="confirmResetPassword(data)"
                v-tooltip.top="'Resetear contraseña'"
              />
            </template>
          </template>
        </Column>
      </DataTable>
    </div>

    <!-- Creación: Stepper 2 pasos -->
    <Dialog
      v-model:visible="showDialog"
      :header="'Nuevo usuario'"
      :modal="true"
      :style="{ width: '550px' }"
      :closable="true"
      :draggable="false"
      v-if="isCreating"
    >
      <Message v-if="errorMessage" severity="error" :closable="false" class="!mb-4 !text-xs">
        {{ errorMessage }}
      </Message>

      <Stepper :value="activeStep" linear>
        <StepList>
          <Step :value="1">Información</Step>
          <Step :value="2">Confirmar</Step>
        </StepList>

        <StepPanels>
          <StepPanel :value="1">
            <div class="grid grid-cols-2 gap-4 pt-4">
              <div class="flex flex-col gap-1.5">
                <label for="first_name" class="text-sm font-semibold">Nombre</label>
                <InputText
                  id="first_name"
                  v-model="form.first_name"
                  class="w-full"
                  :class="{ 'p-invalid': submitted && !form.first_name }"
                />
                <small
                  v-if="submitted && !form.first_name"
                  class="text-xs text-red-500 dark:text-red-400"
                >
                  El nombre es requerido
                </small>
              </div>

              <div class="flex flex-col gap-1.5">
                <label for="last_name" class="text-sm font-semibold">Apellido</label>
                <InputText
                  id="last_name"
                  v-model="form.last_name"
                  class="w-full"
                  :class="{ 'p-invalid': submitted && !form.last_name }"
                />
                <small
                  v-if="submitted && !form.last_name"
                  class="text-xs text-red-500 dark:text-red-400"
                >
                  El apellido es requerido
                </small>
              </div>

              <div class="flex flex-col gap-1.5 col-span-2">
                <label for="email" class="text-sm font-semibold">Correo</label>
                <InputText
                  id="email"
                  v-model="form.email"
                  type="email"
                  class="w-full"
                  :class="{ 'p-invalid': submitted && !form.email }"
                />
                <small
                  v-if="submitted && !form.email"
                  class="text-xs text-red-500 dark:text-red-400"
                >
                  El correo es requerido
                </small>
              </div>

              <div class="flex flex-col gap-1.5">
                <label for="rol" class="text-sm font-semibold">Rol</label>
                <Dropdown
                  id="rol"
                  v-model="form.rol"
                  :options="ROLES"
                  optionLabel="label"
                  optionValue="value"
                  placeholder="Seleccionar rol"
                  class="w-full"
                  :class="{ 'p-invalid': submitted && !form.rol }"
                />
                <small v-if="submitted && !form.rol" class="text-xs text-red-500 dark:text-red-400">
                  El rol es requerido
                </small>
              </div>

              <div v-if="form.rol && isEstatal(form.rol)" class="flex flex-col gap-1.5">
                <label for="estado" class="text-sm font-semibold">Estado</label>
                <Dropdown
                  id="estado"
                  v-model="form.estado_id"
                  :options="estados"
                  optionLabel="nombre"
                  optionValue="id"
                  placeholder="Seleccionar estado"
                  class="w-full"
                  :class="{
                    'p-invalid': submitted && !form.estado_id && isEstatal(form.rol),
                  }"
                />
                <small
                  v-if="submitted && !form.estado_id && isEstatal(form.rol)"
                  class="text-xs text-red-500 dark:text-red-400"
                >
                  El estado es requerido para este rol
                </small>
              </div>
            </div>
          </StepPanel>

          <StepPanel :value="2">
            <div class="pt-4 space-y-3">
              <p class="text-sm text-muted-color font-semibold mb-4">
                Revisa los datos antes de crear:
              </p>
              <div
                class="flex justify-between py-1.5 border-b border-surface-100 dark:border-surface-700"
              >
                <span class="text-sm text-muted-color">Nombre</span>
                <span class="text-sm font-medium">{{ form.first_name }} {{ form.last_name }}</span>
              </div>
              <div
                class="flex justify-between py-1.5 border-b border-surface-100 dark:border-surface-700"
              >
                <span class="text-sm text-muted-color">Correo</span>
                <span class="text-sm font-medium">{{ form.email }}</span>
              </div>
              <div
                class="flex justify-between py-1.5 border-b border-surface-100 dark:border-surface-700"
              >
                <span class="text-sm text-muted-color">Rol</span>
                <span class="text-sm font-medium">{{ rolLabelForm }}</span>
              </div>
              <div
                v-if="isEstatal(form.rol)"
                class="flex justify-between py-1.5 border-b border-surface-100 dark:border-surface-700"
              >
                <span class="text-sm text-muted-color">Estado</span>
                <span class="text-sm font-medium">{{ estadoNombreForm }}</span>
              </div>
              <div class="mt-4 p-3 bg-card-hover rounded-md">
                <p class="text-xs text-muted-color">
                  <i class="pi pi-info-circle mr-1" />
                  El usuario y la contraseña se generarán automáticamente.
                </p>
              </div>
            </div>
          </StepPanel>
        </StepPanels>
      </Stepper>

      <template #footer>
        <div class="flex justify-between w-full">
          <div>
            <Button
              v-if="activeStep === 1"
              label="Cancelar"
              severity="secondary"
              @click="showDialog = false"
            />
            <Button
              v-if="activeStep === 2"
              label="Atrás"
              severity="secondary"
              icon="pi pi-arrow-left"
              @click="activeStep = 1"
            />
          </div>
          <div>
            <Button
              v-if="activeStep === 1"
              label="Siguiente"
              icon="pi pi-arrow-right"
              iconPos="right"
              @click="goToStep2"
            />
            <Button
              v-if="activeStep === 2"
              label="Crear usuario"
              icon="pi pi-check"
              @click="createUser"
            />
          </div>
        </div>
      </template>
    </Dialog>

    <!-- Edición: formulario simple -->
    <Dialog
      v-model:visible="showDialog"
      :header="'Editar usuario'"
      :modal="true"
      :style="{ width: '550px' }"
      :closable="true"
      :draggable="false"
      v-else
    >
      <form @submit.prevent="updateUser">
        <Message v-if="errorMessage" severity="error" :closable="false" class="!mb-4 !text-xs">
          {{ errorMessage }}
        </Message>

        <div class="grid grid-cols-2 gap-4">
          <div class="flex flex-col gap-1.5">
            <label for="edit-username" class="text-sm font-semibold">Usuario</label>
            <InputText
              id="edit-username"
              :model-value="editingUser?.username"
              class="w-full"
              disabled
            />
          </div>

          <div class="flex flex-col gap-1.5">
            <label for="edit-email" class="text-sm font-semibold">Correo</label>
            <InputText
              id="edit-email"
              v-model="form.email"
              type="email"
              class="w-full"
              :class="{ 'p-invalid': submitted && !form.email }"
            />
            <small v-if="submitted && !form.email" class="text-xs text-red-500 dark:text-red-400">
              El correo es requerido
            </small>
          </div>

          <div class="flex flex-col gap-1.5">
            <label for="edit-first_name" class="text-sm font-semibold">Nombre</label>
            <InputText
              id="edit-first_name"
              v-model="form.first_name"
              class="w-full"
              :class="{ 'p-invalid': submitted && !form.first_name }"
            />
            <small
              v-if="submitted && !form.first_name"
              class="text-xs text-red-500 dark:text-red-400"
            >
              El nombre es requerido
            </small>
          </div>

          <div class="flex flex-col gap-1.5">
            <label for="edit-last_name" class="text-sm font-semibold">Apellido</label>
            <InputText
              id="edit-last_name"
              v-model="form.last_name"
              class="w-full"
              :class="{ 'p-invalid': submitted && !form.last_name }"
            />
            <small
              v-if="submitted && !form.last_name"
              class="text-xs text-red-500 dark:text-red-400"
            >
              El apellido es requerido
            </small>
          </div>

          <div class="flex flex-col gap-1.5">
            <label for="edit-rol" class="text-sm font-semibold">Rol</label>
            <Dropdown
              id="edit-rol"
              v-model="form.rol"
              :options="ROLES"
              optionLabel="label"
              optionValue="value"
              placeholder="Seleccionar rol"
              class="w-full"
            />
          </div>

          <div v-if="form.rol && isEstatal(form.rol)" class="flex flex-col gap-1.5">
            <label for="edit-estado" class="text-sm font-semibold">Estado</label>
            <Dropdown
              id="edit-estado"
              v-model="form.estado_id"
              :options="estados"
              optionLabel="nombre"
              optionValue="id"
              placeholder="Seleccionar estado"
              class="w-full"
            />
          </div>
        </div>
      </form>

      <template #footer>
        <Button label="Cancelar" severity="secondary" @click="showDialog = false" />
        <Button label="Guardar" @click="updateUser" />
      </template>
    </Dialog>

    <CredentialModal
      v-model:visible="showCredentialsDialog"
      header="Usuario creado"
      successMessage="Usuario creado exitosamente"
      :fullName="`${createdCredentials.firstName} ${createdCredentials.lastName}`"
      :username="createdCredentials.username"
      :password="createdCredentials.password"
      :copyText="createCopyText"
    />

    <ConfirmDialog
      v-model:visible="showDeactivateDialog"
      header="Desactivar usuario"
      :message="`¿Estás seguro de desactivar al usuario ${userToToggle?.first_name} ${userToToggle?.last_name}?`"
      confirmLabel="Desactivar"
      confirmSeverity="danger"
      @confirm="deactivateUser"
    />
    <ConfirmDialog
      v-model:visible="showActivateDialog"
      header="Reactivar usuario"
      :message="`¿Estás seguro de reactivar al usuario ${userToToggle?.first_name} ${userToToggle?.last_name}?`"
      confirmLabel="Reactivar"
      confirmSeverity="success"
      @confirm="activateUser"
    />
    <ConfirmDialog
      v-model:visible="showResetConfirmDialog"
      header="Resetear contraseña"
      :message="`¿Estás seguro de resetear la contraseña de ${userToReset?.first_name} ${userToReset?.last_name}?`"
      confirmLabel="Resetear"
      confirmSeverity="info"
      @confirm="resetPassword"
    />

    <CredentialModal
      v-model:visible="showResetCredentialsDialog"
      header="Contraseña reseteada"
      icon="pi pi-key"
      iconColorClass="text-blue-600 dark:text-blue-400"
      successMessage="Contraseña restablecida exitosamente"
      :fullName="`${userToReset?.first_name} ${userToReset?.last_name}`"
      :username="userToReset?.username ?? ''"
      :password="resetResult"
      :copyText="resetCopyText"
      warningText="Copia la contraseña ahora. No se podrá mostrar de nuevo."
    />
  </div>
</template>

<style scoped></style>
