<script setup>
</script>

<template>
  <div class="dashboard">
    <h1>Dashboard</h1>
    <div class="kpi-grid">
      <div class="kpi-card">
        <h3>Vehículos Operativos</h3>
        <p class="kpi-value">—</p>
      </div>
      <div class="kpi-card">
        <h3>En Taller</h3>
        <p class="kpi-value">—</p>
      </div>
      <div class="kpi-card">
        <h3>Alertas Preventivas</h3>
        <p class="kpi-value">—</p>
      </div>
      <div class="kpi-card">
        <h3>MTTR (horas)</h3>
        <p class="kpi-value">—</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard h1 {
  margin: 0 0 1.5rem;
  color: #1a1a2e;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.kpi-card {
  background: #fff;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
}

.kpi-card h3 {
  margin: 0 0 0.5rem;
  font-size: 0.875rem;
  color: #666;
}

.kpi-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1a1a2e;
  margin: 0;
}
</style>
