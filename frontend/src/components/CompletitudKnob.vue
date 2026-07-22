<script setup>
import Knob from 'primevue/knob'
import { computed } from 'vue'

const props = defineProps({
  value: { type: Number, required: true },
  size: { type: Number, default: 80 },
  strokeWidth: { type: Number, default: 10 },
})

const clamped = computed(() => Math.min(100, Math.max(0, props.value ?? 0)))

const color = computed(() => {
  if (clamped.value >= 80) return '#22c55e'
  if (clamped.value >= 50) return '#eab308'
  return '#ef4444'
})

const labelFontSize = computed(() => Math.max(11, Math.round(props.size * 0.28)) + 'px')

const ariaLabel = computed(() => `${clamped.value}% completo`)
</script>

<template>
  <Knob
    :modelValue="clamped"
    :valueColor="color"
    :rangeColor="'#d1d5db'"
    :size="size"
    :strokeWidth="strokeWidth"
    class="font-bold"
    :pt="{ label: { style: { fontSize: labelFontSize } } }"
    valueTemplate="{value}%"
    :aria-label="ariaLabel"
    readonly
    v-bind="$attrs"
  />
</template>
