<template>
  <div class="bg-white p-4 rounded shadow-md">
    <h2 class="text-xl font-semibold mb-4">Vendedores e Vendas</h2>
    <table class="w-full table-auto border">
      <thead class="bg-gray-200">
        <tr>
          <th class="px-4 py-2 border">Nome do Vendedor</th>
          <th class="px-4 py-2 border">Quantidade de Vendas</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="vendedor in vendedores"
          :key="vendedor.nome"
          @click="$emit('selecionar-vendedor', vendedor)"
          class="cursor-pointer hover:bg-gray-100"
        >
          <td class="px-4 py-2 border text-blue-600 hover:underline">{{ vendedor.nome }}</td>
          <td class="px-4 py-2 border text-center">{{ vendedor.total_vendas }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
defineProps(['vendedores'])
</script>
