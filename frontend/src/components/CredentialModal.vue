<script setup>
import { ref } from 'vue'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import Message from 'primevue/message'

const props = defineProps({
  visible: { type: Boolean, required: true },
  header: { type: String, required: true },
  icon: { type: String, default: 'pi pi-check-circle' },
  iconColorClass: { type: String, default: 'text-green-600 dark:text-green-400' },
  successMessage: { type: String, required: true },
  fullName: { type: String, required: true },
  username: { type: String, required: true },
  password: { type: String, required: true },
  copyText: { type: String, required: true },
  warningText: {
    type: String,
    default: 'Copia las credenciales ahora. No se podrán mostrar de nuevo.',
  },
})

const emit = defineEmits(['update:visible'])

const copied = ref(false)

function close() {
  copied.value = false
  emit('update:visible', false)
}

async function copy() {
  try {
    await navigator.clipboard.writeText(props.copyText)
    copied.value = true
    setTimeout(() => {
      copied.value = false
    }, 2000)
  } catch {}
}
</script>

<template>
  <Dialog
    :visible="visible"
    :header="header"
    :modal="true"
    :closable="false"
    :draggable="false"
    :style="{ width: '450px' }"
    @update:visible="close"
  >
    <div class="space-y-4">
      <div :class="['flex items-center gap-2', iconColorClass]">
        <i :class="[icon, 'text-xl']" />
        <span class="font-semibold">{{ successMessage }}</span>
      </div>

      <div class="bg-card-hover rounded-md p-4 space-y-2">
        <p class="text-sm font-medium">{{ fullName }}</p>
        <div class="text-sm text-muted-color space-y-1">
          <p>
            <span class="font-medium text-surface-700 dark:text-surface-200">Usuario:</span>
            {{ username }}
          </p>
          <p>
            <span class="font-medium text-surface-700 dark:text-surface-200">Contraseña:</span>
            {{ password }}
          </p>
        </div>
      </div>

      <Button
        :label="copied ? 'Copiado' : 'Copiar credenciales'"
        :icon="copied ? 'pi pi-check' : 'pi pi-copy'"
        class="w-full"
        @click="copy"
      />

      <Message severity="warn" :closable="false" class="!text-xs">
        <i class="pi pi-exclamation-triangle mr-1" />
        {{ warningText }}
      </Message>
    </div>

    <template #footer>
      <Button label="Cerrar" @click="close" />
    </template>
  </Dialog>
</template>
