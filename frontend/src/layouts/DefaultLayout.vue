<script setup>
import { RouterView, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>

<template>
  <div class="default-layout">
    <aside class="sidebar">
      <div class="sidebar-header">
        <h2>SCF</h2>
        <span class="user-rol">{{ auth.user?.rol ? {gerente_nacional:'Gerente Nacional',analista_nacional:'Analista Nacional',responsable_estatal:'Responsable Estatal',mecanico:'Mecánico'}[auth.user.rol] : '' }}</span>
      </div>
      <nav class="sidebar-nav">
        <ul>
          <li><router-link to="/">Dashboard</router-link></li>
          <li v-if="auth.isGerenteNacional"><router-link to="/usuarios">Usuarios</router-link></li>
          <li><router-link to="/vehiculos">Vehículos</router-link></li>
          <li><router-link to="/taller">Taller</router-link></li>
          <li v-if="auth.isGerenteNacional || auth.isAnalistaNacional"><router-link to="/reportes">Reportes</router-link></li>
        </ul>
      </nav>
      <div class="sidebar-footer">
        <span class="user-name">{{ auth.user?.first_name }} {{ auth.user?.last_name }}</span>
        <button class="logout-btn" @click="handleLogout">Cerrar sesión</button>
      </div>
    </aside>
    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.default-layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 260px;
  background-color: #1a1a2e;
  color: #fff;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.sidebar-header {
  padding: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-header h2 {
  margin: 0;
  font-size: 1.25rem;
}

.user-rol {
  font-size: 0.75rem;
  opacity: 0.7;
  display: block;
  margin-top: 0.25rem;
}

.sidebar-nav {
  flex: 1;
}

.sidebar-nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar-nav li {
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.sidebar-nav a {
  display: block;
  padding: 0.875rem 1.5rem;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: background-color 0.2s;
}

.sidebar-nav a:hover,
.sidebar-nav a.router-link-exact-active {
  background-color: rgba(255, 255, 255, 0.1);
}

.sidebar-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.user-name {
  display: block;
  font-size: 0.8rem;
  opacity: 0.8;
  margin-bottom: 0.5rem;
}

.logout-btn {
  width: 100%;
  padding: 0.5rem;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: rgba(255, 255, 255, 0.8);
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
}

.logout-btn:hover {
  background: rgba(255, 255, 255, 0.1);
}

.main-content {
  flex: 1;
  padding: 2rem;
  background-color: #f5f5f5;
  overflow-y: auto;
}
</style>
