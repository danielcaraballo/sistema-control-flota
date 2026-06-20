<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'
import { ROLES, ESTATAL_ROLES, rolLabel, rolSeverity } from '@/utils/roles'
import Button from 'primevue/button'
import Column from 'primevue/column'
import DataTable from 'primevue/datatable'
import Dialog from 'primevue/dialog'
import Dropdown from 'primevue/dropdown'
import InputText from 'primevue/inputtext'
import Message from 'primevue/message'
import Password from 'primevue/password'
import Tag from 'primevue/tag'
import PageHeader from '@/components/PageHeader.vue'

const auth = useAuthStore()
const usuarios = ref([])
const estados = ref([])
const loading = ref(true)
const showDialog = ref(false)
const editingUser = ref(null)
const submitted = ref(false)
const errorMessage = ref('')

const form = ref({
  username: '',
  email: '',
  password: '',
  first_name: '',
  last_name: '',
  rol: null,
  estado_id: null,
  gerencia_id: null,
})

async function loadEstados() {
  try {
    const { data } = await api.get('/organizacion/estados/')
    estados.value = data
  } catch {}
}

async function loadUsuarios() {
  loading.value = true
  try {
    const { data } = await api.get('/usuarios/')
    usuarios.value = data
  } catch {
  } finally {
    loading.value = false
  }
}

function openNew() {
  editingUser.value = null
  errorMessage.value = ''
  form.value = {
    username: '',
    email: '',
    password: '',
    first_name: '',
    last_name: '',
    rol: null,
    estado_id: null,
    gerencia_id: null,
  }
  submitted.value = false
  showDialog.value = true
}

function openEdit(user) {
  editingUser.value = user
  errorMessage.value = ''
  form.value = {
    username: user.username,
    email: user.email,
    password: '',
    first_name: user.first_name,
    last_name: user.last_name,
    rol: user.rol,
    estado_id: user.estado?.id ?? user.estado ?? null,
    gerencia_id: user.gerencia?.id ?? user.gerencia ?? null,
  }
  submitted.value = false
  showDialog.value = true
}

function validateForm() {
  return (
    (!!editingUser.value || form.value.username) &&
    form.value.email &&
    (!!editingUser.value || form.value.password) &&
    form.value.first_name &&
    form.value.last_name &&
    form.value.rol &&
    (!ESTATAL_ROLES.includes(form.value.rol) || form.value.estado_id)
  )
}

async function saveUser() {
  submitted.value = true
  errorMessage.value = ''

  if (!validateForm()) return

  try {
    if (editingUser.value) {
      const payload = {
        email: form.value.email,
        first_name: form.value.first_name,
        last_name: form.value.last_name,
        rol: form.value.rol,
        estado_id: form.value.estado_id,
        gerencia_id: form.value.gerencia_id,
      }
      await api.put(`/usuarios/${editingUser.value.id}`, payload)
    } else {
      await api.post('/usuarios/', form.value)
    }
    showDialog.value = false
    await loadUsuarios()
  } catch (err) {
    errorMessage.value = err.response?.data?.detail || 'Error al guardar el usuario'
  }
}

async function deactivateUser(user) {
  try {
    await api.delete(`/usuarios/${user.id}`)
    await loadUsuarios()
  } catch {}
}

onMounted(() => {
  loadUsuarios()
  loadEstados()
})
</script>

<template>
  <div class="max-w-[1200px]">
    <PageHeader title="Usuarios" subtitle="Gestión de usuarios del sistema" icon="pi pi-users">
      <Button
        v-if="auth.isGerenteNacional"
        label="Nuevo usuario"
        icon="pi pi-plus"
        @click="openNew"
      />
    </PageHeader>

    <div class="border border-surface-200 rounded-md bg-surface-0 overflow-hidden">
      <DataTable
        :value="usuarios"
        :loading="loading"
        stripedRows
        paginator
        :rows="10"
        :rowsPerPageOptions="[10, 25, 50]"
        sortField="username"
        :sortOrder="1"
      >
        <Column field="username" header="Usuario" sortable />
        <Column field="first_name" header="Nombre" sortable>
          <template #body="{ data }"> {{ data.first_name }} {{ data.last_name }} </template>
        </Column>
        <Column field="email" header="Correo" sortable />
        <Column field="rol" header="Rol" sortable>
          <template #body="{ data }">
            <Tag :value="rolLabel(data.rol)" :severity="rolSeverity(data.rol)" />
          </template>
        </Column>
        <Column field="estado_nombre" header="Estado" sortable>
          <template #body="{ data }">
            {{ data.estado_nombre || 'Nacional' }}
          </template>
        </Column>
        <Column field="gerencia_nombre" header="Gerencia" sortable>
          <template #body="{ data }">
            {{ data.gerencia_nombre || '—' }}
          </template>
        </Column>
        <Column field="is_active" header="Activo" sortable>
          <template #body="{ data }">
            <Tag
              :value="data.is_active ? 'Activo' : 'Inactivo'"
              :severity="data.is_active ? 'success' : 'danger'"
            />
          </template>
        </Column>
        <Column v-if="auth.isGerenteNacional" header="Acciones" style="width: 10rem">
          <template #body="{ data }">
            <Button
              icon="pi pi-pencil"
              severity="secondary"
              text
              rounded
              @click="openEdit(data)"
              v-tooltip.top="'Editar'"
            />
            <Button
              v-if="data.is_active"
              icon="pi pi-ban"
              severity="danger"
              text
              rounded
              @click="deactivateUser(data)"
              v-tooltip.top="'Desactivar'"
            />
          </template>
        </Column>
      </DataTable>
    </div>

    <Dialog
      v-model:visible="showDialog"
      :header="editingUser ? 'Editar usuario' : 'Nuevo usuario'"
      :modal="true"
      :style="{ width: '550px' }"
      :closable="true"
    >
      <form @submit.prevent="saveUser">
        <Message v-if="errorMessage" severity="error" :closable="false" class="!mb-4 !text-xs">
          {{ errorMessage }}
        </Message>

        <div class="grid grid-cols-2 gap-4">
          <div class="flex flex-col gap-1.5">
            <label for="username" class="text-sm font-semibold">Usuario</label>
            <InputText
              id="username"
              v-model="form.username"
              class="w-full"
              :disabled="!!editingUser"
            />
            <small v-if="!editingUser" class="text-xs text-muted-color">
              Se genera automáticamente a partir del nombre
            </small>
            <small
              v-if="submitted && !form.username && !editingUser"
              class="text-xs text-red-500 dark:text-red-400"
            >
              El usuario es requerido
            </small>
          </div>

          <div class="flex flex-col gap-1.5">
            <label for="email" class="text-sm font-semibold">Correo</label>
            <InputText
              id="email"
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
            <label for="password" class="text-sm font-semibold">Contraseña</label>
            <Password
              id="password"
              v-model="form.password"
              :feedback="false"
              class="w-full"
              pt:input:class="w-full"
              :required="!editingUser"
              :placeholder="editingUser ? 'Dejar vacío para no cambiar' : ''"
              toggleMask
            />
            <small
              v-if="submitted && !form.password && !editingUser"
              class="text-xs text-red-500 dark:text-red-400"
            >
              La contraseña es requerida
            </small>
          </div>

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

          <div v-if="form.rol && ESTATAL_ROLES.includes(form.rol)" class="flex flex-col gap-1.5">
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
                'p-invalid': submitted && !form.estado_id && ESTATAL_ROLES.includes(form.rol),
              }"
            />
            <small
              v-if="submitted && !form.estado_id && ESTATAL_ROLES.includes(form.rol)"
              class="text-xs text-red-500 dark:text-red-400"
            >
              El estado es requerido para este rol
            </small>
          </div>
        </div>
      </form>

      <template #footer>
        <Button label="Cancelar" severity="secondary" @click="showDialog = false" />
        <Button :label="editingUser ? 'Guardar' : 'Crear'" @click="saveUser" />
      </template>
    </Dialog>
  </div>
</template>
