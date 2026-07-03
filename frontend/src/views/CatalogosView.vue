<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'
import TabView from 'primevue/tabview'
import TabPanel from 'primevue/tabpanel'
import PageHeader from '@/components/PageHeader.vue'
import CatalogoTabContent from '@/components/CatalogoTabContent.vue'

const CATALOGOS = [
  {
    key: 'marcas',
    label: 'Marcas',
    endpoint: '/catalogos/marcas/',
    icon: 'pi pi-tag',
    field: 'nombre',
    filterField: 'nombre',
  },
  {
    key: 'modelos',
    label: 'Modelos',
    endpoint: '/catalogos/modelos/',
    icon: 'pi pi-cog',
    field: 'nombre',
    filterField: 'nombre',
  },
  {
    key: 'tiposVehiculo',
    label: 'Tipos de Vehículo',
    endpoint: '/catalogos/tipos-vehiculo/',
    icon: 'pi pi-car',
    field: 'nombre',
    filterField: 'nombre',
  },
  {
    key: 'tiposUso',
    label: 'Tipos de Uso',
    endpoint: '/catalogos/tipos-uso/',
    icon: 'pi pi-clock',
    field: 'nombre',
    filterField: 'nombre',
  },
  {
    key: 'colores',
    label: 'Colores',
    endpoint: '/catalogos/colores/',
    icon: 'pi pi-palette',
    field: 'nombre',
    filterField: 'nombre',
  },
  {
    key: 'sistemasAfectados',
    label: 'Sistemas Afectados',
    endpoint: '/catalogos/sistemas-afectados/',
    icon: 'pi pi-wrench',
    field: 'nombre',
    filterField: 'nombre',
  },
  {
    key: 'tiposFalla',
    label: 'Tipos de Falla',
    endpoint: '/catalogos/tipos-falla/',
    icon: 'pi pi-exclamation-triangle',
    field: 'descripcion',
    filterField: 'descripcion',
  },
]

const activeIndex = ref(0)
const catalogoMarcas = ref([])
const catalogoSistemas = ref([])

async function loadMarcas() {
  try {
    const { data } = await api.get('/catalogos/marcas/?incluir_inactivos=true')
    catalogoMarcas.value = data
  } catch {}
}

async function loadSistemasAfectados() {
  try {
    const { data } = await api.get('/catalogos/sistemas-afectados/?incluir_inactivos=true')
    catalogoSistemas.value = data
  } catch {}
}

onMounted(() => {
  loadMarcas()
  loadSistemasAfectados()
})
</script>

<template>
  <div class="w-full">
    <PageHeader
      title="Catálogos"
      subtitle="Gestión de tablas maestras del sistema"
      icon="pi pi-book"
    />

    <div class="border border-card-border rounded-md bg-card">
      <TabView v-model:activeIndex="activeIndex" scrollable>
        <TabPanel v-for="cat in CATALOGOS" :key="cat.key">
          <template #header>
            <i :class="cat.icon + ' mr-2'" />
            {{ cat.label }}
          </template>
          <CatalogoTabContent
            :config="cat"
            :fk-catalogs="{ marcas: catalogoMarcas, sistemas: catalogoSistemas }"
          />
        </TabPanel>
      </TabView>
    </div>
  </div>
</template>
