<script setup>
import { ref } from 'vue'
import EnviarCsvExcel from './components/EnviarCsvExcel.vue'
import ListaVendedores from './components/ListaVendedores.vue'
import DetalhesVendedor from './components/DetalhesVendedor.vue'
import BaixarArquivo from './components/BaixarArquivo.vue'

const vendedoresTele = ref([])
const vendedoresPorta = ref([])
const vendedorSelecionado = ref(null)
const arquivoGerado = ref(false)

function receberTele(dados) {
  vendedoresTele.value = dados
}
function receberPorta(dados) {
  vendedoresPorta.value = dados
}

async function mostrarDetalhes(vendedor) {
  vendedorSelecionado.value = {
    nome: vendedor.nome,
    carregando: true,
    clientes: []
  }

  try {
    const response = await fetch(`http://localhost:5000/vendedor_tele/${encodeURIComponent(vendedor.nome)}`)
    const clientes = await response.json()

    vendedorSelecionado.value = {
      nome: vendedor.nome,
      carregando: false,
      clientes: clientes
    }
  } catch (error) {
    console.error('Erro ao buscar detalhes:', error)
    vendedorSelecionado.value.clientes = []
  } finally {
    vendedorSelecionado.value.carregando = false
  }
}
</script>

<template>
  <div>
    <EnviarCsvExcel
      @vendedoresTele="receberTele"
      @vendedoresPorta="receberPorta"
      @arquivoPronto="arquivoGerado = true"
    />

    <BaixarArquivo v-if="arquivoGerado" />

    <div class="container">
      <ListaVendedores
        v-if="vendedoresTele.length || vendedoresPorta.length"
        :vendedoresTele="vendedoresTele"
        :vendedoresPorta="vendedoresPorta"
        @selecionar-vendedor="mostrarDetalhes"
      />

      <DetalhesVendedor
        v-if="vendedorSelecionado"
        :vendedor="vendedorSelecionado"
      />
    </div>
  </div>
</template>

<style scoped>
.container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}
</style>
