<template>
  <div class="enviar-arquivos-card">
    <h1 class="enviar-arquivos-title">Processar Dados de Vendas</h1>

    <div class="enviar-arquivos-buttons">
      <button
        class="upload-button blue-button"
        @click="triggerCsvInput"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="button-icon">
          <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25M9 16.5v.75m3-3v3M15 12v5.25m-4.5-15H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
        </svg>
        CSV
      </button>
      <input
        type="file"
        ref="csvInput"
        @change="onCsvSelected"
        accept=".csv"
        class="hidden-input"
      />

      <button
        class="upload-button green-button"
        @click="triggerExcelInput"
      >
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="button-icon">
        <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25M9 16.5v.75m3-3v3M15 12v5.25m-4.5-15H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
      </svg>
        Excel
      </button>
      <input
        type="file"
        ref="excelInput"
        @change="onExcelSelected"
        accept=".xlsx,.xls"
        class="hidden-input"
      />
    </div>

    <div class="selected-files-info">
      <p v-if="arquivoCsv">CSV Selecionado: <span class="file-name">{{ arquivoCsv.name }}</span></p>
      <p v-else class="file-status-none">Nenhum CSV selecionado</p>
      <p v-if="arquivoExcel">Excel Selecionado: <span class="file-name">{{ arquivoExcel.name }}</span></p>
      <p v-else class="file-status-none">Nenhum Excel selecionado</p>
    </div>

    <button
      v-if="arquivoCsv && arquivoExcel"
      class="process-button"
      @click="enviarArquivos"
      :disabled="enviando"
    >
      <span v-if="enviando" class="loader"></span>
      {{ enviando ? 'Enviando...' : 'Processar Arquivos' }}
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
    const response = await axios.post('/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    const vendedoresResTele = await axios.get('/vendedores_tele')
    emit('vendedoresTele', vendedoresResTele.data)

    const vendedoresResPorta = await axios.get('/vendedores_porta_a_porta')
    emit('vendedoresPorta', vendedoresResPorta.data)

    emit('arquivoPronto', true)
    alert('Arquivos processados com sucesso!')
  } catch (error) {
    console.error('Erro ao enviar arquivos:', error)
    alert('Erro ao processar arquivos: ' + (error.response?.data?.error || error.message))
  } finally {
    enviando.value = false
  }
}
</script>

<style scoped>
.enviar-arquivos-card {
  background-color: #ffffff;
  padding: 32px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 480px; /* Para controlar a largura máxima */
}

.enviar-arquivos-title {
  font-size: 1.875rem; /* 30px */
  font-weight: 700;
  margin-bottom: 32px;
  color: #1f2937;
  text-align: center;
}

.enviar-arquivos-buttons {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 24px;
  margin-bottom: 24px;
  width: 100%;
}

.upload-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 24px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  font-size: 1rem; /* 16px */
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease, transform 0.1s ease;
  width: 160px; /* Largura fixa para os botões */
  border: none;
}

.upload-button.blue-button {
  background-color: #3b82f6; /* Cor azul */
  color: white;
}

.upload-button.blue-button:hover {
  background-color: #2563eb;
  transform: translateY(-1px);
}

.upload-button.green-button {
  background-color: #10b981; /* Cor verde */
  color: white;
}

.upload-button.green-button:hover {
  background-color: #059669;
  transform: translateY(-1px);
}

.button-icon {
  width: 30px;
  height: 30px;
}

.hidden-input {
  display: none;
}

.selected-files-info {
  margin-bottom: 24px;
  font-size: 0.875rem; /* 14px */
  color: #6b7280;
  text-align: center;
  width: 100%;
}

.selected-files-info p {
  margin-bottom: 4px;
}

.file-name {
  font-weight: 500;
  color: #1f2937;
  word-break: break-all; /* Quebra palavras longas */
}

.file-status-none {
  color: #ef4444; /* Cor vermelha para "Nenhum selecionado" */
}

.process-button {
  width: 100%;
  max-width: 280px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 16px 24px;
  background-color: #8b5cf6; /* Cor roxa */
  color: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  font-size: 1.125rem; /* 18px */
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease, transform 0.1s ease;
  border: none;
}

.process-button:hover {
  background-color: #7c3aed;
  transform: translateY(-1px);
}

.process-button:disabled {
  background-color: #d1d5db;
  cursor: not-allowed;
  opacity: 0.7;
}

.loader {
  border: 3px solid #f3f3f3;
  border-top: 3px solid #ffffff;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  animation: spin 0.8s linear infinite;
  display: inline-block;
  vertical-align: middle;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>