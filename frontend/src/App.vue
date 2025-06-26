<script setup>
import { ref, computed } from 'vue'
import './assets/style.css'
import EnviarCsvExcel from './components/EnviarCsvExcel.vue'
import ListaVendedores from './components/ListaVendedores.vue'
import DetalhesVendedor from './components/DetalhesVendedor.vue'
import BaixarArquivo from './components/BaixarArquivo.vue'

const vendedoresTele = ref([])
const vendedoresPorta = ref([])
const vendedorSelecionado = ref(null)
const arquivoGerado = ref(false)
const filtroCategoria = ref("todos")

const vendedoresPortaFiltrados = computed(() => {
  if (filtroCategoria.value === 'todos') {
    return vendedoresPorta.value
  }
  return vendedoresPorta.value.filter(v => v.tipo_vendedor === filtroCategoria.value)
})

function receberTele(dados) {
  vendedoresTele.value = dados
}

function receberPorta(dados) {
  vendedoresPorta.value = dados
}

async function mostrarDetalhes(vendedor, tipo) {
  vendedorSelecionado.value = {
    nome: vendedor.nome,
    carregando: true,
    clientes: []
  }

  let endpoint = ''
  if (tipo === 'tele') {
    endpoint = `/vendedor_tele/${encodeURIComponent(vendedor.nome)}`
  } else {
    endpoint = `/vendedores_porta_a_porta/${encodeURIComponent(vendedor.nome)}`
  }
  const url = `http://localhost:5000${endpoint}`

  try {
    const response = await fetch(url)
    const clientes = await response.json()
    vendedorSelecionado.value = {
      nome: vendedor.nome,
      carregando: false,
      clientes: clientes
    }
  } catch (error) {
    console.error('Erro ao buscar detalhes:', error)
  } finally {
    vendedorSelecionado.value.carregando = false
  }
}
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
        <div class="vendedores-section">
          <ListaVendedores
            v-if="vendedoresTele.length || vendedoresPorta.length"
            :vendedoresTele="vendedoresTele"
            :vendedoresPorta="vendedoresPortaFiltrados"
            :filtroCategoria="filtroCategoria"
            @update-filtro="filtroCategoria = $event"
            @selecionar-vendedor="mostrarDetalhes"
          />
        </div>

        <div class="detalhes-section" v-if="vendedorSelecionado">
          <DetalhesVendedor :vendedor="vendedorSelecionado" />
        </div>
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
  display: flex;
  flex-direction: column;
  gap: 24px;
  width: 100%;
  margin-top: 2rem;
}

.vendedores-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.detalhes-section {
  width: 100%;
}

</style>