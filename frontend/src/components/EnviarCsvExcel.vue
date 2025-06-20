<template>
  <div class="min-h-screen bg-white text-black flex flex-col items-center justify-center px-4 py-10">
    <h1 class="text-4xl font-bold mb-10">Enviar Arquivos</h1>

    <!-- Botões de arquivos -->
    <div class="flex flex-wrap justify-center gap-6 mb-8">
      <button
        class="flex items-center justify-center gap-2 px-8 py-4 bg-gray-100 hover:bg-gray-200 text-black rounded-xl shadow-md text-lg"
        @click="triggerCsvInput"
      >
        CSV
      </button>
      <input
        type="file"
        ref="csvInput"
        @change="onCsvSelected"
        accept=".csv"
        class="hidden"
      />

      <button
        class="flex items-center justify-center gap-2 px-8 py-4 bg-gray-100 hover:bg-gray-200 text-black rounded-xl shadow-md text-lg"
        @click="triggerExcelInput"
      >
        Excel
      </button>
      <input
        type="file"
        ref="excelInput"
        @change="onExcelSelected"
        accept=".xlsx,.xls"
        class="hidden"
      />
    </div>

    <!-- Nomes dos arquivos -->
    <div class="mb-6 text-sm text-gray-600">
      <p v-if="arquivoCsv">CSV Selecionado: {{ arquivoCsv.name }}</p>
      <p v-if="arquivoExcel">Excel Selecionado: {{ arquivoExcel.name }}</p>
    </div>

    <!-- Botão Enviar -->
    <button
      v-if="arquivoCsv && arquivoExcel"
      class="mt-4 px-8 py-4 bg-blue-600 hover:bg-blue-700 text-white rounded-xl shadow-md text-lg"
      @click="enviarArquivos"
      :disabled="enviando"
    >
      <span v-if="enviando" class="loader mr-2"></span>
      {{ enviando ? 'Enviando...' : 'Enviar Arquivos' }}
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const emit = defineEmits(['arquivoPronto', 'vendedoresTele', 'vendedoresPorta'])
const arquivoCsv = ref(null)
const arquivoExcel = ref(null)
const enviando = ref(false)

const csvInput = ref(null)
const excelInput = ref(null)

function triggerCsvInput() {
  csvInput.value.click()
}

function triggerExcelInput() {
  excelInput.value.click()
}

function onCsvSelected(event) {
  arquivoCsv.value = event.target.files[0]
}

function onExcelSelected(event) {
  arquivoExcel.value = event.target.files[0]
}

async function enviarArquivos() {
  enviando.value = true
  const formData = new FormData()
  formData.append('csv', arquivoCsv.value)
  formData.append('excel', arquivoExcel.value)

  try {
    const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    emit('respostaRecebida', response.data)

    const vendedoresRes = await axios.get('http://localhost:5000/vendedores_tele')
    emit('vendedoresTele', vendedoresRes.data)

    const vendedoresPorta = await axios.get('http://localhost:5000/vendedores_porta_a_porta')
    emit('vendedoresPorta', vendedoresPorta.data)

    emit('arquivoPronto', true)
  } catch (error) {
    alert('Erro ao enviar arquivos: ' + error.message)
    emit('respostaRecebida', { error: error.message })
  } finally {
    enviando.value = false
  }
}
</script>

<style scoped>
.loader {
  border: 2px solid #f3f3f3;
  border-top: 2px solid #3498db;
  border-radius: 50%;
  width: 14px;
  height: 14px;
  animation: spin 1s linear infinite;
  display: inline-block;
  vertical-align: middle;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

</style>

