<template>
  <div class="dashboard-container">
    <EnviarCsvExcel 
      @arquivoProcessado="buscarVendedores"
    />

    <div class="painel-container">
      <!-- Painel Tele -->
      <PainelVendedores 
        titulo="Vendedores Tele"
        :vendedores="vendedores.tele"
        @selecionar="mostrarDetalhes"
      />

      <!-- Painel Porta a Porta -->
      <PainelVendedores 
        titulo="Vendedores Porta a Porta"
        :vendedores="vendedores.porta"
        @selecionar="mostrarDetalhes"
      />
    </div>

    <DetalhesVendedor 
      v-if="vendedorSelecionado"
      :vendedor="vendedorSelecionado"
    />
  </div>
</template>

<script>
import { ref } from 'vue';
import EnviarCsvExcel from './components/EnviarCsvExcel.vue';
import PainelVendedores from './components/PainelVendedores.vue';
import DetalhesVendedor from './components/DetalhesVendedor.vue';

export default {
  components: {
    EnviarCsvExcel,
    PainelVendedores,
    DetalhesVendedor
  },
  setup() {
    const vendedores = ref({ tele: [], porta: [] });
    const vendedorSelecionado = ref(null);

    const buscarVendedores = async () => {
      try {
        const response = await fetch('http://localhost:5000/todos_vendedores');
        const data = await response.json();
        vendedores.value = data;
      } catch (error) {
        console.error('Erro ao buscar vendedores:', error);
      }
    };

    const mostrarDetalhes = async (vendedor) => {
      vendedorSelecionado.value = { ...vendedor, carregando: true };
      
      try {
        const response = await fetch(
          `http://localhost:5000${vendedor.link_detalhes}`
        );
        const clientes = await response.json();
        
        vendedorSelecionado.value = {
          ...vendedor,
          clientes,
          carregando: false
        };
      } catch (error) {
        console.error('Erro nos detalhes:', error);
        vendedorSelecionado.value.carregando = false;
      }
    };

    return { vendedores, vendedorSelecionado, buscarVendedores, mostrarDetalhes };
  }
};
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.painel-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-top: 20px;
}
</style>