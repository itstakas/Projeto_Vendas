<script setup>
import { ref } from 'vue'
import EnviarCsvExcel from './components/EnviarCsvExcel.vue'
import ListaVendedores from './components/ListaVendedores.vue'
import DetalhesVendedor from './components/DetalhesVendedor.vue'
import BaixarArquivo from './components/BaixarArquivo.vue'

// Estado para lista de vendedores
const vendedores = ref([])
// Estado para o vendedor selecionado
const vendedorSelecionado = ref(null)
// Estado para exibir botão de download
const arquivoPronto = ref(false)

function selecionarVendedor(nome) {
  vendedorSelecionado.value = nome
}

function atualizarVendedores(lista) {
  vendedores.value = lista
}

function marcarArquivoPronto() {
  arquivoPronto.value = true
}
</script>

<template>
  <div style="padding: 20px">
    <!-- Upload de arquivos -->
    <EnviarCsvExcel 
      @vendedoresAtualizados="atualizarVendedores" 
      @arquivoPronto="marcarArquivoPronto"
    />

    <!-- Botão de download -->
    <BaixarArquivo :visivel="arquivoPronto" />

    <!-- Lista de vendedores -->
    <ListaVendedores 
      :vendedores="vendedores" 
      @selecionar-vendedor="selecionarVendedor" 
    />

    <!-- Detalhes do vendedor -->
    <DetalhesVendedor 
      v-if="vendedorSelecionado" 
      :nome="vendedorSelecionado" 
    />
  </div>
</template>
