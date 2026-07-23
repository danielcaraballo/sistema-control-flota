<script setup>
import { computed } from 'vue'

const props = defineProps({
  total: { type: Number, default: 0 },
  porcentaje: { type: Number, default: 0 },
  operativos: { type: Number, default: 0 },
  inactivos: { type: Number, default: 0 },
})

const pctColor = computed(() => {
  if (props.porcentaje >= 80) return 'var(--p-green-500)'
  if (props.porcentaje >= 50) return 'var(--p-yellow-500)'
  return 'var(--p-red-500)'
})

const pctBg = computed(() => {
  if (props.porcentaje >= 80) return 'bg-green-100 dark:bg-green-900/30'
  if (props.porcentaje >= 50) return 'bg-yellow-100 dark:bg-yellow-900/30'
  return 'bg-red-100 dark:bg-red-900/30'
})
</script>

<template>
  <div class="border border-card-border rounded-md bg-card p-6 h-full flex flex-col">
    <div class="text-5xl font-bold leading-none text-[var(--p-text-color)]">
      {{ total.toLocaleString() }}
    </div>
    <div class="text-sm font-semibold text-muted-color uppercase tracking-wider mt-1 mb-5">
      Vehículos registrados
    </div>

    <div
      class="border-t border-[var(--p-surface-200)] dark:border-[var(--p-surface-600)] pt-4 flex-1 flex flex-col justify-between gap-4"
    >
      <div>
        <div class="flex items-baseline gap-2 mb-1.5">
          <span class="text-2xl font-bold leading-none" :style="{ color: pctColor }">
            {{ porcentaje }}%
          </span>
          <span class="text-xs text-muted-color">de operatividad</span>
        </div>
        <div class="h-2 rounded-full overflow-hidden" :class="pctBg">
          <div
            class="h-full rounded-full transition-all duration-500"
            :style="{ width: Math.min(porcentaje, 100) + '%', backgroundColor: pctColor }"
          />
        </div>
      </div>

      <div class="flex items-center gap-6">
        <div class="flex items-center gap-2">
          <div class="w-2.5 h-2.5 rounded-full bg-[var(--p-green-500)] shrink-0" />
          <span class="text-sm">
            <strong class="text-[var(--p-green-500)]">{{ operativos.toLocaleString() }}</strong>
            <span class="text-muted-color ml-1">operativos</span>
          </span>
        </div>
        <div class="flex items-center gap-2">
          <div class="w-2.5 h-2.5 rounded-full bg-[var(--p-red-500)] shrink-0" />
          <span class="text-sm">
            <strong class="text-[var(--p-red-500)]">{{ inactivos.toLocaleString() }}</strong>
            <span class="text-muted-color ml-1">inactivos</span>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>
