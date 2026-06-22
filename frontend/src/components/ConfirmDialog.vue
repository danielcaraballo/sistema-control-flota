<script setup>
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'

defineProps({
  visible: { type: Boolean, required: true },
  header: { type: String, required: true },
  message: { type: String, required: true },
  confirmLabel: { type: String, required: true },
  confirmSeverity: { type: String, default: 'danger' },
  onConfirm: { type: Function, required: true },
})

const emit = defineEmits(['update:visible'])

function close() {
  emit('update:visible', false)
}
</script>

<template>
  <Dialog
    :visible="visible"
    :header="header"
    :modal="true"
    :closable="true"
    :draggable="false"
    :style="{ width: '400px' }"
    @update:visible="close"
  >
    <p class="text-sm text-muted-color" v-text="message" />
    <template #footer>
      <Button label="Cancelar" severity="secondary" @click="close" />
      <Button :label="confirmLabel" :severity="confirmSeverity" @click="onConfirm" />
    </template>
  </Dialog>
</template>
