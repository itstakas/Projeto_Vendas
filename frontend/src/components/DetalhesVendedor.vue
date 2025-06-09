<template>
  <div v-if="clientes.length">
    <h3>{{ nome }} - {{ clientes.length }} vendas</h3>
    <ul>
      <li v-for="(cliente, index) in clientes" :key="index">
        {{ cliente.NOME }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import axios from 'axios'

const props = defineProps({
  nome: String
})

const clientes = ref([])

watch(() => props.nome, async (novoNome) => {
  if (!novoNome) {
    clientes.value = []
    return
  }

  try {
    const res = await axios.get(`http://127.0.0.1:5000/vendedor_tele/${encodeURIComponent(novoNome)}`)
    clientes.value = res.data
    console.log('Clientes recebidos:', clientes.value)
  } catch (error) {
    console.error('Erro ao buscar clientes do vendedor:', error)
    clientes.value = []
  }
}, { immediate: true })
</script>
