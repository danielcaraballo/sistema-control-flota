import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import api from '@/services/api'
import { tieneRolMinimo, esEstatal, ROLES } from '@/utils/roles'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('access_token') || null)
  const isAuthenticated = ref(!!token.value)
  const loading = ref(!!token.value)

  let _resolveInit = null
  const initialized = new Promise((resolve) => {
    _resolveInit = resolve
  })

  const rol = computed(() => user.value?.rol || null)
  const rolData = computed(() => ROLES.find((r) => r.value === rol.value))
  const esEstatalValue = computed(() => esEstatal(rol.value))

  function tieneRol(rolMinimo) {
    return tieneRolMinimo(rol.value, rolMinimo)
  }

  async function login(credential, password) {
    const { data } = await api.post('/auth/login', { username: credential, password })
    token.value = data.access
    user.value = data.user
    isAuthenticated.value = true
    localStorage.setItem('access_token', data.access)
    localStorage.setItem('refresh_token', data.refresh)
    return data
  }

  async function fetchMe() {
    try {
      const { data } = await api.get('/auth/me')
      user.value = data
      return data
    } catch {
      logout()
      return null
    }
  }

  function logout() {
    user.value = null
    token.value = null
    isAuthenticated.value = false
    loading.value = false
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  async function initialize() {
    if (!token.value) {
      _resolveInit()
      return
    }
    loading.value = true
    await fetchMe()
    loading.value = false
    _resolveInit()
  }

  return {
    user,
    token,
    isAuthenticated,
    loading,
    initialized,
    rol,
    rolData,
    esEstatal: esEstatalValue,
    tieneRol,
    login,
    fetchMe,
    logout,
    initialize,
  }
})
