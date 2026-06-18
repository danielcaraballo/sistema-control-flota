<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

const auth = useAuthStore()
const usuarios = ref([])
const loading = ref(true)
const showForm = ref(false)
const editingUser = ref(null)
const form = ref({
  username: '',
  email: '',
  password: '',
  first_name: '',
  last_name: '',
  rol: 'mecanico',
  gerencia_id: null,
})

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

function openCreate() {
  editingUser.value = null
  form.value = {
    username: '',
    email: '',
    password: '',
    first_name: '',
    last_name: '',
    rol: 'mecanico',
    gerencia_id: null,
  }
  showForm.value = true
}

function openEdit(user) {
  editingUser.value = user
  form.value = {
    username: user.username,
    email: user.email,
    password: '',
    first_name: user.first_name,
    last_name: user.last_name,
    rol: user.rol,
    gerencia_id: user.gerencia,
  }
  showForm.value = true
}

async function saveUser() {
  try {
    if (editingUser.value) {
      const payload = { ...form.value }
      delete payload.password
      delete payload.username
      if (!payload.password) delete payload.password
      await api.put(`/usuarios/${editingUser.value.id}`, payload)
    } else {
      await api.post('/usuarios/', form.value)
    }
    showForm.value = false
    await loadUsuarios()
  } catch (err) {
    console.error(err)
  }
}

async function deactivateUser(id) {
  if (confirm('¿Desactivar este usuario?')) {
    try {
      await api.delete(`/usuarios/${id}`)
      await loadUsuarios()
    } catch (err) {
      console.error(err)
    }
  }
}

const rolNombre = (rol) => ({
  gerente_nacional: 'Gerente Nacional',
  analista_nacional: 'Analista Nacional',
  responsable_estatal: 'Responsable Estatal',
  mecanico: 'Mecánico',
}[rol] || rol)

onMounted(loadUsuarios)
</script>

<template>
  <div class="usuarios">
    <div class="header">
      <h1>Usuarios</h1>
      <button v-if="auth.isGerenteNacional" class="btn-primary" @click="openCreate">
        + Nuevo usuario
      </button>
    </div>

    <div v-if="loading" class="loading">Cargando...</div>

    <div v-else class="table-container">
      <table>
        <thead>
          <tr>
            <th>Usuario</th>
            <th>Nombre</th>
            <th>Correo</th>
            <th>Rol</th>
            <th>Gerencia</th>
            <th>Estado</th>
            <th v-if="auth.isGerenteNacional">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="u in usuarios" :key="u.id">
            <td>{{ u.username }}</td>
            <td>{{ u.first_name }} {{ u.last_name }}</td>
            <td>{{ u.email }}</td>
            <td>{{ rolNombre(u.rol) }}</td>
            <td>{{ u.gerencia_nombre || '—' }}</td>
            <td>{{ u.is_active ? 'Activo' : 'Inactivo' }}</td>
            <td v-if="auth.isGerenteNacional">
              <button class="btn-sm" @click="openEdit(u)">Editar</button>
              <button class="btn-sm btn-danger" @click="deactivateUser(u.id)" v-if="u.is_active">
                Desactivar
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal Formulario -->
    <div v-if="showForm" class="modal-overlay" @click.self="showForm = false">
      <div class="modal">
        <h2>{{ editingUser ? 'Editar usuario' : 'Nuevo usuario' }}</h2>
        <form @submit.prevent="saveUser">
          <div class="form-grid">
            <div class="form-group">
              <label>Usuario</label>
              <input v-model="form.username" required :disabled="!!editingUser" />
            </div>
            <div class="form-group">
              <label>Correo</label>
              <input v-model="form.email" type="email" required />
            </div>
            <div class="form-group">
              <label>Contraseña</label>
              <input v-model="form.password" type="password" :required="!editingUser" :placeholder="editingUser ? 'Dejar vacío para no cambiar' : ''" />
            </div>
            <div class="form-group">
              <label>Nombre</label>
              <input v-model="form.first_name" />
            </div>
            <div class="form-group">
              <label>Apellido</label>
              <input v-model="form.last_name" />
            </div>
            <div class="form-group">
              <label>Rol</label>
              <select v-model="form.rol">
                <option value="gerente_nacional">Gerente Nacional</option>
                <option value="analista_nacional">Analista Nacional</option>
                <option value="responsable_estatal">Responsable Estatal</option>
                <option value="mecanico">Mecánico</option>
              </select>
            </div>
            <div class="form-group" v-if="form.rol !== 'gerente_nacional' && form.rol !== 'analista_nacional'">
              <label>Gerencia</label>
              <input v-model="form.gerencia_id" type="number" placeholder="ID de gerencia" />
            </div>
          </div>
          <div class="modal-actions">
            <button type="button" class="btn-secondary" @click="showForm = false">Cancelar</button>
            <button type="submit" class="btn-primary">{{ editingUser ? 'Guardar' : 'Crear' }}</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.usuarios {
  max-width: 1200px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.header h1 {
  margin: 0;
  color: #1a1a2e;
}

.loading {
  text-align: center;
  color: #666;
  padding: 2rem;
}

.table-container {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  text-align: left;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #eee;
  font-size: 0.875rem;
}

th {
  background: #f9f9f9;
  color: #666;
  font-weight: 600;
}

.btn-primary {
  padding: 0.5rem 1rem;
  background-color: #1a1a2e;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
}

.btn-sm {
  padding: 0.375rem 0.75rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  background: #fff;
  cursor: pointer;
  font-size: 0.8rem;
  margin-right: 0.375rem;
}

.btn-danger {
  color: #c53030;
  border-color: #c53030;
}

.btn-secondary {
  padding: 0.5rem 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  background: #fff;
  cursor: pointer;
  font-size: 0.875rem;
  margin-right: 0.5rem;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal {
  background: #fff;
  border-radius: 8px;
  padding: 2rem;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal h2 {
  margin: 0 0 1.5rem;
  color: #1a1a2e;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group.full {
  grid-column: 1 / -1;
}

.form-group label {
  font-size: 0.8rem;
  color: #666;
  margin-bottom: 0.25rem;
}

.form-group input,
.form-group select {
  padding: 0.5rem 0.625rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 0.875rem;
}

.modal-actions {
  margin-top: 1.5rem;
  display: flex;
  justify-content: flex-end;
}
</style>
