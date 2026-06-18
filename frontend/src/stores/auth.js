import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(null)
  const isAuthenticated = ref(false)

  async function login(email, password) {
    // TODO: Implementar llamada a API Django Ninja
  }

  function logout() {
    user.value = null
    token.value = null
    isAuthenticated.value = false
  }

  return { user, token, isAuthenticated, login, logout }
})
