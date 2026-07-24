<script setup>
import { computed } from 'vue'

const props = defineProps({
  estado: { type: Object, required: true },
})

const barColor = computed(() => {
  const pct = props.estado.operatividad
  if (pct >= 80) return 'bg-green-500'
  if (pct >= 50) return 'bg-yellow-500'
  return 'bg-red-500'
})

const barBg = computed(() => {
  const pct = props.estado.operatividad
  if (pct >= 80) return 'bg-green-100 dark:bg-green-900/30'
  if (pct >= 50) return 'bg-yellow-100 dark:bg-yellow-900/30'
  return 'bg-red-100 dark:bg-red-900/30'
})
</script>

<template>
  <div class="flex items-center gap-4 p-3 rounded-md border border-card-border bg-card-hover/30">
    <div class="flex-1 min-w-0">
      <div class="flex items-center justify-between mb-1">
        <span class="text-sm font-semibold text-color truncate">{{ estado.estado_nombre }}</span>
        <span class="text-sm font-bold" :class="barColor.replace('bg-', 'text-')">
          {{ estado.operatividad }}%
        </span>
      </div>
      <div class="h-2 rounded-full overflow-hidden" :class="barBg">
        <div
          class="h-full rounded-full transition-all duration-300"
          :class="barColor"
          :style="{ width: Math.min(estado.operatividad, 100) + '%' }"
        />
      </div>
      <div class="flex items-center gap-3 mt-1 text-xs text-muted-color">
        <span>{{ estado.total }} vehículos</span>
        <span class="text-green-600"> {{ estado.activos }} operativos </span>
        <span class="text-red-600"> {{ estado.inactivos }} inactivos </span>
      </div>
    </div>
  </div>
</template>
