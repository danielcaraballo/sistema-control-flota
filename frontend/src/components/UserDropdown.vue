<script setup>
import { ref, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useTheme } from '@/composables/useTheme'
import Popover from 'primevue/popover'
import ChangePasswordDialog from './ChangePasswordDialog.vue'

const POPOVER_WIDTH = 244

const emit = defineEmits(['show', 'hide'])

const auth = useAuthStore()
const router = useRouter()
const { themeMode, setThemeMode } = useTheme()
const popoverRef = ref()
const showChangePassword = ref(false)

let positionTarget = null

function ensureTarget() {
  if (!positionTarget || !document.body.contains(positionTarget)) {
    positionTarget = document.createElement('div')
    positionTarget.style.cssText = 'position:fixed;width:0;height:0;pointer-events:none'
    document.body.appendChild(positionTarget)
  }
  return positionTarget
}

function toggle(event) {
  const trigger = event.currentTarget
  const triggerRect = trigger.getBoundingClientRect()
  const target = ensureTarget()
  const left = triggerRect.left + (triggerRect.width - POPOVER_WIDTH) / 2
  target.style.left = `${left}px`
  target.style.top = `${triggerRect.top}px`
  popoverRef.value.toggle(event, target)
}

defineExpose({ toggle })

function handleLogout() {
  auth.logout()
  router.push('/login')
}

onUnmounted(() => {
  if (positionTarget && document.body.contains(positionTarget)) {
    positionTarget.remove()
  }
})
</script>

<template>
  <Popover
    ref="popoverRef"
    class="!w-[244px] user-dropdown-popover"
    :pt="{ content: { class: '!p-0' } }"
    @show="emit('show')"
    @hide="emit('hide')"
  >
    <div class="flex flex-col py-2">
      <div
        class="flex border border-surface-200 dark:border-surface-600 rounded-md mx-3 overflow-hidden"
      >
        <button
          v-for="opt in [
            { icon: 'pi pi-sun', label: 'Claro', value: 'light' },
            { icon: 'pi pi-moon', label: 'Oscuro', value: 'dark' },
            { icon: 'pi pi-desktop', label: 'Sistema', value: 'system' },
          ]"
          :key="opt.value"
          class="flex-1 flex items-center justify-center gap-1.5 px-2 py-1.5 text-sm transition-colors cursor-pointer"
          :class="
            themeMode === opt.value
              ? 'bg-primary text-primary-contrast font-medium'
              : 'text-muted-color hover:bg-surface-100 dark:hover:bg-surface-700'
          "
          @click="setThemeMode(opt.value)"
        >
          <i :class="[opt.icon, 'text-sm']" />
          <span class="text-xs">{{ opt.label }}</span>
        </button>
      </div>

      <hr class="border-surface-200 dark:border-surface-600 mx-3 my-2" />

      <button
        class="flex items-center gap-3 px-4 py-2.5 text-sm transition-colors cursor-pointer w-full text-left text-color hover:bg-surface-100 dark:hover:bg-surface-700"
        @click="showChangePassword = true"
      >
        <i class="pi pi-key text-muted-color" />
        <span>Cambiar contraseña</span>
      </button>

      <hr class="border-surface-200 dark:border-surface-600 mx-3 my-2" />

      <button
        class="flex items-center gap-3 px-4 py-2.5 text-sm transition-colors cursor-pointer w-full text-left text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20"
        @click="handleLogout"
      >
        <i class="pi pi-sign-out" />
        <span>Cerrar sesión</span>
      </button>
    </div>
  </Popover>

  <ChangePasswordDialog v-if="showChangePassword" @close="showChangePassword = false" />
</template>

<style>
.user-dropdown-popover::before,
.user-dropdown-popover::after {
  display: none !important;
}
</style>
