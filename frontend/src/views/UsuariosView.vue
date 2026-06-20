<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'
import Button from 'primevue/button'
import Card from 'primevue/card'
import Column from 'primevue/column'
import DataTable from 'primevue/datatable'
import Dialog from 'primevue/dialog'
import Dropdown from 'primevue/dropdown'
import InputText from 'primevue/inputtext'
import Message from 'primevue/message'
import Password from 'primevue/password'
import Tag from 'primevue/tag'

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

const roles = [
  { label: 'Gerente Nacional', value: 'gerente_nacional' },
  { label: 'Analista Nacional', value: 'analista_nacional' },
  { label: 'Responsable Estatal', value: 'responsable_estatal' },
  { label: 'Mecánico', value: 'mecanico' },
]

const ESTATAL_ROLES = ['responsable_estatal', 'mecanico']

async function loadEstados() {
  try {
    const { data } = await api.get('/organizacion/estados/')
    estados.value = data
  } catch (err) {
    console.error(err)
  }
}

async function loadUsuarios() {
  loading.value = true
  try {
    const { data } = await api.get('/usuarios/')
    usuarios.value = data
  } catch (err) {
    console.error(err)
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
    estado_id: user.estado,
    gerencia_id: user.gerencia,
  }
  submitted.value = false
  showDialog.value = true
}

async function saveUser() {
  submitted.value = true
  errorMessage.value = ''

  if (!form.value.rol) return

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
      await api.post('/usuarios/', {
        ...form.value,
        rol: form.value.rol.value || form.value.rol,
      })
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
  } catch (err) {
    console.error(err)
  }
}

const rolSeverity = (rol) => ({
  gerente_nacional: 'danger',
  analista_nacional: 'warn',
  responsable_estatal: 'info',
  mecanico: 'success',
}[rol] || 'info')

const rolLabel = (rol) => ({
  gerente_nacional: 'Gerente Nacional',
  analista_nacional: 'Analista Nacional',
  responsable_estatal: 'Responsable Estatal',
  mecanico: 'Mecánico',
}[rol] || rol)

onMounted(() => {
  loadUsuarios()
  loadEstados()
})
</script>

<template>
  <div class="usuarios-page">
    <div class="page-header">
      <h1>Usuarios</h1>
      <Button
        v-if="auth.isGerenteNacional"
        label="Nuevo usuario"
        icon="pi pi-plus"
        @click="openNew"
      />
    </div>

    <Card>
      <template #content>
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
            <template #body="{ data }">
              {{ data.first_name }} {{ data.last_name }}
            </template>
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
          <Column field="is_active" header="Estado" sortable>
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
      </template>
    </Card>

    <Dialog
      v-model:visible="showDialog"
      :header="editingUser ? 'Editar usuario' : 'Nuevo usuario'"
      :modal="true"
      :style="{ width: '550px' }"
      :closable="true"
    >
      <form @submit.prevent="saveUser">
        <Message v-if="errorMessage" severity="error" :closable="false" class="mb-3">
          {{ errorMessage }}
        </Message>

        <div class="form-grid">
          <div class="field">
            <label for="username">Usuario</label>
            <InputText
              id="username"
              v-model="form.username"
              class="w-full"
              :disabled="!!editingUser"
            />
            <small v-if="!editingUser" class="text-muted">
              Se genera automáticamente a partir del nombre
            </small>
          </div>

          <div class="field">
            <label for="email">Correo</label>
            <InputText
              id="email"
              v-model="form.email"
              type="email"
              class="w-full"
              :class="{ 'p-invalid': submitted && !form.email }"
            />
          </div>

          <div class="field">
            <label for="password">Contraseña</label>
            <Password
              id="password"
              v-model="form.password"
              :feedback="false"
              class="w-full"
              :input-style="{ width: '100%' }"
              :required="!editingUser"
              :placeholder="editingUser ? 'Dejar vacío para no cambiar' : ''"
              toggleMask
            />
          </div>

          <div class="field">
            <label for="first_name">Nombre</label>
            <InputText id="first_name" v-model="form.first_name" class="w-full" />
          </div>

          <div class="field">
            <label for="last_name">Apellido</label>
            <InputText id="last_name" v-model="form.last_name" class="w-full" />
          </div>

          <div class="field">
            <label for="rol">Rol</label>
            <Dropdown
              id="rol"
              v-model="form.rol"
              :options="roles"
              optionLabel="label"
              optionValue="value"
              placeholder="Seleccionar rol"
              class="w-full"
              :class="{ 'p-invalid': submitted && !form.rol }"
            />
          </div>

          <div
            v-if="form.rol && ESTATAL_ROLES.includes(form.rol)"
            class="field"
          >
            <label for="estado">Estado</label>
            <Dropdown
              id="estado"
              v-model="form.estado_id"
              :options="estados"
              optionLabel="nombre"
              optionValue="id"
              placeholder="Seleccionar estado"
              class="w-full"
              :class="{ 'p-invalid': submitted && !form.estado_id && ESTATAL_ROLES.includes(form.rol) }"
            />
          </div>
        </div>
      </form>

      <template #footer>
        <Button label="Cancelar" severity="secondary" @click="showDialog = false" />
        <Button
          :label="editingUser ? 'Guardar' : 'Crear'"
          @click="saveUser"
        />
      </template>
    </Dialog>
  </div>
</template>

<style scoped>
.usuarios-page {
  max-width: 1200px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.page-header h1 {
  margin: 0;
  font-size: 1.5rem;
  color: var(--p-text-color);
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}

.field label {
  font-size: 0.875rem;
  font-weight: 500;
}

.w-full {
  width: 100%;
}

:deep(.p-password input) {
  width: 100%;
}
</style>
