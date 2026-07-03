<script setup>
import { ref } from 'vue'
import TabView from 'primevue/tabview'
import TabPanel from 'primevue/tabpanel'
import PageHeader from '@/components/PageHeader.vue'
import CatalogoTabContent from '@/components/CatalogoTabContent.vue'

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
          <CatalogoTabContent :config="cat" />
        </TabPanel>
      </TabView>
    </div>
  </div>
</template>
