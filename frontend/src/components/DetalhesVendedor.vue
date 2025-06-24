<template>
  <div class="detalhes-vendedor-card">
    <h3 class="detalhes-vendedor-title">Detalhes de {{ vendedor.nome }}</h3>

    <div v-if="vendedor.carregando" class="detalhes-vendedor-loading">Carregando...</div>
    <div v-else-if="vendedor.clientes.length">
      <div class="detalhes-vendedor-table-wrapper">
        <table class="detalhes-vendedor-table">
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
    </div>
    <div v-else class="detalhes-vendedor-no-data">Nenhum cliente encontrado para este vendedor.</div>
  </div>
</template>

<script setup>
defineProps(['vendedor'])
</script>

<style scoped>
.detalhes-vendedor-card {
  background: #ffffff;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  color: #333;
  margin-top: 30px; /* Mantém um espaçamento superior se não estiver em um grid */
}

.detalhes-vendedor-title {
  font-size: 1.25rem; /* 20px */
  font-weight: 600;
  margin-bottom: 16px;
  text-align: center;
  color: #1f2937;
}

.detalhes-vendedor-loading,
.detalhes-vendedor-no-data {
  text-align: center;
  color: #6b7280;
  padding: 16px;
}

.detalhes-vendedor-table-wrapper {
  overflow-x: auto; /* Para tabelas que podem ser largas em telas pequenas */
}

.detalhes-vendedor-table {
  width: 100%;
  border-collapse: collapse;
}

.detalhes-vendedor-table th,
.detalhes-vendedor-table td {
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid #e5e7eb; /* Cor de borda mais suave */
}

.detalhes-vendedor-table th {
  background-color: #f9fafb; /* Fundo leve para cabeçalhos */
  font-size: 0.75rem; /* 12px */
  font-weight: 500;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.detalhes-vendedor-table tbody tr:hover {
  background-color: #f3f4f6; /* Hover mais suave */
}
</style>