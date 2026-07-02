<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { RouterView, useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useTheme } from '@/composables/useTheme'
import { rolLabel } from '@/utils/roles'
import Avatar from 'primevue/avatar'
import Button from 'primevue/button'

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

const { isDark, toggleTheme } = useTheme()

const sidebarCollapsed = ref(false)
const mobileOpen = ref(false)
const isMobile = ref(false)

function checkMobile() {
  isMobile.value = window.innerWidth < 768
  if (isMobile.value) mobileOpen.value = false
}

onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
})

function toggleSidebar() {
  if (isMobile.value) {
    mobileOpen.value = !mobileOpen.value
  } else {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }
}

function closeMobile() {
  mobileOpen.value = false
}

function navigate(path) {
  router.push(path)
  closeMobile()
}

const menuItems = computed(() => {
  const items = [{ label: 'Dashboard', icon: 'pi pi-home', routeName: 'dashboard', path: '/' }]
  if (auth.tieneRol('nacional')) {
    items.push({ label: 'Usuarios', icon: 'pi pi-users', routeName: 'usuarios', path: '/usuarios' })
  }
  items.push({
    label: 'Vehículos',
    icon: 'pi pi-truck',
    routeName: 'vehiculos',
    path: '/vehiculos',
  })
  if (auth.tieneRol('nacional')) {
    items.push({
      label: 'Catálogos',
      icon: 'pi pi-book',
      routeName: 'catalogos',
      path: '/catalogos',
    })
  }
  items.push({ label: 'Taller', icon: 'pi pi-wrench', routeName: 'taller', path: '/taller' })
  if (auth.tieneRol('analista')) {
    items.push({
      label: 'Reportes',
      icon: 'pi pi-chart-bar',
      routeName: 'reportes',
      path: '/reportes',
    })
  }
  return items
})

const userRolLabel = computed(() => rolLabel(auth.user?.rol))

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>

<template>
  <div class="flex h-dvh">
    <aside
      class="sidebar fixed md:relative z-[100] flex flex-col bg-[#1e293c] overflow-hidden transition-all duration-200"
      :class="[
        isMobile ? (mobileOpen ? 'translate-x-0' : '-translate-x-full') : '',
        sidebarCollapsed && !isMobile ? 'w-[64px]' : 'w-[260px]',
      ]"
    >
      <div class="flex items-center min-h-14 px-5 border-b border-white/10 shrink-0">
        <div class="flex items-center gap-2 font-bold text-white">
          <i class="pi pi-car text-xl" />
          <span v-show="!sidebarCollapsed || isMobile" class="text-xl">SCF</span>
        </div>
      </div>

      <nav class="flex-1 overflow-y-auto py-2">
        <a
          v-for="item in menuItems"
          :key="item.routeName"
          class="flex items-center gap-3 px-5 py-2.5 text-sm font-medium text-white/65 cursor-pointer transition-all duration-150 border-l-3 border-transparent hover:text-white hover:bg-white/5"
          :class="{
            '!text-white !bg-white/8 !border-l-[var(--p-primary-color)]':
              route.name === item.routeName,
          }"
          @click="navigate(item.path)"
        >
          <span class="w-7 h-7 flex items-center justify-center shrink-0">
            <i :class="item.icon" class="text-base" />
          </span>
          <span v-show="!sidebarCollapsed || isMobile" class="truncate">{{ item.label }}</span>
        </a>
      </nav>

      <div class="flex items-center justify-between px-5 py-3 border-t border-white/10 shrink-0">
        <div class="flex items-center gap-2.5 overflow-hidden min-w-0">
          <Avatar
            :label="(auth.user?.first_name?.[0] || '').toUpperCase()"
            size="small"
            shape="circle"
            class="!bg-[var(--p-primary-color)] shrink-0"
          />
          <div v-show="!sidebarCollapsed || isMobile" class="flex flex-col gap-0.5 overflow-hidden">
            <span class="text-sm font-semibold text-white leading-none truncate">
              {{ auth.user?.first_name }} {{ auth.user?.last_name }}
            </span>
            <span class="text-xs text-white/50 leading-none truncate">{{ userRolLabel }}</span>
          </div>
        </div>
        <Button
          icon="pi pi-sign-out"
          severity="secondary"
          text
          rounded
          @click="handleLogout"
          v-tooltip.bottom="'Cerrar sesión'"
          class="!text-white/45 hover:!text-white shrink-0"
        />
      </div>
    </aside>

    <div
      v-if="isMobile && mobileOpen"
      class="fixed inset-0 bg-black/40 z-[99]"
      @click="closeMobile"
    />

    <div class="flex-1 flex flex-col min-w-0">
      <header
        class="h-14 flex items-center gap-3 px-6 bg-white dark:bg-surface-50 border-b border-surface-200 shrink-0"
      >
        <Button
          icon="pi pi-bars"
          severity="secondary"
          text
          rounded
          @click="toggleSidebar"
          v-tooltip.bottom="isMobile ? 'Menú' : 'Colapsar sidebar'"
        />
        <span class="text-sm font-medium text-muted-color">Sistema de Control de Flota</span>
        <div class="flex-1" />

        <Button
          :icon="isDark ? 'pi pi-sun' : 'pi pi-moon'"
          severity="secondary"
          text
          rounded
          @click="toggleTheme"
          v-tooltip.bottom="isDark ? 'Modo claro' : 'Modo oscuro'"
        />
      </header>

      <main class="flex-1 p-6 md:p-8 bg-surface-50 overflow-y-auto">
        <RouterView />
      </main>
    </div>
  </div>
</template>
