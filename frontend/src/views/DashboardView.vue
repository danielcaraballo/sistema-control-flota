<script setup>
import { ref, computed, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import Button from 'primevue/button'
import api from '@/services/api'
import PageHeader from '@/components/PageHeader.vue'
import KpiCard from '@/components/KpiCard.vue'
import KpiTotalCard from '@/components/dashboard/KpiTotalCard.vue'
import StatusCard from '@/components/dashboard/StatusCard.vue'
import EstadoComparisonCard from '@/components/dashboard/EstadoComparisonCard.vue'
import { useAuthStore } from '@/stores/auth'
import { ROL_NACIONAL } from '@/utils/roles'

const toast = useToast()
const auth = useAuthStore()
const kpis = ref(null)
const nacionalData = ref(null)
const error = ref(false)

const esNacional = computed(() => auth.tieneRol(ROL_NACIONAL))

const kpisValidos = computed(() => kpis.value && kpis.value.total_vehiculos !== undefined)

const nacionalDataValidos = computed(() => Array.isArray(nacionalData.value?.resumen_estados))

async function loadDashboard() {
  error.value = false
  try {
    const calls = [api.get('/dashboard/kpis')]
    if (esNacional.value) {
      calls.push(api.get('/dashboard/nacional'))
    }
    const results = await Promise.allSettled(calls)
    const kpiResult = results[0]
    if (kpiResult.status === 'fulfilled') {
      kpis.value = kpiResult.value.data
    } else {
      throw kpiResult.reason
    }
    const nacionalResult = results[1]
    if (nacionalResult && nacionalResult.status === 'fulfilled') {
      nacionalData.value = nacionalResult.value.data
    }
  } catch (err) {
    error.value = true
    console.error('Error al cargar dashboard:', err)
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'No se pudo cargar el dashboard',
      life: 5000,
    })
  }
}

function retryDashboard() {
  kpis.value = null
  nacionalData.value = null
  loadDashboard()
}

onMounted(loadDashboard)
</script>

<template>
  <div class="max-w-[1200px]">
    <PageHeader title="Dashboard" subtitle="Resumen general de la flota" icon="pi pi-home" />

    <template v-if="error">
      <div class="border border-card-border rounded-md bg-card p-8 text-center">
        <p class="text-muted-color mb-4">Error al cargar el dashboard</p>
        <Button label="Reintentar" severity="secondary" size="small" @click="retryDashboard" />
      </div>
    </template>

    <template v-else-if="kpis === null">
      <div class="border border-card-border rounded-md bg-card p-8 text-center text-muted-color">
        Cargando...
      </div>
    </template>

    <template v-else-if="kpisValidos && kpis.total_vehiculos > 0">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-6">
        <KpiTotalCard
          :total="kpis.total_vehiculos"
          :porcentaje="kpis.porcentaje_operatividad"
          :operativos="kpis.operativos"
          :inactivos="kpis.inactivos"
        />
        <StatusCard :estatus="kpis.estatus" :total="kpis.total_vehiculos" />
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6">
        <KpiCard
          title="Completitud promedio"
          :value="`${kpis.completitud_promedio}%`"
          icon="pi pi-check-circle"
          color="info"
        />
        <template v-if="esNacional && nacionalDataValidos">
          <KpiCard
            v-if="nacionalData.mejor_operatividad"
            title="Mejor operatividad"
            :value="nacionalData.mejor_operatividad.estado_nombre"
            :trend="'up'"
            :trend-label="`${nacionalData.mejor_operatividad.operatividad}%`"
            icon="pi pi-arrow-up"
            color="success"
          />
          <KpiCard
            v-if="nacionalData.peor_operatividad"
            title="Peor operatividad"
            :value="nacionalData.peor_operatividad.estado_nombre"
            :trend="'down'"
            :trend-label="`${nacionalData.peor_operatividad.operatividad}%`"
            icon="pi pi-arrow-down"
            color="danger"
          />
        </template>
      </div>

      <template v-if="esNacional && nacionalDataValidos && nacionalData.resumen_estados.length">
        <div class="border border-card-border rounded-md bg-card p-5 mb-6">
          <h2 class="text-sm font-semibold text-muted-color uppercase tracking-wider mb-4">
            Comparativa por estado
          </h2>
          <div class="flex flex-col gap-3">
            <EstadoComparisonCard
              v-for="est in nacionalData.resumen_estados"
              :key="est.estado_nombre"
              :estado="est"
            />
          </div>
        </div>
      </template>
    </template>

    <div
      v-else
      class="border border-card-border rounded-md bg-card p-8 text-center text-muted-color"
    >
      No hay vehículos registrados
    </div>
  </div>
</template>
