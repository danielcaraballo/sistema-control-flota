<script setup>
import { ref, computed, onMounted } from 'vue'
import TabView from 'primevue/tabview'
import TabPanel from 'primevue/tabpanel'
import Select from 'primevue/select'
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
  } catch (err) {
    console.error('Error al cargar estados:', err)
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

const activeCatalogKey = computed({
  get: () => CATALOGOS[activeIndex.value]?.key,
  set: (key) => {
    const idx = CATALOGOS.findIndex((c) => c.key === key)
    if (idx !== -1) activeIndex.value = idx
  },
})

function handleItemSaved(key) {
  if (key === 'estados') loadEstados()
}

onMounted(loadEstados)
</script>

<template>
  <div class="w-full">
    <PageHeader
      title="Organización"
      subtitle="Gestión de estados, gerencias y centros de servicio"
      icon="pi pi-sitemap"
    />

    <!-- Selector directo para pantallas móviles (< sm) -->
    <div class="sm:hidden mb-4">
      <label class="block text-xs font-semibold text-muted-color uppercase tracking-wider mb-1.5">
        Sección seleccionada
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
            :fk-catalogs="{ estados }"
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
          :fk-catalogs="{ estados }"
          @item-saved="handleItemSaved"
        />
      </div>
    </div>
  </div>
</template>
