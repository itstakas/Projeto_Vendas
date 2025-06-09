<template>
  <div class="h1">
    <h1>Upload de arquivos</h1>

    <button @click="triggerCsvInput">Selecionar arquivo CSV</button>
    <input
      type="file"
      ref="csvInput"
      @change="onCsvSelected"
      accept=".csv"
      style="display: none"
    />

    <button @click="triggerExcelInput">Selecionar arquivo Excel</button>
    <input
      type="file"
      ref="excelInput"
      @change="onExcelSelected"
      accept=".xlsx,.xls"
      style="display: none"
    />

    <button
      @click="enviarArquivos"
      :disabled="!arquivoCsv || !arquivoExcel || enviando"
    >
      <span v-if="enviando" class="loader"></span>
      {{ enviando ? 'Enviando...' : 'Enviar arquivos' }}
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const arquivoCsv = ref(null)
const arquivoExcel = ref(null)
const enviando = ref(false)

const csvInput = ref(null)
const excelInput = ref(null)

const emit = defineEmits(['respostaRecebida', 'arquivoPronto', 'vendedoresAtualizados'])

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
    const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    emit('respostaRecebida', response.data)

    const vendedoresRes = await axios.get('http://localhost:5000/vendedores_tele')
    emit('vendedoresAtualizados', vendedoresRes.data)

    emit('arquivoPronto', true)
  } catch (error) {
    alert('Erro ao enviar arquivos: ' + error.message)
    emit('respostaRecebida', { error: error.message })
  } finally {
    enviando.value = false
  }
}
</script>
