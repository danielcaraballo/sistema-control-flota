<script setup>
defineProps({
  title: { type: String, required: true },
  value: { type: [String, Number], default: '—' },
  icon: { type: String, default: '' },
  color: { type: String, default: 'primary' },
  trend: { type: String, default: '' },
  trendLabel: { type: String, default: '' },
})
</script>

<template>
  <div
    class="border border-card-border rounded-md bg-card transition-all duration-150 hover:shadow-xs"
  >
    <div class="p-3 flex items-center justify-between gap-3">
      <div class="flex flex-col gap-1 min-w-0">
        <span class="text-xs font-semibold text-muted-color uppercase tracking-wider">{{
          title
        }}</span>
        <div class="flex items-baseline gap-1.5">
          <span class="text-xl font-bold leading-none text-[var(--p-text-color)]">{{ value }}</span>
          <div
            v-if="trend"
            class="inline-flex items-center gap-0.5 text-xs font-semibold whitespace-nowrap"
            :class="trend === 'up' ? 'text-green-600' : 'text-red-600'"
          >
            <i :class="trend === 'up' ? 'pi pi-arrow-up' : 'pi pi-arrow-down'" class="text-xs" />
            <span>{{ trendLabel }}</span>
          </div>
        </div>
      </div>
      <div
        v-if="icon"
        class="w-9 h-9 rounded-full flex items-center justify-center shrink-0"
        :class="{
          'bg-primary-100 dark:bg-primary-900/25 text-primary-color': color === 'primary',
          'bg-green-100 dark:bg-green-900/25 text-green-600 dark:text-green-400':
            color === 'success',
          'bg-orange-100 dark:bg-orange-900/25 text-orange-600 dark:text-orange-400':
            color === 'warn',
          'bg-red-100 dark:bg-red-900/25 text-red-600 dark:text-red-400': color === 'danger',
          'bg-cyan-100 dark:bg-cyan-900/25 text-cyan-600 dark:text-cyan-400':
            color === 'info-color',
        }"
      >
        <i :class="icon" class="text-base" />
      </div>
    </div>
  </div>
</template>
