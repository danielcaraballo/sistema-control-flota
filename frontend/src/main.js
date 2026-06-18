import { createApp } from 'vue'
import { createPinia } from 'pinia'
import PrimeVue from 'primevue/config'
import Aura from '@primevue/themes/aura'
import 'primeicons/primeicons.css'

import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import Password from 'primevue/password'
import FloatLabel from 'primevue/floatlabel'
import Message from 'primevue/message'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Dialog from 'primevue/dialog'
import Dropdown from 'primevue/dropdown'
import Tag from 'primevue/tag'
import Card from 'primevue/card'
import PanelMenu from 'primevue/panelmenu'
import Avatar from 'primevue/avatar'
import Badge from 'primevue/badge'
import Menubar from 'primevue/menubar'
import Select from 'primevue/select'
import Textarea from 'primevue/textarea'
import FileUpload from 'primevue/fileupload'
import Toast from 'primevue/toast'
import ConfirmDialog from 'primevue/confirmdialog'
import ProgressSpinner from 'primevue/progressspinner'

import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(PrimeVue, {
  theme: {
    preset: Aura,
    options: {
      darkModeSelector: false,
      cssLayer: {
        name: 'primevue',
        order: 'theme, base, primevue',
      },
    },
  },
  pt: {
    global: {
      fontFamily: "'Poppins', sans-serif",
    },
  },
  ripple: true,
})

// Global component registration
app.component('Button', Button)
app.component('InputText', InputText)
app.component('InputNumber', InputNumber)
app.component('Password', Password)
app.component('FloatLabel', FloatLabel)
app.component('Message', Message)
app.component('DataTable', DataTable)
app.component('Column', Column)
app.component('Dialog', Dialog)
app.component('Dropdown', Dropdown)
app.component('Tag', Tag)
app.component('Card', Card)
app.component('PanelMenu', PanelMenu)
app.component('Avatar', Avatar)
app.component('Badge', Badge)
app.component('Menubar', Menubar)
app.component('Select', Select)
app.component('Textarea', Textarea)
app.component('FileUpload', FileUpload)
app.component('Toast', Toast)
app.component('ConfirmDialog', ConfirmDialog)
app.component('ProgressSpinner', ProgressSpinner)

const auth = useAuthStore()
auth.initialize()

app.mount('#app')
