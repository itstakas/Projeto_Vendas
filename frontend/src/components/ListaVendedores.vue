<template>
  <div>
    <h2>Vendedores TELE</h2>
    <div>
      <button
        v-for="v in vendedores"
        :key="v.nome"
        @click="selecionar(v.nome)"
        style="margin: 4px; padding: 8px 12px; font-weight: bold;"
      >
        {{ v.nome }} - {{ v.total_vendas }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const vendedores = ref([])

onMounted(async () => {
  try {
    const res = await axios.get('http://127.0.0.1:5000/vendedores_tele')

    console.log('Vendedores recebidos:', res.data)

    vendedores.value = res.data
  } catch (error) {
    console.error('Erro ao buscar vendedores:', error)
  }
})

const emit = defineEmits(['selecionar-vendedor'])
const selecionar = (nome) => emit('selecionar-vendedor', nome)
</script>
