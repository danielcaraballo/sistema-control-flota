<script setup>
const CARD_COLORS = [
  'var(--p-blue-500)',
  'var(--p-green-500)',
  'var(--p-yellow-500)',
  'var(--p-red-500)',
  'var(--p-purple-500)',
  'var(--p-cyan-500)',
]

const props = defineProps({
  estatus: { type: Array, required: true },
  total: { type: Number, default: 0 },
})

function barWidth(cantidad) {
  if (!props.total) return 0
  return Math.round((cantidad / props.total) * 100)
}
</script>

<template>
  <div class="border border-card-border rounded-md bg-card p-5 h-full flex flex-col">
    <h2 class="text-sm font-semibold text-muted-color uppercase tracking-wider mb-4">
      Distribución por estatus
    </h2>

    <div class="flex-1 flex flex-col gap-3 min-h-0">
      <div v-for="(e, i) in estatus" :key="e.id" class="flex items-center gap-3">
        <div
          class="w-2.5 h-2.5 rounded-full shrink-0"
          :style="{ backgroundColor: CARD_COLORS[i % CARD_COLORS.length] }"
        />
        <span class="text-sm text-color flex-1 min-w-0 truncate capitalize">{{ e.nombre }}</span>
        <div class="flex items-center gap-2 flex-1 max-w-[200px]">
          <div
            class="flex-1 h-1.5 rounded-full overflow-hidden bg-[var(--p-surface-200)] dark:bg-[var(--p-surface-600)]"
          >
            <div
              class="h-full rounded-full transition-all duration-300"
              :style="{
                width: barWidth(e.cantidad) + '%',
                backgroundColor: CARD_COLORS[i % CARD_COLORS.length],
              }"
            />
          </div>
        </div>
        <span class="text-sm font-semibold text-color shrink-0 w-10 text-right">{{
          e.cantidad.toLocaleString()
        }}</span>
      </div>
    </div>
  </div>
</template>
