<template>
  <div class="bg-white p-4 rounded shadow-md">
    <h3 class="text-lg font-semibold mb-2">
      Detalhes de {{ vendedor.nome }}
    </h3>

    <div v-if="vendedor.carregando">Carregando detalhes...</div>
    <div v-else-if="vendedor.clientes.length">
      <table class="min-w-full border">
        <thead class="bg-gray-200">
          <tr>
            <th class="px-4 py-2 border">Nome do Cliente</th>
            <th class="px-4 py-2 border">Data do Contrato</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(cliente, index) in vendedor.clientes" :key="index">
            <td class="px-4 py-2 border">{{ cliente.NOME }}</td>
            <td class="px-4 py-2 border">{{ cliente.DATA_CONTRATO }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else>
      Nenhum cliente encontrado.
    </div>
  </div>
</template>

<script setup>
defineProps(['vendedor'])
</script>
