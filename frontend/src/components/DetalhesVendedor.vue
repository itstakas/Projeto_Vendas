<template>
  <div class="detalhes-vendedor">
    <h3>Detalhes de {{ vendedor.nome }}</h3>

    <div v-if="vendedor.carregando">Carregando...</div>
    <div v-else-if="vendedor.clientes.length">
      <table>
        <thead>
          <tr>
            <th>Nome do Cliente</th>
            <th>Data do Contrato</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(cliente, index) in vendedor.clientes" :key="index">
            <td>{{ cliente.NOME }}</td>
            <td>{{ cliente.DATA_CONTRATO }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else>Nenhum cliente encontrado.</div>
  </div>
</template>

<script setup>
defineProps(['vendedor'])
</script>

<style scoped>
.detalhes-vendedor {
  margin-top: 30px;
  background: #1f1f1f;
  padding: 20px;
  border-radius: 10px;
  color: #ffffff;
}

.detalhes-vendedor table {
  width: 100%;
  border-collapse: collapse;
}

.detalhes-vendedor th,
.detalhes-vendedor td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid #444;
}

.detalhes-vendedor tr:hover {
  background-color: #2a2a2a;
}
</style>
