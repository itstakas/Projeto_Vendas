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
    <table>
      <thead>
        <tr>
          <th>Nome do Vendedor</th>
          <th>Quantidade de Vendas</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="vendedor in VendedoresPorta"
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
defineProps(['vendedoresTele', 'VendedoresPorta'])
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
