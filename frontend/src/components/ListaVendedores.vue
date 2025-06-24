<template>
  <div class="dashboard-card">
    <h2 class="dashboard-title">Vendedores Tele</h2>
    <div v-if="vendedoresTele.length > 0" class="table-container">
      <table class="dashboard-table">
        <thead>
          <tr>
            <th>Nome do Vendedor</th>
            <th>Vendas</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="vendedor in vendedoresTele"
            :key="vendedor.nome"
            @click="$emit('selecionar-vendedor', vendedor)"
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
         <option value="porta">Somente Porta a Porta</option>
         <option value="externa">Somente Vendas Externas</option>
        </select>
      </div>

    <div v-if="vendedoresPorta.length > 0" class="table-container">
      <table class="dashboard-table">
        <thead>
          <tr>
            <th>Nome do Vendedor</th>
            <th>Vendas</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="vendedor in vendedoresPorta"
            :key="vendedor.nome"
            @click="$emit('selecionar-vendedor', vendedor)"
            class="clickable-row"
          >
            <td class="vendedor-name">{{ vendedor.nome }}</td>
            <td>{{ vendedor.total_vendas }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else class="no-data-message">Nenhum vendedor porta a porta encontrado para a categoria selecionada.</div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  vendedoresTele: Array,
  vendedoresPorta: Array,
  filtroCategoria: String
})

const emit = defineEmits(['selecionar-vendedor', 'update-filtro'])
</script>

<style scoped>
.dashboard-card {
  background: #ffffff;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  color: #333;
  margin-top: 24px; /* Espaçamento entre os cards */
}

.dashboard-title {
  font-size: 1.5rem; /* 24px */
  font-weight: 600;
  margin-bottom: 16px;
  text-align: center;
  color: #1f2937;
}

.table-container {
  overflow-x: auto; /* Para tabelas que podem ser largas em telas pequenas */
}

.dashboard-table {
  width: 100%;
  border-collapse: collapse;
}

.dashboard-table th,
.dashboard-table td {
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}

.dashboard-table th {
  background-color: #f9fafb;
  font-size: 0.75rem; /* 12px */
  font-weight: 500;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.clickable-row {
  cursor: pointer;
  transition: background-color 0.15s ease;
}

.clickable-row:hover {
  background-color: #f3f4f6; /* Um cinza muito claro para o hover */
}

.vendedor-name {
  font-weight: 500; /* Levemente mais negrito */
  transition: color 0.15s ease;
}

.clickable-row:hover .vendedor-name {
  color: #2563eb; /* Cor azul no hover para indicar clique */
}

.no-data-message {
  text-align: center;
  color: #6b7280;
  padding: 16px;
}

.filter-controls {
  margin-bottom: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

@media (min-width: 640px) {
  .filter-controls {
    flex-direction: row;
    justify-content: center;
  }
}

.filter-label {
  font-size: 0.875rem; /* 14px */
  font-weight: 500;
  color: #4b5563;
}

.filter-select {
  display: block;
  width: 100%;
  max-width: 200px; /* Limita a largura do select */
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  background-color: #ffffff;
  border-radius: 6px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  font-size: 0.875rem; /* 14px */
  color: #374151;
  -webkit-appearance: none; /* Remove o estilo padrão do navegador no Chrome/Safari */
  -moz-appearance: none;    /* Remove o estilo padrão do navegador no Firefox */
  appearance: none;         /* Remove o estilo padrão do navegador */
  background-image: url('data:image/svg+xml;charset=UTF-8,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2020%2020%22%20fill%3D%22none%22%20stroke%3D%22currentColor%22%20stroke-width%3D%221.5%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%3E%3Cpath%20d%3D%22M6%209l6%206%206-6%22%2F%3E%3C%2Fsvg%3E'); /* Ícone de seta para baixo */
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
  background-size: 0.8em;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

.filter-select:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.25);
}
</style>