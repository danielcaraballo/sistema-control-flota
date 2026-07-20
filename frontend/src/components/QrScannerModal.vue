<script setup>
import { ref, watch } from 'vue'
import { useToast } from 'primevue/usetoast'
import { QrcodeStream, QrcodeDropZone } from 'vue-qrcode-reader'
import { BarcodeDetector } from 'barcode-detector/pure'
import Dialog from 'primevue/dialog'
import Button from 'primevue/button'
import TabView from 'primevue/tabview'
import TabPanel from 'primevue/tabpanel'
import { useAuthStore } from '@/stores/auth'
import { ROL_MECANICO } from '@/utils/roles'
import api from '@/services/api'

defineOptions({ inheritAttrs: false })

const props = defineProps({ visible: Boolean })
const emit = defineEmits(['update:visible', 'scan'])

const toast = useToast()
const auth = useAuthStore()

const activeTab = ref(0)
const isPaused = ref(false)
const isProcessing = ref(false)
const cameraError = ref(null)
const cameraErrorType = ref('camera')
const scanSuccess = ref(false)
const isDragOver = ref(false)
const fileInputRef = ref(null)

function extractVehicleId(rawValue) {
  try {
    const url = new URL(rawValue)
    const match = url.pathname.match(/^\/vehiculos\/(\d+)/)
    if (match) return parseInt(match[1])
  } catch {
    // not a URL, maybe just a plain ID
  }
  if (/^\d+$/.test(rawValue)) return parseInt(rawValue)
  return null
}

async function onDetect(detectedCodes) {
  if (isProcessing.value || detectedCodes.length === 0 || !detectedCodes[0]?.rawValue) return
  isProcessing.value = true
  isPaused.value = true
  try {
    await handleResult(detectedCodes[0].rawValue, 'cámara')
  } catch {
    isProcessing.value = false
    isPaused.value = false
  }
}

async function onCaptureDetect(detectedCodes) {
  if (isProcessing.value || detectedCodes.length === 0 || !detectedCodes[0]?.rawValue) return
  isProcessing.value = true
  try {
    await handleResult(detectedCodes[0].rawValue, 'archivo')
  } catch {
    isProcessing.value = false
  }
}

async function onFileSelected(event) {
  const file = event.target.files[0]
  if (!file) return
  isProcessing.value = true

  try {
    const imageBitmap = await createImageBitmap(file)
    const detector = new BarcodeDetector({ formats: ['qr_code'] })
    const codes = await detector.detect(imageBitmap)

    if (codes.length > 0 && codes[0]?.rawValue) {
      await handleResult(codes[0].rawValue, 'archivo')
    } else {
      toast.add({
        severity: 'error',
        summary: 'QR no encontrado',
        detail: 'No se detectó un código QR en la imagen',
        life: 3000,
      })
      isProcessing.value = false
    }
  } catch (err) {
    const msg =
      err?.message?.includes('WASM') || err?.message?.includes('wasm')
        ? 'El motor de detección no está disponible. Recarga la página e intenta de nuevo.'
        : 'No se pudo procesar la imagen seleccionada'
    toast.add({
      severity: 'error',
      summary: 'Error al procesar',
      detail: msg,
      life: 4000,
    })
    isProcessing.value = false
  }

  event.target.value = ''
}

async function handleResult(rawValue, source) {
  const vehicleId = extractVehicleId(rawValue)

  if (!vehicleId) {
    toast.add({
      severity: 'error',
      summary: 'QR inválido',
      detail: `El código ${source === 'cámara' ? 'escaneado' : 'seleccionado'} no corresponde a un vehículo`,
      life: 3000,
    })
    isProcessing.value = false
    isPaused.value = false
    return
  }

  if (!auth.tieneRol(ROL_MECANICO)) {
    toast.add({
      severity: 'error',
      summary: 'Sin permisos',
      detail: 'No tienes permisos suficientes para ver información de vehículos',
      life: 4000,
    })
    close()
    return
  }

  try {
    await api.get(`/vehiculos/${vehicleId}`)

    // brief success animation before closing
    scanSuccess.value = true
    if (navigator.vibrate) navigator.vibrate(30)
    await new Promise((r) => setTimeout(r, 600))

    emit('scan', vehicleId)
    close()
  } catch (err) {
    if (err.response?.status === 403) {
      toast.add({
        severity: 'error',
        summary: 'Sin permisos',
        detail: 'No tienes permisos para acceder a este vehículo',
        life: 4000,
      })
    } else if (err.response?.status === 404) {
      toast.add({
        severity: 'error',
        summary: 'No encontrado',
        detail: 'El vehículo no existe o ha sido desactivado',
        life: 3000,
      })
    } else if (!err.response) {
      toast.add({
        severity: 'error',
        summary: 'Error de conexión',
        detail: 'No se pudo conectar con el servidor. Verifica tu conexión.',
        life: 4000,
      })
    } else {
      toast.add({
        severity: 'error',
        summary: 'Error',
        detail: 'No se pudo obtener la información del vehículo',
        life: 3000,
      })
    }
    isProcessing.value = false
    isPaused.value = false
  }
}

function onCameraReady() {
  cameraError.value = null
  cameraErrorType.value = 'camera'
}

function retryCamera() {
  cameraError.value = null
  cameraErrorType.value = 'camera'
}

function onCameraError(err) {
  cameraError.value = err
  const msg = err?.message || ''
  if (msg.includes('wasm') || msg.includes('WASM')) {
    cameraErrorType.value = 'wasm'
  } else if (err?.name === 'NotAllowedError') {
    cameraErrorType.value = 'permission'
  } else {
    cameraErrorType.value = 'camera'
  }
}

function onDropError(err) {
  const msg =
    err?.message?.includes('WASM') || err?.message?.includes('wasm')
      ? 'El motor de detección no está disponible. Recarga la página e intenta de nuevo.'
      : 'No se pudo procesar la imagen arrastrada'
  toast.add({
    severity: 'error',
    summary: 'Error al leer imagen',
    detail: msg,
    life: 4000,
  })
}

function close() {
  scanSuccess.value = false
  isPaused.value = false
  isProcessing.value = false
  cameraError.value = null
  cameraErrorType.value = 'camera'
  isDragOver.value = false
  emit('update:visible', false)
}

watch(
  () => props.visible,
  (val) => {
    if (!val) {
      scanSuccess.value = false
      isPaused.value = false
      isProcessing.value = false
      cameraError.value = null
      cameraErrorType.value = 'camera'
      isDragOver.value = false
    }
  },
)
</script>

<template>
  <Dialog
    :visible="visible"
    modal
    :dismissable="!isProcessing"
    :closable="!isProcessing"
    :pt="{
      root: 'scanner-dialog',
      content: '!p-0',
    }"
    :style="{ width: 'min(480px, calc(100vw - 1rem))' }"
    @update:visible="close"
  >
    <template #header>
      <div class="flex items-center gap-2 text-lg font-semibold">
        <i class="pi pi-camera" />
        <span>Escanear QR</span>
      </div>
    </template>

    <div class="tabview-wrapper min-h-[340px] max-h-[55vh] flex flex-col">
      <TabView v-model:activeIndex="activeTab">
        <TabPanel header="Cámara">
          <div
            class="relative flex-1 min-h-0 rounded-md overflow-hidden bg-black flex items-center justify-center"
          >
            <QrcodeStream
              v-if="visible"
              :paused="isPaused || activeTab === 1"
              :constraints="{ facingMode: 'environment' }"
              :formats="['qr_code']"
              class="w-full h-full object-contain"
              @detect="onDetect"
              @camera-on="onCameraReady"
              @error="onCameraError"
            />

            <!-- Error overlay -->
            <div
              v-if="cameraError"
              class="absolute inset-0 flex flex-col items-center justify-center gap-3 bg-black/80 text-white p-6 text-center"
            >
              <i class="pi pi-exclamation-triangle text-3xl text-yellow-400" />
              <p class="font-medium">
                {{ cameraErrorType === 'wasm' ? 'Error de detección' : 'Error de cámara' }}
              </p>
              <p class="text-sm text-white/70">
                {{
                  cameraErrorType === 'wasm'
                    ? 'El motor de detección no está disponible. Recarga la página e intenta de nuevo.'
                    : cameraErrorType === 'permission'
                      ? 'Permiso de cámara denegado. Habilita el acceso en la configuración del navegador.'
                      : cameraError.message ||
                        'No se pudo acceder a la cámara. Verifica los permisos.'
                }}
              </p>
              <Button label="Reintentar" size="small" @click="retryCamera" />
            </div>

            <!-- Success overlay -->
            <div
              v-if="scanSuccess"
              class="absolute inset-0 flex items-center justify-center bg-black/60"
            >
              <div class="flex flex-col items-center gap-2">
                <i class="pi pi-check-circle text-4xl text-green-400" />
                <span class="text-sm font-medium text-white">QR detectado</span>
              </div>
            </div>

            <!-- Processing overlay -->
            <div
              v-else-if="isPaused && isProcessing"
              class="absolute inset-0 flex items-center justify-center bg-black/60"
            >
              <i class="pi pi-spin pi-spinner text-3xl text-white" />
            </div>

            <!-- Hint overlay -->
            <div
              class="absolute bottom-0 left-0 right-0 flex justify-center pb-3 pointer-events-none"
            >
              <span
                class="text-xs text-white/70 bg-black/50 px-3 py-1 rounded-full backdrop-blur-sm"
              >
                Apunta la cámara hacia el código QR del vehículo
              </span>
            </div>
          </div>
        </TabPanel>

        <TabPanel header="Subir imagen">
          <div
            class="relative flex-1 min-h-0 rounded-md overflow-hidden bg-surface-100 dark:bg-surface-800 flex items-center justify-center"
          >
            <input
              ref="fileInputRef"
              type="file"
              accept="image/*"
              class="hidden"
              @change="onFileSelected"
            />

            <QrcodeDropZone
              v-if="visible"
              class="w-full h-full cursor-pointer"
              @detect="onCaptureDetect"
              @error="onDropError"
              @dragover="isDragOver = $event"
              @click="fileInputRef?.click()"
            >
              <div
                class="flex flex-col items-center justify-center h-full gap-4 p-8 border-2 border-dashed rounded-xl transition-all duration-200"
                :class="
                  isDragOver
                    ? 'border-primary bg-primary/10 scale-[1.02]'
                    : 'border-muted-color hover:border-primary/50'
                "
              >
                <i
                  class="pi pi-image text-5xl transition-colors duration-200"
                  :class="isDragOver ? 'text-primary' : 'text-muted-color'"
                />
                <p class="text-sm text-muted-color text-center max-w-xs">
                  Arrastra una imagen con QR o haz clic para seleccionar
                </p>
                <p v-if="isDragOver" class="text-xs text-primary font-medium animate-pulse">
                  Suelta para escanear
                </p>
              </div>
            </QrcodeDropZone>

            <!-- Success overlay -->
            <div
              v-if="scanSuccess"
              class="absolute inset-0 flex items-center justify-center bg-black/60"
            >
              <div class="flex flex-col items-center gap-2">
                <i class="pi pi-check-circle text-4xl text-green-400" />
                <span class="text-sm font-medium text-white">QR detectado</span>
              </div>
            </div>

            <!-- Processing overlay -->
            <div
              v-else-if="isProcessing"
              class="absolute inset-0 flex items-center justify-center bg-black/60"
            >
              <i class="pi pi-spin pi-spinner text-3xl text-white" />
            </div>
          </div>
        </TabPanel>
      </TabView>
    </div>

    <template #footer>
      <Button label="Cancelar" severity="secondary" @click="close" />
    </template>
  </Dialog>
</template>

<style scoped>
:deep(.scanner-dialog) {
  max-height: 90vh;
}
:deep(.scanner-dialog .p-dialog-content) {
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
:deep(.tabview-wrapper) {
  display: flex;
  flex-direction: column;
}
:deep(.tabview-wrapper .p-tabview) {
  display: flex;
  flex-direction: column;
  min-height: 0;
  flex: 1;
}
:deep(.tabview-wrapper .p-tabview-panels) {
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
}
:deep(.tabview-wrapper .p-tabview-panel) {
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
}
:deep(.tabview-wrapper .p-tabview-panel > .p-tabpanel) {
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
}
.hidden {
  display: none;
}
</style>
