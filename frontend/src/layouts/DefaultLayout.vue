<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { RouterView, useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { rolLabel, ROL_NACIONAL } from '@/utils/roles'
import { isDemoMode } from '@/utils/demo'
import Avatar from 'primevue/avatar'
import Button from 'primevue/button'
import UserDropdown from '@/components/UserDropdown.vue'
import QrScannerModal from '@/components/QrScannerModal.vue'

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()
const userDropdownRef = ref()
const dropdownOpen = ref(false)
const showScanner = ref(false)

function onScanned(vehicleId) {
  router.push(`/vehiculos/${vehicleId}`)
}
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

const menuSections = computed(() => {
  const mainItems = [
    { label: 'Dashboard', icon: 'pi pi-home', routeName: 'dashboard', path: '/' },
    { label: 'Vehículos', icon: 'pi pi-truck', routeName: 'vehiculos', path: '/vehiculos' },
    { label: 'Taller', icon: 'pi pi-wrench', routeName: 'taller', path: '/taller' },
  ]
  if (auth.tieneRol(ROL_NACIONAL)) {
    mainItems.push({
      label: 'Reportes',
      icon: 'pi pi-chart-bar',
      routeName: 'reportes',
      path: '/reportes',
    })
  }
  const sections = [{ items: mainItems }]

  if (auth.tieneRol(ROL_NACIONAL)) {
    sections.push({
      label: 'Administración',
      items: [
        { label: 'Usuarios', icon: 'pi pi-users', routeName: 'usuarios', path: '/usuarios' },
        {
          label: 'Organización',
          icon: 'pi pi-sitemap',
          routeName: 'organizacion',
          path: '/organizacion',
        },
        { label: 'Catálogos', icon: 'pi pi-book', routeName: 'catalogos', path: '/catalogos' },
      ],
    })
  }
  return sections
})

const userRolLabel = computed(() => rolLabel(auth.user?.rol))
</script>

<template>
  <div class="flex h-dvh overflow-hidden">
    <aside
      class="sidebar fixed md:relative inset-y-0 left-0 z-[100] flex flex-col bg-card border-r border-card-border overflow-hidden transition-all duration-200"
      :class="[
        isMobile ? (mobileOpen ? 'translate-x-0' : '-translate-x-full') : '',
        sidebarCollapsed && !isMobile ? 'w-[64px]' : 'w-[260px]',
      ]"
    >
      <div class="flex items-center min-h-14 px-5 border-b border-card-border shrink-0">
        <div class="flex items-center gap-2 font-bold text-color">
          <i class="pi pi-car text-xl text-[var(--p-primary-color)]" />
          <span v-show="!sidebarCollapsed || isMobile" class="text-xl">SCF</span>
        </div>
        <Button
          v-if="isMobile"
          icon="pi pi-times"
          severity="secondary"
          text
          rounded
          class="ml-auto !w-9 !h-9"
          @click="closeMobile"
        />
      </div>

      <nav class="flex-1 overflow-y-auto py-2">
        <template v-for="(section, si) in menuSections" :key="si">
          <div
            v-if="section.label"
            v-show="!sidebarCollapsed || isMobile"
            class="px-5 pt-4 pb-1 text-xs font-semibold text-muted-color uppercase tracking-wider"
          >
            {{ section.label }}
          </div>
          <a
            v-for="item in section.items"
            :key="item.routeName"
            class="flex items-center gap-3 px-5 py-3 md:py-2.5 text-sm font-medium text-muted-color cursor-pointer transition-all duration-150 border-l-3 border-transparent hover:text-color hover:bg-card-hover"
            :class="{
              '!text-primary !bg-card-hover !border-l-[var(--p-primary-color)]':
                route.path === item.path ||
                (item.path !== '/' && route.path.startsWith(item.path + '/')),
            }"
            @click="navigate(item.path)"
          >
            <span class="w-7 h-7 flex items-center justify-center shrink-0">
              <i :class="item.icon" class="text-base" />
            </span>
            <span v-show="!sidebarCollapsed || isMobile" class="truncate">{{ item.label }}</span>
          </a>
        </template>
      </nav>

      <div
        class="border-t border-card-border shrink-0 cursor-pointer select-none"
        @click="userDropdownRef?.toggle($event)"
      >
        <div class="flex items-center gap-2.5 px-5 py-3">
          <Avatar
            :label="(auth.user?.first_name?.[0] || '').toUpperCase()"
            size="small"
            shape="square"
            class="!bg-[var(--p-primary-color)] shrink-0 !rounded-lg"
          />
          <div
            v-show="!sidebarCollapsed || isMobile"
            class="flex flex-col gap-0.5 overflow-hidden min-w-0"
          >
            <span class="text-sm font-semibold text-color leading-none truncate">
              {{ auth.user?.first_name }} {{ auth.user?.last_name }}
            </span>
            <span class="text-xs text-muted-color leading-none truncate">{{ userRolLabel }}</span>
          </div>
          <i
            v-show="!sidebarCollapsed || isMobile"
            class="pi text-muted-color text-xs ml-auto shrink-0 transition-transform duration-200"
            :class="dropdownOpen ? 'pi-chevron-down' : 'pi-chevron-up'"
          />
        </div>
      </div>
    </aside>

    <UserDropdown ref="userDropdownRef" @show="dropdownOpen = true" @hide="dropdownOpen = false" />

    <div
      v-if="isMobile && mobileOpen"
      class="fixed inset-0 bg-black/50 backdrop-blur-xs z-[99] transition-opacity"
      @click="closeMobile"
    />

    <div class="flex-1 flex flex-col min-w-0 overflow-hidden">
      <header
        class="h-14 flex items-center gap-2 sm:gap-3 px-3 sm:px-6 bg-card border-b border-card-border shrink-0"
      >
        <Button
          icon="pi pi-bars"
          severity="secondary"
          text
          rounded
          class="!hidden md:!inline-flex !w-10 !h-10"
          @click="toggleSidebar"
          v-tooltip.bottom="'Colapsar sidebar'"
        />
        <div class="flex items-center gap-1.5 text-color sm:hidden">
          <i class="pi pi-car text-lg text-[var(--p-primary-color)]" />
          <span class="text-sm font-bold tracking-tight">SCF</span>
        </div>
        <span class="text-sm font-medium text-muted-color hidden sm:inline"
          >Sistema de Control de Flota</span
        >
        <span
          v-if="isDemoMode"
          class="ml-1 sm:ml-2 inline-flex items-center gap-1 rounded-full bg-amber-100 dark:bg-amber-900/30 px-2 py-0.5 text-xs font-medium text-amber-700 dark:text-amber-400 shrink-0"
        >
          <i class="pi pi-code text-amber-500 text-xs" />
          Demo
        </span>
        <div class="flex-1" />
        <Button
          icon="pi pi-camera"
          severity="secondary"
          text
          rounded
          class="!w-10 !h-10"
          @click="showScanner = true"
          v-tooltip.bottom="'Escanear QR'"
        />
      </header>

      <main
        class="flex-1 p-3 sm:p-4 md:p-6 lg:p-8 bg-[var(--scf-page-bg)] overflow-y-auto pb-20 md:pb-6"
      >
        <RouterView />
      </main>

      <!-- Bottom Navigation Bar for Mobile Phones -->
      <nav
        class="md:hidden fixed bottom-0 left-0 right-0 z-40 bg-card border-t border-card-border flex items-center justify-around h-16 px-1 shadow-lg"
      >
        <button
          type="button"
          class="flex flex-col items-center justify-center min-w-[64px] h-12 rounded-lg gap-1 transition-colors text-xs font-medium"
          :class="
            route.path === '/' ? 'text-primary font-semibold' : 'text-muted-color hover:text-color'
          "
          @click="navigate('/')"
        >
          <i class="pi pi-home text-lg" />
          <span>Inicio</span>
        </button>
        <button
          type="button"
          class="flex flex-col items-center justify-center min-w-[64px] h-12 rounded-lg gap-1 transition-colors text-xs font-medium"
          :class="
            route.path.startsWith('/vehiculos')
              ? 'text-primary font-semibold'
              : 'text-muted-color hover:text-color'
          "
          @click="navigate('/vehiculos')"
        >
          <i class="pi pi-truck text-lg" />
          <span>Vehículos</span>
        </button>
        <button
          type="button"
          class="flex flex-col items-center justify-center min-w-[64px] h-12 rounded-lg gap-1 transition-colors text-xs font-medium"
          :class="
            route.path.startsWith('/taller')
              ? 'text-primary font-semibold'
              : 'text-muted-color hover:text-color'
          "
          @click="navigate('/taller')"
        >
          <i class="pi pi-wrench text-lg" />
          <span>Taller</span>
        </button>
        <button
          type="button"
          class="flex flex-col items-center justify-center min-w-[64px] h-12 rounded-lg gap-1 transition-colors text-xs font-medium text-muted-color hover:text-color"
          @click="toggleSidebar"
        >
          <i class="pi pi-th-large text-lg" />
          <span>Más</span>
        </button>
      </nav>
    </div>
  </div>

  <QrScannerModal v-model:visible="showScanner" @scan="onScanned" />
</template>
