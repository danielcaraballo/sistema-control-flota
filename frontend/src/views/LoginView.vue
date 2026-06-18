<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    await auth.login(email.value, password.value)
    router.push('/')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al iniciar sesión'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-container">
    <div class="login-card">
      <h1>SCF</h1>
      <p class="subtitle">Sistema de Control de Flota</p>
      <form @submit.prevent="handleLogin">
        <div v-if="error" class="error-message">{{ error }}</div>
        <div class="form-group">
          <label for="email">Correo corporativo</label>
          <input id="email" v-model="email" type="email" required placeholder="usuario@corp.com" />
        </div>
        <div class="form-group">
          <label for="password">Contraseña</label>
          <input id="password" v-model="password" type="password" required />
        </div>
        <button type="submit" class="btn-primary" :disabled="loading">
          {{ loading ? 'Ingresando...' : 'Iniciar sesión' }}
        </button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  width: 100%;
  max-width: 400px;
  padding: 1rem;
}

.login-card {
  background: #fff;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.login-card h1 {
  margin: 0 0 0.25rem;
  text-align: center;
  color: #1a1a2e;
}

.subtitle {
  text-align: center;
  color: #666;
  margin-bottom: 2rem;
}

.error-message {
  background: #fde8e8;
  color: #c53030;
  padding: 0.75rem;
  border-radius: 4px;
  margin-bottom: 1rem;
  font-size: 0.875rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.375rem;
  font-size: 0.875rem;
  color: #333;
}

.form-group input {
  width: 100%;
  padding: 0.625rem 0.75rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 0.875rem;
  box-sizing: border-box;
}

.btn-primary {
  width: 100%;
  padding: 0.75rem;
  background-color: #1a1a2e;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 0.5rem;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary:hover:not(:disabled) {
  background-color: #16213e;
}
</style>
