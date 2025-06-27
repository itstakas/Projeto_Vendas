<script setup>
import { ref, computed } from 'vue'

import './assets/style.css'
import EnviarCsvExcel from './components/EnviarCsvExcel.vue'
import ListaVendedores from './components/ListaVendedores.vue'
import DetalhesVendedor from './components/DetalhesVendedor.vue'
import BaixarArquivo from './components/BaixarArquivo.vue'

// Estado reativo para armazenar os dados dos vendedores
const vendedoresTele = ref([])
const vendedoresPorta = ref([])
const vendedorSelecionado = ref(null)
const arquivoGerado = ref(false)
const filtroCategoria = ref("todos")

// Computed para aplicar filtro na lista de vendedores Porta a Porta
const vendedoresPortaFiltrados = computed(() => {
  if (filtroCategoria.value === 'todos') {
    return vendedoresPorta.value
  }
  return vendedoresPorta.value.filter(v => v.tipo_vendedor === filtroCategoria.value)
})

// Função chamada ao receber dados de Telemarketing
function receberTele(dados) {
  vendedoresTele.value = dados
}

// Função chamada ao receber dados de Porta a Porta
function receberPorta(dados) {
  vendedoresPorta.value = dados
}

// Função para buscar os detalhes de um vendedor ao ser clicado na lista
async function mostrarDetalhes(vendedor, tipo) {
  // Inicia o carregamento e limpa clientes anteriores
  vendedorSelecionado.value = {
    nome: vendedor.nome,
    carregando: true,
    clientes: []
  }

  // Define o endpoint da API conforme o tipo de vendedor
  let endpoint = ''
  if (tipo === 'tele') {
    endpoint = `/vendedor_tele/${encodeURIComponent(vendedor.nome)}`
  } else {
    endpoint = `/vendedores_porta_a_porta/${encodeURIComponent(vendedor.nome)}`
  }

  // CORREÇÃO 2: Usando http em vez de https
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
      <!-- Componente de upload de arquivos CSV e Excel -->
      <EnviarCsvExcel
        @vendedoresTele="receberTele"
        @vendedoresPorta="receberPorta"
        @arquivoPronto="arquivoGerado = true"
      />

      <!-- Botão de download visível apenas após processamento -->
      <BaixarArquivo v-if="arquivoGerado" class="download-section" />

      <!-- Área com as tabelas de vendedores e detalhes -->
      <div class="data-display-area">
        <!-- Tabelas de vendedores -->
        <div class="lista-vendedores-wrapper">
          <!-- CORREÇÃO 1: A forma correta de ouvir o evento com os dois parâmetros -->
          <ListaVendedores
            v-if="vendedoresTele.length || vendedoresPorta.length"
            :vendedoresTele="vendedoresTele"
            :vendedoresPorta="vendedoresPortaFiltrados"
            :filtroCategoria="filtroCategoria"
            @update-filtro="filtroCategoria = $event"
            @selecionar-vendedor="mostrarDetalhes"
          />
        </div>

        <!-- Tabela com os detalhes do vendedor clicado -->
        <div class="detalhes-section" v-if="vendedorSelecionado">
          <DetalhesVendedor :vendedor="vendedorSelecionado" />
        </div>
      </div>
    </div>
  </main>
</template>

<style>
/* Estilos da área principal da aplicação */
.app-main {
  min-height: 100vh;
  padding: 2rem 1rem;
  background-color: #f2f4f7;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

/* Wrapper principal com limite de largura */
.app-container-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 1200px;
  width: 100%;
  padding: 0 1rem;
}

/* Seção do botão de download */
.download-section {
  margin-top: 2rem;
}

/* Área onde ficam as listas e os detalhes */
.data-display-area {
  display: flex;
  flex-direction: column;
  gap: 24px;
  width: 100%;
  margin-top: 2rem;
}

/* Wrapper que garante largura total das tabelas de vendedores */
.lista-vendedores-wrapper {
  width: 100%;
}

/* Detalhes de vendedor ocupa 100% abaixo das listas */
.detalhes-section {
  width: 100%;
}
</style>
