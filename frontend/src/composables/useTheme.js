import { ref } from 'vue'

function readInitialTheme() {
  try {
    const saved = localStorage.getItem('theme')
    if (saved) return saved === 'dark'
  } catch {}
  return window.matchMedia('(prefers-color-scheme: dark)').matches
}

const isDark = ref(readInitialTheme())

function applyTheme(dark) {
  isDark.value = dark
  document.documentElement.classList.toggle('p-dark', dark)
  localStorage.setItem('theme', dark ? 'dark' : 'light')
}

function toggleTheme() {
  applyTheme(!isDark.value)
}

export { applyTheme, readInitialTheme }

export function useTheme() {
  return {
    isDark,
    toggleTheme,
  }
}
