<script setup>
import { ref, computed, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import api from '@/services/api'
import Skeleton from 'primevue/skeleton'
import PageHeader from '@/components/PageHeader.vue'
import KpiCard from '@/components/KpiCard.vue'
import KpiTotalCard from '@/components/dashboard/KpiTotalCard.vue'
import StatusCard from '@/components/dashboard/StatusCard.vue'
import EstadoComparisonCard from '@/components/dashboard/EstadoComparisonCard.vue'
import { useAuthStore } from '@/stores/auth'
import { ROL_NACIONAL } from '@/utils/roles'

const toast = useToast()
const auth = useAuthStore()
const loading = ref(true)
const kpis = ref(null)
const nacionalData = ref(null)

const esNacional = computed(() => auth.tieneRol(ROL_NACIONAL))

async function loadDashboard() {
  loading.value = true
  try {
    const calls = [api.get('/dashboard/kpis')]
    if (esNacional.value) {
      calls.push(api.get('/dashboard/nacional'))
    }
    const [kpiRes, nacionalRes] = await Promise.all(calls)
    kpis.value = kpiRes.data
    nacionalData.value = nacionalRes?.data ?? null
  } catch {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'No se pudo cargar el dashboard',
      life: 5000,
    })
  } finally {
    loading.value = false
  }
}

onMounted(loadDashboard)
</script>

<template>
  <div class="max-w-[1200px]">
    <PageHeader title="Dashboard" subtitle="Resumen general de la flota" icon="pi pi-home" />

    <template v-if="loading">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-6">
        <Skeleton class="h-[220px]" />
        <Skeleton class="h-[220px]" />
      </div>
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6">
        <Skeleton v-for="i in 3" :key="'r2-' + i" class="h-[100px]" />
      </div>
      <div class="mb-6">
        <Skeleton class="h-[200px]" />
      </div>
    </template>

    <template v-else-if="kpis?.total_vehiculos > 0">
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
          color="info-color"
        />
        <template v-if="esNacional && nacionalData">
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
        <div v-else class="lg:col-span-2" />
      </div>

      <template v-if="esNacional && nacionalData?.resumen_estados?.length">
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
