<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import Message from 'primevue/message'
import Checkbox from 'primevue/checkbox'
import FloatLabel from 'primevue/floatlabel'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const credential = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)
const rememberMe = ref(localStorage.getItem('remember_me') === 'true')
const showCard = ref(false)
const submitted = ref(false)

const credentialError = computed(() => {
  if (!submitted.value) return ''
  return credential.value.trim() ? '' : 'El usuario o correo es requerido'
})

const passwordError = computed(() => {
  if (!submitted.value) return ''
  return password.value ? '' : 'La contraseña es requerida'
})

const formValid = computed(() => {
  return credential.value.trim() && password.value
})

if (rememberMe.value) {
  credential.value = localStorage.getItem('remembered_username') || ''
}

onMounted(() => {
  showCard.value = true
})

async function handleLogin() {
  submitted.value = true
  error.value = ''

  if (!formValid.value) return

  loading.value = true
  try {
    await auth.login(credential.value, password.value)
    if (rememberMe.value) {
      localStorage.setItem('remember_me', 'true')
      localStorage.setItem('remembered_username', credential.value)
    } else {
      localStorage.removeItem('remember_me')
      localStorage.removeItem('remembered_username')
    }
    const redirect = route.query.redirect || '/'
    router.push(redirect)
  } catch (err) {
    if (err.response) {
      error.value =
        err.response.data?.detail || `Error ${err.response.status}: credenciales inválidas`
    } else if (err.request) {
      error.value = 'No se pudo conectar con el servidor. Verifica tu conexión.'
    } else {
      error.value = 'Error al iniciar sesión'
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="flex min-h-screen">
    <!-- Left panel: Branding -->
    <div
      class="hidden lg:flex w-3/5 bg-primary p-12 flex-col items-center justify-center relative overflow-hidden"
    >
      <div class="absolute top-[-80px] left-[-80px] w-64 h-64 rounded-full bg-white/10" />
      <div class="absolute bottom-[-120px] right-[-60px] w-80 h-80 rounded-full bg-white/5" />
      <div class="absolute top-1/2 right-[-100px] w-48 h-48 rounded-full bg-white/8" />

      <div class="text-center relative z-10">
        <i class="pi pi-car text-7xl text-white mb-4 block" />
        <h1 class="text-white text-4xl font-bold m-0">SCF</h1>
        <p class="text-white/70 text-lg mt-2">Sistema de Control de Flota</p>
      </div>

      <p class="absolute bottom-8 text-white/40 text-sm">&copy; 2026 SCF</p>
    </div>

    <!-- Right panel: Form -->
    <div
      class="w-full lg:w-2/5 flex items-center justify-center px-6 py-10 sm:px-12 bg-[var(--scf-page-bg)]"
    >
      <div
        :class="['w-full max-w-md', showCard ? 'animate-fade-in-up' : 'opacity-0 translate-y-6']"
      >
        <!-- Mobile logo -->
        <div class="lg:hidden text-center mb-8">
          <i class="pi pi-car text-4xl text-primary mb-2 block" />
          <h1 class="text-2xl font-bold text-surface-900 dark:text-surface-0 m-0">SCF</h1>
          <p class="text-sm text-muted-color mt-1">Sistema de Control de Flota</p>
        </div>

        <h2 class="text-2xl font-bold text-center text-surface-900 dark:text-surface-0 m-0">
          Iniciar sesión
        </h2>
        <p class="text-sm text-muted-color text-center mt-1 mb-5">
          Ingresa tus credenciales para acceder al sistema
        </p>

        <form @submit.prevent="handleLogin" class="relative">
          <Transition name="fade">
            <Message
              v-if="error"
              severity="error"
              :closable="true"
              class="mb-4 text-sm"
              @close="error = ''"
            >
              {{ error }}
            </Message>
          </Transition>

          <div :class="{ 'opacity-40 pointer-events-none': loading }" class="transition-opacity">
            <div class="mb-5">
              <FloatLabel variant="on">
                <InputText
                  id="credential"
                  v-model="credential"
                  class="w-full"
                  :invalid="!!credentialError"
                  :disabled="loading"
                  autofocus
                  autocomplete="username"
                />
                <label for="credential">Usuario o correo</label>
              </FloatLabel>
              <small v-if="credentialError" class="text-red-500 block mt-1">{{
                credentialError
              }}</small>
            </div>

            <div class="mb-5">
              <FloatLabel variant="on">
                <Password
                  id="password"
                  v-model="password"
                  :feedback="false"
                  toggleMask
                  fluid
                  :disabled="loading"
                  :invalid="!!passwordError"
                />
                <label for="password">Contraseña</label>
              </FloatLabel>
              <small v-if="passwordError" class="text-red-500 block mt-1">{{
                passwordError
              }}</small>
            </div>

            <div class="flex items-center mb-5">
              <Checkbox v-model="rememberMe" :binary="true" input-id="remember" />
              <label
                for="remember"
                class="text-sm cursor-pointer text-surface-700 dark:text-surface-300 ml-2"
              >
                Recordar sesión
              </label>
            </div>
          </div>

          <Button
            type="submit"
            label="Iniciar sesión"
            icon="pi pi-sign-in"
            class="w-full"
            :loading="loading"
          />

          <div v-if="loading" class="absolute inset-0 cursor-wait rounded-xl" />
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(24px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in-up {
  animation: fadeInUp 0.4s ease-out forwards;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
