<script setup>
import { ref, computed } from 'vue'
import './assets/style.css' // Importa o CSS principal
import EnviarCsvExcel from './components/EnviarCsvExcel.vue'
import ListaVendedores from './components/ListaVendedores.vue'
import DetalhesVendedor from './components/DetalhesVendedor.vue'
import BaixarArquivo from './components/BaixarArquivo.vue'

const vendedoresTele = ref([])
const vendedoresPorta = ref([])
const vendedorSelecionado = ref(null)
const arquivoGerado = ref(false)
const filtroCategoria = ref("todos") // 'todos' | 'porta' | 'externa' -são as opções de filtro

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

// Estes arrays poderiam vir de uma API no futuro para maior flexibilidade
const nomesPortaPorta = [
  "GLEICI IDALINA PEREIRA RUIZ",
  "VEND.SILAS DE OLIVEIRA",
  "MARIA ROSELI",
  "ANA BEATRIZ DO PRADO SCAVONE",
  "ELIZABETE ALVES",
  "TALITA JUNIA DA CONCEICAO SILVA"
]

const nomesExterna = [
  "ANDRE MENOSSI",
  "MARIO ANTONIO DELGADO MOREL",
  "NATANAEL DE SOUZA BRASIL",
  "ANA GRACIELA BENITEZ",
  "DIANA ELIZABETH FERREIRA PALACIOS",
  "DEMETRIO FIDEL INSFRAN BALBUENA"
]

const vendedoresPortaFiltrados = computed(() => {
  if (filtroCategoria.value === 'porta') {
    return vendedoresPorta.value.filter(v => nomesPortaPorta.includes(v.nome))
  } else if (filtroCategoria.value === 'externa'){
    return vendedoresPorta.value.filter(v => nomesExterna.includes(v.nome))
  } else {
    return vendedoresPorta.value // todos
  }
})
</script>

<template>
  <main class="app-main">
    <div class="app-container-wrapper">
      <EnviarCsvExcel
        @vendedoresTele="receberTele"
        @vendedoresPorta="receberPorta"
        @arquivoPronto="arquivoGerado = true"
      />

      <BaixarArquivo v-if="arquivoGerado" class="download-section" />

      <div class="data-display-area">
        <ListaVendedores
          v-if="vendedoresTele.length || vendedoresPortaFiltrados.length"
          :vendedoresTele="vendedoresTele"
          :vendedoresPorta="vendedoresPortaFiltrados"
          :filtroCategoria="filtroCategoria"
          @update-filtro="filtroCategoria = $event"
          @selecionar-vendedor="mostrarDetalhes"
        />

        <DetalhesVendedor
          v-if="vendedorSelecionado"
          :vendedor="vendedorSelecionado"
        />
      </div>
    </div>
  </main>
</template>

<style>
/* Estilos globais (não scoped) ou de layout principal */
.app-main {
  min-height: 100vh;
  padding: 2rem 1rem;
  background-color: #f2f4f7;
  display: flex;
  justify-content: center; /* Centraliza horizontalmente */
  align-items: flex-start; /* Alinha ao topo verticalmente */
}

.app-container-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 1200px; /* Limita a largura máxima do conteúdo */
  width: 100%;
  padding: 0 1rem; /* Padding horizontal para telas menores */
}

.download-section {
  margin-top: 2rem;
}

.data-display-area {
  display: grid;
  grid-template-columns: 1fr;
  gap: 24px;
  width: 100%;
  margin-top: 2rem;
}

@media (min-width: 768px) {
  .data-display-area {
    grid-template-columns: 1fr 1fr;
  }
}
</style>