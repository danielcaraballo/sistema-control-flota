import axios from 'axios'
import router from '@/router'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

let refreshPromise = null

function redirectLogin() {
  router.push('/login')
}

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status !== 401 || originalRequest._retry) {
      return Promise.reject(error)
    }

    const refreshToken = localStorage.getItem('refresh_token')
    if (!refreshToken) {
      const { useAuthStore } = await import('@/stores/auth')
      useAuthStore().logout()
      redirectLogin()
      return Promise.reject(error)
    }

    originalRequest._retry = true

    if (!refreshPromise) {
      refreshPromise = (async () => {
        try {
          const { data } = await axios.post(`${api.defaults.baseURL}/auth/refresh`, {
            refresh: refreshToken,
          })
          localStorage.setItem('access_token', data.access)
          return data.access
        } catch {
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          const { useAuthStore } = await import('@/stores/auth')
          useAuthStore().logout()
          redirectLogin()
          return null
        }
      })().finally(() => {
        refreshPromise = null
      })
    }

    const newToken = await refreshPromise
    if (!newToken) return Promise.reject(error)

    originalRequest.headers.Authorization = `Bearer ${newToken}`
    return api(originalRequest)
  },
)

export default api
