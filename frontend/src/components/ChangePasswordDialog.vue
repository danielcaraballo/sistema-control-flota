<script setup>
import { ref, computed } from 'vue'
import { useToast } from 'primevue/usetoast'
import api from '@/services/api'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import Message from 'primevue/message'

const emit = defineEmits(['close'])

const toast = useToast()

const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const submitting = ref(false)
const error = ref('')

const passwordsMatch = computed(() => newPassword.value === confirmPassword.value)
const passwordLengthOk = computed(() => newPassword.value.length >= 8)
const formValid = computed(
  () =>
    currentPassword.value &&
    newPassword.value &&
    confirmPassword.value &&
    passwordsMatch.value &&
    passwordLengthOk.value,
)

function resetForm() {
  currentPassword.value = ''
  newPassword.value = ''
  confirmPassword.value = ''
  error.value = ''
}

async function handleSubmit() {
  if (!formValid.value || submitting.value) return

  submitting.value = true
  error.value = ''

  try {
    await api.post('/auth/change-password', {
      current_password: currentPassword.value,
      new_password: newPassword.value,
    })
    toast.add({
      severity: 'success',
      summary: 'Contraseña cambiada',
      detail: 'Tu contraseña se actualizó correctamente.',
      life: 3000,
    })
    resetForm()
    emit('close')
  } catch (err) {
    error.value =
      err.response?.data?.detail || err.response?.data?.message || 'Error al cambiar la contraseña'
  } finally {
    submitting.value = false
  }
}

function handleClose() {
  resetForm()
  emit('close')
}
</script>

<template>
  <Dialog
    :visible="true"
    header="Cambiar contraseña"
    :modal="true"
    :closable="true"
    :draggable="false"
    :style="{ width: '420px' }"
    @update:visible="handleClose"
  >
    <div class="space-y-4">
      <Message v-if="error" severity="error" :closable="false" class="!text-sm">
        {{ error }}
      </Message>

      <div class="space-y-2">
        <label for="currentPassword" class="text-sm font-medium text-color"
          >Contraseña actual</label
        >
        <InputText id="currentPassword" v-model="currentPassword" type="password" class="w-full" />
      </div>

      <div class="space-y-2">
        <label for="newPassword" class="text-sm font-medium text-color">Nueva contraseña</label>
        <InputText
          id="newPassword"
          v-model="newPassword"
          type="password"
          class="w-full"
          :invalid="!!(newPassword && !passwordLengthOk)"
        />
        <small v-if="newPassword && !passwordLengthOk" class="text-red-500">
          Mínimo 8 caracteres
        </small>
      </div>

      <div class="space-y-2">
        <label for="confirmPassword" class="text-sm font-medium text-color"
          >Confirmar nueva contraseña</label
        >
        <InputText
          id="confirmPassword"
          v-model="confirmPassword"
          type="password"
          class="w-full"
          :invalid="!!(confirmPassword && !passwordsMatch)"
        />
        <small v-if="confirmPassword && !passwordsMatch" class="text-red-500">
          Las contraseñas no coinciden
        </small>
      </div>
    </div>

    <template #footer>
      <div class="flex gap-2 justify-end">
        <Button label="Cancelar" severity="secondary" @click="handleClose" />
        <Button
          label="Guardar"
          :disabled="!formValid"
          :loading="submitting"
          @click="handleSubmit"
        />
      </div>
    </template>
  </Dialog>
</template>
