<template>
  <div class="bg-white p-4 rounded shadow-md">
    <h3 class="text-lg font-semibold mb-2">
      Vendas de {{ vendedor.nome }}
    </h3>
    <ul class="list-disc list-inside text-gray-700">
      <li v-for="cliente in vendedor.clientes" :key="cliente">
        {{ cliente }}
      </li>
    </ul>
  </div>
</template>

<script setup>
defineProps(['vendedor'])
</script>
