<template>
  <div class="p-6 space-y-6">
    <!-- Envio de arquivos -->
    <EnviarCsvExcel
      @vendedoresAtualizados="receberDados"
      @arquivoPronto="arquivoGerado = true"
    />

    <!-- Botão de download (usando componente separado) -->
    <BaixarArquivo v-if="arquivoGerado" />

    <!-- Lista de vendedores -->
    <ListaVendedores
      v-if="vendedores.length"
      :vendedores="vendedores"
      @selecionar-vendedor="mostrarDetalhes"
    />

    <!-- Detalhes do vendedor -->
    <DetalhesVendedor
      v-if="vendedorSelecionado"
      :vendedor="vendedorSelecionado"
    />
  </div>
</template>

<script>
import EnviarCsvExcel from './components/EnviarCsvExcel.vue'
import ListaVendedores from './components/ListaVendedores.vue'
import DetalhesVendedor from './components/DetalhesVendedor.vue'
import BaixarArquivo from './components/BaixarArquivo.vue'

export default {
  components: {
    EnviarCsvExcel,
    ListaVendedores,
    DetalhesVendedor,
    BaixarArquivo
  },
  data() {
    return {
      vendedores: [],
      vendedorSelecionado: null,
      arquivoGerado: false
    }
  },
  methods: {
    receberDados(dados) {
      this.vendedores = dados
      this.vendedorSelecionado = null
    },
    mostrarDetalhes(vendedor) {
      this.vendedorSelecionado = vendedor
    }
  }
}
</script>
