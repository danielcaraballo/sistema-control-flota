import { createApp } from 'vue'
import { createPinia } from 'pinia'
import PrimeVue from 'primevue/config'
import Aura from '@primeuix/themes/aura'
import { definePreset, updateSurfacePalette } from '@primeuix/themes'
import ToastService from 'primevue/toastservice'
import Tooltip from 'primevue/tooltip'
import 'primeicons/primeicons.css'
import './assets/main.css'

import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth'

const ScfPreset = definePreset(Aura, {
  semantic: {
    fontFamily: "'Poppins', sans-serif",
    primary: {
      50: '{sky.50}',
      100: '{sky.100}',
      200: '{sky.200}',
      300: '{sky.300}',
      400: '{sky.400}',
      500: '{sky.500}',
      600: '{sky.600}',
      700: '{sky.700}',
      800: '{sky.800}',
      900: '{sky.900}',
      950: '{sky.950}',
    },
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

updateSurfacePalette({
  50: '{slate.50}',
  100: '{slate.100}',
  200: '{slate.200}',
  300: '{slate.300}',
  400: '{slate.400}',
  500: '{slate.500}',
  600: '{slate.600}',
  700: '{slate.700}',
  800: '{slate.800}',
  900: '{slate.900}',
  950: '{slate.950}',
})

async function startApp() {
  if (auth.token) {
    await auth.initialize()
  }
  app.mount('#app')
}

startApp()
