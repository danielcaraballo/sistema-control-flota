<script setup>
</script>

<template>
  <div class="dashboard-page">
    <h1>Dashboard</h1>
    <div class="kpi-grid">
      <Card>
        <template #title>Vehículos Operativos</template>
        <template #content>
          <p class="kpi-value">—</p>
        </template>
      </Card>
      <Card>
        <template #title>En Taller</template>
        <template #content>
          <p class="kpi-value">—</p>
        </template>
      </Card>
      <Card>
        <template #title>Alertas Preventivas</template>
        <template #content>
          <p class="kpi-value">—</p>
        </template>
      </Card>
      <Card>
        <template #title>MTTR (horas)</template>
        <template #content>
          <p class="kpi-value">—</p>
        </template>
      </Card>
    </div>
  </div>
</template>

<style scoped>
.dashboard-page h1 {
  margin: 0 0 1.5rem;
  font-size: 1.5rem;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1rem;
}

.kpi-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--p-primary-color);
  margin: 0;
}
</style>
