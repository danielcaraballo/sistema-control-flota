<script setup>
defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
  icon: { type: String, default: '' },
})
</script>

<template>
  <div
    class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 sm:gap-4 mb-4 sm:mb-6"
  >
    <div class="flex-1 min-w-0">
      <h1
        class="text-xl sm:text-2xl font-semibold text-[var(--p-text-color)] flex items-center gap-2"
      >
        <i
          v-if="icon"
          :class="icon"
          class="text-lg sm:text-xl text-[var(--p-primary-color)] shrink-0"
        />
        <span class="truncate">{{ title }}</span>
      </h1>
      <p v-if="subtitle" class="mt-0.5 sm:mt-1 text-xs sm:text-sm text-muted-color">
        {{ subtitle }}
      </p>
    </div>
    <div v-if="$slots.default" class="flex items-center gap-2 flex-wrap sm:shrink-0">
      <slot />
    </div>
  </div>
</template>
