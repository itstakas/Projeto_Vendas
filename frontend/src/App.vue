<template>
  <div class="">
    <!-- Envio de arquivos -->
    <EnviarCsvExcel
      @vendedoresAtualizados="receberDados"
      @arquivoPronto="arquivoGerado = true"
    />

    <!-- Botão de download (usando componente separado) -->
    <BaixarArquivo v-if="arquivoGerado" />

    <div class="container">
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

    async mostrarDetalhes(vendedor) {
      // Mostra o nome e flag de carregamento
      this.vendedorSelecionado = {
        nome: vendedor.nome,
        carregando: true,
        clientes: []
      }

      try {
        const response = await fetch(`http://localhost:5000/vendedor_tele/${encodeURIComponent(vendedor.nome)}`)
        const clientes = await response.json()

        console.log('Clientes retornados da API: ', clientes)

        // this.vendedorSelecionado.clientes = clientes
        this.vendedorSelecionado = {
          nome: vendedor.nome,
          carregando: false,
          clientes: clientes
        }

      } catch (error) {
        console.error('Erro ao buscar detalhes:', error)
        this.vendedorSelecionado.clientes = []
      } finally {
        this.vendedorSelecionado.carregando = false
      }
    }
  }
}
</script>

<style scoped>
.container{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

</style>
