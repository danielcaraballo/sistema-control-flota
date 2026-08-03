<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'
import TabView from 'primevue/tabview'
import TabPanel from 'primevue/tabpanel'
import Select from 'primevue/select'
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

const activeCatalogKey = computed({
  get: () => CATALOGOS[activeIndex.value]?.key,
  set: (key) => {
    const idx = CATALOGOS.findIndex((c) => c.key === key)
    if (idx !== -1) activeIndex.value = idx
  },
})

async function loadMarcas() {
  try {
    const { data } = await api.get('/catalogos/marcas/?incluir_inactivos=true')
    catalogoMarcas.value = data
  } catch (err) {
    console.error('Error al cargar marcas:', err)
  }
}

async function loadSistemasAfectados() {
  try {
    const { data } = await api.get('/catalogos/sistemas-afectados/?incluir_inactivos=true')
    catalogoSistemas.value = data
  } catch (err) {
    console.error('Error al cargar sistemas afectados:', err)
  }
}
function handleItemSaved(key) {
  if (key === 'marcas') loadMarcas()
  if (key === 'sistemasAfectados') loadSistemasAfectados()
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

    <!-- Selector directo para pantallas móviles (< sm) -->
    <div class="sm:hidden mb-4">
      <label class="block text-xs font-semibold text-muted-color uppercase tracking-wider mb-1.5">
        Catálogo seleccionado
      </label>
      <Select
        v-model="activeCatalogKey"
        :options="CATALOGOS"
        optionLabel="label"
        optionValue="key"
        class="w-full"
      >
        <template #value="{ value, placeholder }">
          <div v-if="value" class="flex items-center gap-2">
            <i
              :class="CATALOGOS.find((c) => c.key === value)?.icon"
              class="text-[var(--p-primary-color)]"
            />
            <span class="font-medium">{{ CATALOGOS.find((c) => c.key === value)?.label }}</span>
          </div>
          <span v-else>{{ placeholder }}</span>
        </template>
        <template #option="{ option }">
          <div class="flex items-center gap-2 py-0.5">
            <i :class="option.icon" class="text-[var(--p-primary-color)]" />
            <span>{{ option.label }}</span>
          </div>
        </template>
      </Select>
    </div>

    <div class="border border-card-border rounded-md bg-card">
      <!-- Pestañas visibles en escritorio/tablet (sm:block) -->
      <TabView v-model:activeIndex="activeIndex" scrollable class="hidden sm:block">
        <TabPanel v-for="cat in CATALOGOS" :key="cat.key">
          <template #header>
            <div class="flex items-center gap-2">
              <i :class="cat.icon" class="text-base" />
              <span>{{ cat.label }}</span>
            </div>
          </template>
          <CatalogoTabContent
            :config="cat"
            :fk-catalogs="{ marcas: catalogoMarcas, sistemas: catalogoSistemas }"
            @item-saved="handleItemSaved"
          />
        </TabPanel>
      </TabView>

      <!-- Renderizado directo en móvil (< sm) sin pestañas -->
      <div class="sm:hidden p-2">
        <CatalogoTabContent
          v-if="CATALOGOS[activeIndex]"
          :key="CATALOGOS[activeIndex].key"
          :config="CATALOGOS[activeIndex]"
          :fk-catalogs="{ marcas: catalogoMarcas, sistemas: catalogoSistemas }"
          @item-saved="handleItemSaved"
        />
      </div>
    </div>
  </div>
</template>
