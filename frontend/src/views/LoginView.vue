<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const credential = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    await auth.login(credential.value, password.value)
    router.push('/')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al iniciar sesión'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-wrapper">
    <Card class="login-card">
      <template #title>
        <div class="login-header">
          <i class="pi pi-car" style="font-size: 2rem; color: var(--p-primary-color)"></i>
          <h1>SCF</h1>
        </div>
      </template>
      <template #subtitle>
        Sistema de Control de Flota
      </template>
      <template #content>
        <form @submit.prevent="handleLogin">
          <Message v-if="error" severity="error" :closable="false" class="mb-3">
            {{ error }}
          </Message>

          <div class="field mb-3">
            <label for="credential">Correo o usuario</label>
            <InputText
              id="credential"
              v-model="credential"
              type="text"
              placeholder="usuario o correo"
              class="w-full"
              :disabled="loading"
            />
          </div>

          <div class="field mb-4">
            <label for="password">Contraseña</label>
            <Password
              id="password"
              v-model="password"
              :feedback="false"
              placeholder="Contraseña"
              class="w-full"
              :input-style="{ width: '100%' }"
              :disabled="loading"
              toggleMask
            />
          </div>

          <Button
            type="submit"
            label="Iniciar sesión"
            class="w-full"
            :loading="loading"
          />
        </form>
      </template>
    </Card>
  </div>
</template>

<style scoped>
.login-wrapper {
  width: 100%;
  max-width: 420px;
  padding: 1rem;
}

.login-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.login-header h1 {
  margin: 0;
  font-size: 1.5rem;
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

.mb-3 {
  margin-bottom: 1rem;
}

.mb-4 {
  margin-bottom: 1.5rem;
}

.w-full {
  width: 100%;
}

:deep(.p-password input) {
  width: 100%;
}
</style>
