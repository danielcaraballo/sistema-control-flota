<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <div class="default-layout">
    <aside class="sidebar">
      <div class="sidebar-header">
        <h2>SCF</h2>
      </div>
      <nav class="sidebar-nav">
        <ul>
          <li><router-link to="/">Dashboard</router-link></li>
          <li><router-link to="/vehiculos">Vehículos</router-link></li>
          <li><router-link to="/taller">Taller</router-link></li>
          <li><router-link to="/reportes">Reportes</router-link></li>
        </ul>
      </nav>
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
}

.sidebar-header {
  padding: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-header h2 {
  margin: 0;
  font-size: 1.25rem;
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

.sidebar-nav a:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.main-content {
  flex: 1;
  padding: 2rem;
  background-color: #f5f5f5;
  overflow-y: auto;
}
</style>
