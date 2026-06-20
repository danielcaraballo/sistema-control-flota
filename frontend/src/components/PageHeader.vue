<script setup>
defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
  icon: { type: String, default: '' },
})
</script>

<template>
  <div class="flex justify-between items-start gap-4 mb-6">
    <div class="flex-1 min-w-0">
      <h1
        class="m-0 text-[1.375rem] font-semibold text-[var(--p-text-color)] flex items-center gap-2"
      >
        <i v-if="icon" :class="icon" class="text-lg text-[var(--p-primary-color)]" />
        {{ title }}
      </h1>
      <p v-if="subtitle" class="mt-1 text-sm text-muted-color m-0">{{ subtitle }}</p>
    </div>
    <div class="flex items-center gap-2 shrink-0">
      <slot />
    </div>
  </div>
</template>
