<script setup>
import { ref, onMounted } from 'vue'
import TabView from 'primevue/tabview'
import TabPanel from 'primevue/tabpanel'
import { useToast } from 'primevue/usetoast'
import PageHeader from '@/components/PageHeader.vue'
import CatalogoTabContent from '@/components/CatalogoTabContent.vue'
import api from '@/services/api'

const toast = useToast()
const estados = ref([])

async function loadEstados() {
  try {
    const { data } = await api.get('/organizacion/estados/?incluir_inactivos=true')
    estados.value = data
  } catch {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'No se pudieron cargar los estados',
      life: 5000,
    })
  }
}

const CATALOGOS = [
  {
    key: 'estados',
    label: 'Estados',
    endpoint: '/organizacion/estados/',
    icon: 'pi pi-map',
    field: 'nombre',
    filterField: 'nombre',
  },
  {
    key: 'gerencias',
    label: 'Gerencias',
    endpoint: '/organizacion/gerencias/',
    icon: 'pi pi-sitemap',
    field: 'nombre',
    filterField: 'nombre',
  },
  {
    key: 'centrosServicio',
    label: 'Centros de Servicio',
    endpoint: '/organizacion/centros-servicio/',
    icon: 'pi pi-building',
    field: 'nombre',
    filterField: 'nombre',
  },
]

const activeIndex = ref(0)

onMounted(loadEstados)
</script>

<template>
  <div class="w-full">
    <PageHeader
      title="Organización"
      subtitle="Gestión de estados, gerencias y centros de servicio"
      icon="pi pi-sitemap"
    />

    <div class="border border-card-border rounded-md bg-card">
      <TabView v-model:activeIndex="activeIndex" scrollable>
        <TabPanel v-for="cat in CATALOGOS" :key="cat.key">
          <template #header>
            <i :class="cat.icon + ' mr-2'" />
            {{ cat.label }}
          </template>
          <CatalogoTabContent :config="cat" :fk-catalogs="{ estados }" />
        </TabPanel>
      </TabView>
    </div>
  </div>
</template>
