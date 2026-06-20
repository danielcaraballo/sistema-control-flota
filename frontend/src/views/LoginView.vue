<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Message from 'primevue/message'
import Password from 'primevue/password'

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
  <div class="w-full flex items-center justify-center">
    <div class="w-full max-w-[420px] px-4">
      <div class="border border-surface-200 rounded-md bg-surface-0">
        <div class="px-6 pt-6 pb-2">
          <div class="flex items-center gap-3 mb-1">
            <i class="pi pi-car text-2xl" style="color: var(--p-primary-color)" />
            <h1 class="m-0 text-xl font-semibold">SCF</h1>
          </div>
          <p class="text-sm text-muted-color mt-1">Sistema de Control de Flota</p>
        </div>
        <div class="px-6 pb-6 pt-4">
          <form @submit.prevent="handleLogin">
            <Message v-if="error" severity="error" :closable="false" class="mb-3 text-xs">
              {{ error }}
            </Message>

            <div class="flex flex-col gap-1.5 mb-3">
              <label for="credential" class="text-sm font-semibold">Correo o usuario</label>
              <InputText
                id="credential"
                v-model="credential"
                type="text"
                placeholder="usuario o correo"
                class="w-full"
                :disabled="loading"
              />
            </div>

            <div class="flex flex-col gap-1.5 mb-5">
              <label for="password" class="text-sm font-semibold">Contraseña</label>
              <Password
                id="password"
                v-model="password"
                :feedback="false"
                placeholder="Contraseña"
                class="w-full"
                pt:input:class="w-full"
                :disabled="loading"
                toggleMask
              />
            </div>

            <Button type="submit" label="Iniciar sesión" class="w-full" :loading="loading" />
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
