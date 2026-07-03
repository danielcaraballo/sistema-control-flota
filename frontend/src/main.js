import { createApp } from 'vue'
import { createPinia } from 'pinia'
import PrimeVue from 'primevue/config'
import Aura from '@primevue/themes/aura'
import { definePreset } from '@primevue/themes'
import ToastService from 'primevue/toastservice'
import Tooltip from 'primevue/tooltip'
import 'primeicons/primeicons.css'
import './assets/main.css'

import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth'
import { applyTheme, readInitialTheme } from './composables/useTheme'

const ScfPreset = definePreset(Aura, {
  semantic: {
    fontFamily: "'Poppins', sans-serif",
  },
})

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(PrimeVue, {
  theme: {
    preset: ScfPreset,
    options: {
      darkModeSelector: '.p-dark',
      cssLayer: {
        name: 'primevue',
        order: 'theme, base, primevue, utilities',
      },
    },
  },
  ripple: true,
})

app.use(ToastService)
app.directive('tooltip', Tooltip)

const auth = useAuthStore()

async function startApp() {
  if (auth.token) {
    await auth.initialize()
  }
  applyTheme(readInitialTheme())
  app.mount('#app')
}

startApp()
