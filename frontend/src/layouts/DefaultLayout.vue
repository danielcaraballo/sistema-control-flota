<script setup>
import { RouterView, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ref, computed } from 'vue'

const auth = useAuthStore()
const router = useRouter()

const menuItems = computed(() => {
  const items = [
    {
      label: 'Dashboard',
      icon: 'pi pi-home',
      command: () => router.push('/'),
    },
  ]

  if (auth.isGerenteNacional) {
    items.push({
      label: 'Usuarios',
      icon: 'pi pi-users',
      command: () => router.push('/usuarios'),
    })
  }

  items.push(
    {
      label: 'Vehículos',
      icon: 'pi pi-truck',
      command: () => router.push('/vehiculos'),
    },
    {
      label: 'Taller',
      icon: 'pi pi-wrench',
      command: () => router.push('/taller'),
    },
  )

  if (auth.isGerenteNacional || auth.isAnalistaNacional) {
    items.push({
      label: 'Reportes',
      icon: 'pi pi-chart-bar',
      command: () => router.push('/reportes'),
    })
  }

  return items
})

const rolLabel = computed(() => ({
  gerente_nacional: 'Gerente Nacional',
  analista_nacional: 'Analista Nacional',
  responsable_estatal: 'Responsable Estatal',
  mecanico: 'Mecánico',
}[auth.user?.rol] || ''))

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>

<template>
  <div class="layout">
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="brand">
          <i class="pi pi-car" style="font-size: 1.5rem"></i>
          <span class="brand-text">SCF</span>
        </div>
        <Tag :value="rolLabel" severity="info" />
      </div>

      <PanelMenu :model="menuItems" class="sidebar-menu" />

      <div class="sidebar-footer">
        <div class="user-info">
          <Avatar
            :label="(auth.user?.first_name?.[0] || '').toUpperCase()"
            size="small"
            shape="circle"
          />
          <div class="user-details">
            <span class="user-name">{{ auth.user?.first_name }} {{ auth.user?.last_name }}</span>
            <span class="user-email">{{ auth.user?.email }}</span>
          </div>
        </div>
        <Button
          icon="pi pi-sign-out"
          severity="secondary"
          text
          rounded
          @click="handleLogout"
          v-tooltip.bottom="'Cerrar sesión'"
        />
      </div>
    </aside>

    <main class="content">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 280px;
  background: var(--p-surface-0);
  border-right: 1px solid var(--p-surface-200);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.sidebar-header {
  padding: 1.25rem;
  border-bottom: 1px solid var(--p-surface-200);
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--p-primary-color);
}

.brand-text {
  font-size: 1.5rem;
}

.sidebar-menu {
  flex: 1;
  border: none;
  overflow-y: auto;
}

.sidebar-footer {
  padding: 1rem 1.25rem;
  border-top: 1px solid var(--p-surface-200);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.625rem;
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
}

.user-name {
  font-size: 0.875rem;
  font-weight: 500;
  line-height: 1;
}

.user-email {
  font-size: 0.75rem;
  color: var(--p-text-muted-color);
  line-height: 1;
}

.content {
  flex: 1;
  padding: 2rem;
  background: var(--p-surface-50);
  overflow-y: auto;
}
</style>
