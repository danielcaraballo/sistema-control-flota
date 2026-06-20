<script setup>
import { ref, onMounted } from 'vue'
import PageHeader from '@/components/PageHeader.vue'
import KpiCard from '@/components/KpiCard.vue'
import Chart from 'primevue/chart'

const kpiData = {
  operativos: { value: 42, trend: 'up', trendLabel: '8%' },
  taller: { value: 5, trend: 'down', trendLabel: '2' },
  alertas: { value: 3, trend: 'up', trendLabel: '1' },
  mttr: { value: 2.4, trend: 'down', trendLabel: '0.3h' },
  conductores: { value: 38, trend: 'up', trendLabel: '2' },
  kilometraje: { value: '45,230', trend: 'up', trendLabel: '12%' },
}

const estadoData = ref(null)
const tipoData = ref(null)
const manttoData = ref(null)

onMounted(() => {
  estadoData.value = {
    labels: ['Operativos', 'En Taller', 'Dados de Baja', 'Disponibles'],
    datasets: [
      {
        data: [42, 5, 3, 8],
        backgroundColor: ['#22c55e', '#f59e0b', '#ef4444', '#3b82f6'],
        borderWidth: 0,
      },
    ],
  }

  tipoData.value = {
    labels: ['Sedan', 'SUV', 'Pickup', 'Camión'],
    datasets: [
      {
        data: [18, 12, 15, 5],
        backgroundColor: ['#6366f1', '#8b5cf6', '#a855f7', '#c084fc'],
        borderWidth: 0,
      },
    ],
  }

  manttoData.value = {
    labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
    datasets: [
      {
        label: 'Mantenimientos',
        data: [8, 12, 7, 15, 10, 9],
        fill: false,
        borderColor: 'var(--p-primary-color)',
        backgroundColor: 'var(--p-primary-color)',
        tension: 0.4,
      },
      {
        label: 'Alertas',
        data: [3, 5, 2, 7, 4, 3],
        fill: false,
        borderColor: '#ef4444',
        backgroundColor: '#ef4444',
        tension: 0.4,
      },
    ],
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: { boxWidth: 10, padding: 6, font: { size: 10 } },
    },
  },
}

const donutOptions = {
  ...chartOptions,
  cutout: '65%',
}

const lineOptions = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: { mode: 'index', intersect: false },
  scales: {
    y: { beginAtZero: true, ticks: { font: { size: 10 } } },
    x: { ticks: { font: { size: 10 } } },
  },
  plugins: {
    legend: {
      position: 'bottom',
      labels: { boxWidth: 10, padding: 6, font: { size: 10 } },
    },
  },
}
</script>

<template>
  <div class="h-full flex flex-col gap-2">
    <PageHeader
      title="Dashboard"
      subtitle="Resumen general de la flota"
      icon="pi pi-home"
      class="!mb-0"
    />

    <div class="grid grid-cols-3 xl:grid-cols-6 gap-2 shrink-0">
      <KpiCard
        title="Vehículos Operativos"
        :value="kpiData.operativos.value"
        icon="pi pi-check-circle"
        color="success"
        :trend="kpiData.operativos.trend"
        :trend-label="kpiData.operativos.trendLabel"
      />
      <KpiCard
        title="En Taller"
        :value="kpiData.taller.value"
        icon="pi pi-wrench"
        color="warn"
        :trend="kpiData.taller.trend"
        :trend-label="kpiData.taller.trendLabel"
      />
      <KpiCard
        title="Alertas Preventivas"
        :value="kpiData.alertas.value"
        icon="pi pi-exclamation-triangle"
        color="danger"
        :trend="kpiData.alertas.trend"
        :trend-label="kpiData.alertas.trendLabel"
      />
      <KpiCard
        title="MTTR (horas)"
        :value="kpiData.mttr.value"
        icon="pi pi-clock"
        color="info-color"
        :trend="kpiData.mttr.trend"
        :trend-label="kpiData.mttr.trendLabel"
      />
      <KpiCard
        title="Conductores"
        :value="kpiData.conductores.value"
        icon="pi pi-users"
        color="primary"
        :trend="kpiData.conductores.trend"
        :trend-label="kpiData.conductores.trendLabel"
      />
      <KpiCard
        title="KM Recorridos (mes)"
        :value="kpiData.kilometraje.value"
        icon="pi pi-map-marker"
        color="info-color"
        :trend="kpiData.kilometraje.trend"
        :trend-label="kpiData.kilometraje.trendLabel"
      />
    </div>

    <div class="flex-1 grid grid-cols-1 lg:grid-cols-3 gap-2 min-h-0">
      <div class="border border-surface-200 rounded-md bg-surface-0 p-3 flex flex-col min-h-0">
        <h3 class="text-xs font-semibold text-muted-color uppercase tracking-wider mb-2 shrink-0">
          <i class="pi pi-chart-pie text-xs mr-1.5" />Distribución por Estado
        </h3>
        <div class="flex-1 min-h-0">
          <Chart v-if="estadoData" type="doughnut" :data="estadoData" :options="donutOptions" />
        </div>
      </div>
      <div class="border border-surface-200 rounded-md bg-surface-0 p-3 flex flex-col min-h-0">
        <h3 class="text-xs font-semibold text-muted-color uppercase tracking-wider mb-2 shrink-0">
          <i class="pi pi-car text-xs mr-1.5" />Distribución por Tipo
        </h3>
        <div class="flex-1 min-h-0">
          <Chart v-if="tipoData" type="pie" :data="tipoData" :options="chartOptions" />
        </div>
      </div>
      <div class="border border-surface-200 rounded-md bg-surface-0 p-3 flex flex-col min-h-0">
        <h3 class="text-xs font-semibold text-muted-color uppercase tracking-wider mb-2 shrink-0">
          <i class="pi pi-chart-line text-xs mr-1.5" />Mantenimientos y Alertas
        </h3>
        <div class="flex-1 min-h-0">
          <Chart v-if="manttoData" type="line" :data="manttoData" :options="lineOptions" />
        </div>
      </div>
    </div>

    <div class="border border-surface-200 rounded-md bg-surface-0 overflow-hidden shrink-0">
      <div class="flex items-center gap-2 px-3 py-1.5 border-b border-surface-200 bg-surface-50">
        <i class="pi pi-bell text-xs text-muted-color" />
        <span class="text-xs font-semibold text-muted-color uppercase tracking-wider"
          >Alertas Recientes</span
        >
      </div>
      <div class="flex divide-x divide-surface-200 text-xs">
        <div class="flex-1 flex items-center gap-2 px-3 py-2 min-w-0">
          <span class="w-1.5 h-1.5 rounded-full bg-yellow-500 shrink-0" />
          <span class="truncate text-surface-700 dark:text-surface-200"
            >TQ-456-A Cambio de aceite próximo</span
          >
          <span class="ml-auto shrink-0 text-muted-color">2h</span>
        </div>
        <div class="flex-1 flex items-center gap-2 px-3 py-2 min-w-0">
          <span class="w-1.5 h-1.5 rounded-full bg-orange-500 shrink-0" />
          <span class="truncate text-surface-700 dark:text-surface-200"
            >TQ-123-B Frenos requieren revisión</span
          >
          <span class="ml-auto shrink-0 text-muted-color">5h</span>
        </div>
        <div class="flex-1 flex items-center gap-2 px-3 py-2 min-w-0">
          <span class="w-1.5 h-1.5 rounded-full bg-red-500 shrink-0" />
          <span class="truncate text-surface-700 dark:text-surface-200"
            >TQ-789-C Motor sobrecalentado</span
          >
          <span class="ml-auto shrink-0 text-muted-color">1d</span>
        </div>
        <div class="flex-1 flex items-center gap-2 px-3 py-2 min-w-0">
          <span class="w-1.5 h-1.5 rounded-full bg-green-500 shrink-0" />
          <span class="truncate text-surface-700 dark:text-surface-200"
            >TQ-321-D Mantenimiento completado</span
          >
          <span class="ml-auto shrink-0 text-muted-color">2d</span>
        </div>
      </div>
    </div>
  </div>
</template>
