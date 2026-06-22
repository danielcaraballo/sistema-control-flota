import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import api from '@/services/api'
import { tieneRolMinimo, esEstatal, ROLES } from '@/utils/roles'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('access_token') || null)
  const isAuthenticated = ref(!!token.value)

  const rol = computed(() => user.value?.rol || null)
  const rolData = computed(() => ROLES.find(r => r.value === rol.value))
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
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  function initialize() {
    if (token.value) {
      fetchMe()
    }
  }

  return {
    user,
    token,
    isAuthenticated,
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
