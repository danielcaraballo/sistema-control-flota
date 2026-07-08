<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { RouterView, useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { rolLabel, ROL_NACIONAL } from '@/utils/roles'
import Avatar from 'primevue/avatar'
import Button from 'primevue/button'
import UserDropdown from '@/components/UserDropdown.vue'

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()
const userDropdownRef = ref()
const dropdownOpen = ref(false)

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
  <div class="flex h-dvh">
    <aside
      class="sidebar fixed md:relative z-[100] flex flex-col bg-card border-r border-card-border overflow-hidden transition-all duration-200"
      :class="[
        isMobile ? (mobileOpen ? 'translate-x-0' : '-translate-x-full') : '',
        sidebarCollapsed && !isMobile ? 'w-[64px]' : 'w-[260px]',
      ]"
    >
      <div class="flex items-center min-h-14 px-5 border-b border-card-border shrink-0">
        <div class="flex items-center gap-2 font-bold text-color">
          <i class="pi pi-car text-xl" />
          <span v-show="!sidebarCollapsed || isMobile" class="text-xl">SCF</span>
        </div>
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
            class="flex items-center gap-3 px-5 py-2.5 text-sm font-medium text-muted-color cursor-pointer transition-all duration-150 border-l-3 border-transparent hover:text-color hover:bg-card-hover"
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
      class="fixed inset-0 bg-black/40 z-[99]"
      @click="closeMobile"
    />

    <div class="flex-1 flex flex-col min-w-0">
      <header
        class="h-14 flex items-center gap-3 px-6 bg-card border-b border-card-border shrink-0"
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
      </header>

      <main class="flex-1 p-6 md:p-8 bg-[var(--scf-page-bg)] overflow-y-auto">
        <RouterView />
      </main>
    </div>
  </div>
</template>
