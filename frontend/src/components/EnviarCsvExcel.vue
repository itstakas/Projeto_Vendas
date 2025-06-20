<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-900 text-white">
    <div class="p-6 bg-gray-800 rounded-xl shadow-lg w-full max-w-md">
      <h1 class="text-2xl font-semibold mb-6 text-center">Upload de Arquivos</h1>

      <div class="space-y-6">
        <!-- Botão CSV -->
        <div class="text-center">
          <button
            class="w-full bg-gray-200 hover:bg-gray-300 text-black font-semibold py-2 px-4 rounded"
            @click="triggerCsvInput"
          >
            Selecionar arquivo CSV
          </button>
          <input
            type="file"
            ref="csvInput"
            @change="onCsvSelected"
            accept=".csv"
            class="hidden"
            style="display: none;"
          />
          <p v-if="arquivoCsv" class="text-sm text-gray-300 mt-2">{{ arquivoCsv.name }}</p>
        </div>

        <!-- Botão Excel -->
        <div class="text-center">
          <button
            class="w-full bg-gray-200 hover:bg-gray-300 text-black font-semibold py-2 px-4 rounded"
            @click="triggerExcelInput"
          >
            Selecionar arquivo Excel
          </button>
          <input
            type="file"
            ref="excelInput"
            @change="onExcelSelected"
            accept=".xlsx,.xls"
            class="hidden"
            style="display: none;"
          />
          <p v-if="arquivoExcel" class="text-sm text-gray-300 mt-2">{{ arquivoExcel.name }}</p>
        </div>

        <!-- Botão Enviar -->
        <div class="text-center">
          <button
            class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded disabled:opacity-50"
            @click="enviarArquivos"
            :disabled="!arquivoCsv || !arquivoExcel || enviando"
          >
            <span v-if="enviando" class="loader mr-2"></span>
            {{ enviando ? 'Enviando...' : 'Enviar arquivos' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref } from 'vue'
import axios from 'axios'

// Refs para arquivos
const arquivoCsv = ref(null)
const arquivoExcel = ref(null)
const enviando = ref(false)

// Refs para inputs
const csvInput = ref(null)
const excelInput = ref(null)

// Emissor de eventos
const emit = defineEmits(['arquivoPronto', 'vendedoresTele', 'vendedoresPorta'])

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
  if (!arquivoCsv.value || !arquivoExcel.value) {
    alert('Envie ambos os arquivos antes de enviar.')
    return
  }

  enviando.value = true

  const formData = new FormData()
  formData.append('csv', arquivoCsv.value)
  formData.append('excel', arquivoExcel.value)

  try {
    // Envia arquivos para o backend
    const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    emit('respostaRecebida', response.data)

    // Busca os dados de vendedores processados
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
