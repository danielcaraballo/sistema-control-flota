import { computed, ref, watch } from 'vue'

const THEME_KEY = 'theme-mode'
const OLD_THEME_KEY = 'theme'

function readInitialThemeMode() {
  try {
    const saved = localStorage.getItem(THEME_KEY)
    if (saved === 'light' || saved === 'dark' || saved === 'system') return saved
    const old = localStorage.getItem(OLD_THEME_KEY)
    if (old === 'dark') return 'dark'
    if (old === 'light') return 'light'
  } catch {}
  return 'system'
}

const themeMode = ref(readInitialThemeMode())
const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
const systemDark = ref(mediaQuery.matches)
let systemListenerActive = false

const isDark = computed(() => {
  if (themeMode.value === 'dark') return true
  if (themeMode.value === 'light') return false
  return systemDark.value
})

function updateSystemPref() {
  systemDark.value = mediaQuery.matches
}

function manageSystemListener() {
  if (themeMode.value === 'system' && !systemListenerActive) {
    mediaQuery.addEventListener('change', updateSystemPref)
    systemListenerActive = true
  } else if (themeMode.value !== 'system' && systemListenerActive) {
    mediaQuery.removeEventListener('change', updateSystemPref)
    systemListenerActive = false
  }
}

function syncDomAndStorage() {
  document.documentElement.classList.toggle('p-dark', isDark.value)
  localStorage.setItem(THEME_KEY, themeMode.value)
}

watch([themeMode, systemDark], () => {
  manageSystemListener()
  syncDomAndStorage()
})

manageSystemListener()
syncDomAndStorage()

export function readInitialTheme() {
  return themeMode.value
}

export function applyTheme() {
  /* theme is reactively applied */
}

export function useTheme() {
  return { isDark, themeMode, setThemeMode, toggleTheme }
}

function setThemeMode(mode) {
  themeMode.value = mode
}

function toggleTheme() {
  if (themeMode.value === 'light') themeMode.value = 'dark'
  else if (themeMode.value === 'dark') themeMode.value = 'system'
  else themeMode.value = 'light'
}
