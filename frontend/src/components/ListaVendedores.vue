<template>
  <div class="dashboard-vendedores">
    <h2>Vendedores Tele</h2>
    <table>
      <thead>
        <tr>
          <th>Nome do Vendedor</th>
          <th>Quantidade de Vendas</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="vendedor in vendedoresTele"
          :key="vendedor.nome"
          @click="$emit('selecionar-vendedor', vendedor)"
        >
          <td>{{ vendedor.nome }}</td>
          <td>{{ vendedor.total_vendas }}</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="dashboard-vendedores">
      <h2>Vendedores Porta a Porta</h2>

      <label for="filtro" style="margin-right: 10px;">Filtrar:</label>
      <select
      id="filtro"
      :value="props.filtroCategoria"
      @change="emit('update-filtro', $event.target.value)"
      style="margin-bottom: 10px; padding: 5px;"
      >
       <option value="todos">Todos</option>
       <option value="porta">Somente Porta a Porta</option>
       <option value="externa">Somente Vendas Externas</option>
      </select>
    <table>
      <thead>
        <tr>
          <th>Nome do Vendedor</th>
          <th>Quantidade de Vendas</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="vendedor in vendedoresPorta"
          :key="vendedor.nome"
          @click="$emit('selecionar-vendedor', vendedor)"
        >
          <td>{{ vendedor.nome }}</td>
          <td>{{ vendedor.total_vendas }}</td>
        </tr>
      </tbody>
    </table>
  </div>


</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  vendedoresTele: Array,
  vendedoresPorta: Array,
  filtroCategoria: String
})

const emit = defineEmits(['selecionar-vendedor', 'upadte-filtro'])
</script>

<style scoped>
.dashboard-vendedores {
  margin-top: 30px;
  background: #1f1f1f;
  padding: 20px;
  border-radius: 10px;
  color: #ffffff;
}

.dashboard-vendedores table {
  width: 100%;
  border-collapse: collapse;
}

.dashboard-vendedores th,
.dashboard-vendedores td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid #444;
}

.dashboard-vendedores tr:hover {
  background-color: #2a2a2a;
  cursor: pointer;
}
</style>
