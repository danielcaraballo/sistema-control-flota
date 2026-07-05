<script setup>
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'

defineProps({
  visible: { type: Boolean, required: true },
  header: { type: String, required: true },
  message: { type: String, required: true },
  confirmLabel: { type: String, required: true },
  confirmSeverity: { type: String, default: 'danger' },
  loading: { type: Boolean, default: false },
})

const emit = defineEmits(['update:visible', 'confirm'])

function close() {
  if (props.loading) return
  emit('update:visible', false)
}

function handleConfirm() {
  emit('confirm')
}
</script>

<template>
  <Dialog
    :visible="visible"
    :header="header"
    :modal="true"
    :closable="!loading"
    :draggable="false"
    :style="{ width: 'min(400px, calc(100vw - 2rem))' }"
    @update:visible="close"
  >
    <p class="text-sm text-muted-color" v-text="message" />
    <template #footer>
      <Button label="Cancelar" severity="secondary" :disabled="loading" @click="close" />
      <Button
        :label="confirmLabel"
        :severity="confirmSeverity"
        :loading="loading"
        @click="handleConfirm"
      />
    </template>
  </Dialog>
</template>
