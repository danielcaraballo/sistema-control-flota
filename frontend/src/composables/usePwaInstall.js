import { ref, onMounted, onUnmounted } from 'vue'

const deferredPrompt = ref(null)
const canInstall = ref(false)
const isInstalled = ref(false)
const isIos = ref(false)
const isAndroid = ref(false)

export function usePwaInstall() {
  function checkStandalone() {
    isInstalled.value =
      window.matchMedia('(display-mode: standalone)').matches ||
      window.navigator.standalone === true
  }

  function checkPlatform() {
    const userAgent = window.navigator.userAgent.toLowerCase()
    isIos.value = /iphone|ipad|ipod/.test(userAgent) && !window.MSStream
    isAndroid.value = /android/.test(userAgent)
  }

  function onBeforeInstallPrompt(e) {
    e.preventDefault()
    deferredPrompt.value = e
    canInstall.value = true
  }

  function onAppInstalled() {
    canInstall.value = false
    deferredPrompt.value = null
    isInstalled.value = true
  }

  onMounted(() => {
    checkStandalone()
    checkPlatform()
    window.addEventListener('beforeinstallprompt', onBeforeInstallPrompt)
    window.addEventListener('appinstalled', onAppInstalled)
  })

  onUnmounted(() => {
    window.removeEventListener('beforeinstallprompt', onBeforeInstallPrompt)
    window.removeEventListener('appinstalled', onAppInstalled)
  })

  async function promptInstall() {
    if (!deferredPrompt.value) return false
    deferredPrompt.value.prompt()
    const { outcome } = await deferredPrompt.value.userChoice
    if (outcome === 'accepted') {
      canInstall.value = false
      deferredPrompt.value = null
    }
    return outcome === 'accepted'
  }

  return {
    canInstall,
    isInstalled,
    isIos,
    isAndroid,
    promptInstall,
  }
}
