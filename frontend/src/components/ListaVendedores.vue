<template>
  <div class="listas-container">

    <div class="dashboard-card">
      <h2 class="dashboard-title">Vendedores Tele</h2>
      <div v-if="props.vendedoresTele.length > 0" class="table-container">
        <table class="dashboard-table">
          <thead>
            <tr>
              <th>Nome do Vendedor</th>
              <th>Vendas</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="vendedor in props.vendedoresTele"
              :key="vendedor.nome"
              @click="emit('selecionar-vendedor', vendedor, 'tele')"
              class="clickable-row"
            >
              <td class="vendedor-name">{{ vendedor.nome }}</td>
              <td>{{ vendedor.total_vendas }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="no-data-message">Nenhum vendedor de telemarketing encontrado.</div>
    </div>

    <div class="dashboard-card">
      <h2 class="dashboard-title">Vendedores Porta a Porta</h2>
      <div class="filter-controls">
        <label for="filtro" class="filter-label">Filtrar Categoria:</label>
        <select
          id="filtro"
          :value="props.filtroCategoria"
          @change="emit('update-filtro', $event.target.value)"
          class="filter-select"
        >
          <option value="todos">Todos</option>
          <option value="porta">Porta a Porta</option>
          <option value="externa">Externa</option>
          <option value="Outro">Outros</option>
        </select>
      </div>
      <div v-if="props.vendedoresPorta.length > 0" class="table-container">
        <table class="dashboard-table">
          <thead>
            <tr>
              <th>Nome do Vendedor</th>
              <th>Vendas</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="vendedor in props.vendedoresPorta"
              :key="vendedor.nome"
              @click="emit('selecionar-vendedor', vendedor, vendedor.tipo_vendedor)"
              class="clickable-row"
            >
              <td class="vendedor-name">{{ vendedor.nome }}</td>
              <td>{{ vendedor.total_vendas }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="no-data-message">Nenhum vendedor encontrado para a categoria selecionada.</div>
    </div>

  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  vendedoresTele: Array,
  vendedoresPorta: Array,
  filtroCategoria: String
})

const emit = defineEmits(['selecionar-vendedor', 'update-filtro'])
</script>

<style scoped>
.listas-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  width: 100%;
}

.dashboard-card {
  width: 100%; /* <-- força os cards a ocuparem toda a coluna */
}


@media (max-width: 768px) {
  .listas-container {
    grid-template-columns: 1fr;
  }
}

.dashboard-card {
  background: #ffffff;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  color: #333;
}

.dashboard-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 16px;
  text-align: center;
  color: #1f2937;
}

.table-container {
  overflow-x: auto;
}

.dashboard-table {
  width: 100%;
  border-collapse: collapse;
  background-color: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.dashboard-table th,
.dashboard-table td {
  padding: 12px 16px;
  text-align: left;
  font-size: 0.95rem;
}

.dashboard-table th {
  background-color: #f3f4f6;
  color: #374151;
  font-weight: 600;
  border-bottom: 1px solid #e5e7eb;
}

.dashboard-table td {
  border-bottom: 1px solid #e5e7eb;
  color: #1f2937;
}

.clickable-row {
  cursor: pointer;
  transition: background-color 0.15s ease;
}

.clickable-row:hover {
  background-color: #f9fafb;
}

.vendedor-name {
  font-weight: 500;
}

.no-data-message {
  text-align: center;
  color: #6b7280;
  padding: 16px;
}

.filter-controls {
  margin-bottom: 16px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
}

.filter-label {
  font-weight: 500;
}

.filter-select {
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background-color: #ffffff;
}
:host{
  width: 100%;
}
</style>
