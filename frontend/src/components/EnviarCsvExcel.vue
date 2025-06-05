
<template>
    <div class="container">
        <h1>Upload de arquivos: </h1>

        <input type="file" ref="csvInput" accept=".csv" style="display: none;" @change="selecionarCsv"/>
        <input type="file" ref="excelInput" accept=".xlsx, .xls" style="display: none;" @change="selecionarExcel"/>
    
        <button @click="abrirCsv">Enviar CSV</button>
        <button @click="abrirExcel">Enviar EXCEL</button>

        <!-- <div>
        <button
        v-on:click="enviarArquivos"
        v-bind="!arquivoCsv || !arquivoExcel || carregando"
    >
        {{ carregando ? 'Enviando...' : 'Enviar arquivos' }}
    </button>
        -->
        

    <input 
        type="file"
        ref="csvInput"
        accept=".csv"
        @change="selecionarCsv"
        style="display: none;"
    />

    <input 
        type="file"
        ref="excelInput"
        accept=".xlsx, .xls"
        @change="selecionarExcel"
        style="display: none;"
    />
    </div>
    <EnviarArquivos
        :arquivoCsv="arquivoCsv"
        :arquivoExcel="arquivoExcel"
        @respostaRecebida="resposta = $event"
        @arquivoPronto="mostrarBotaoDownload = $event"
    />

    <BaixarArquivo :visivel="mostrarBotaoDownload"/>


    <div v-if="resposta">
        <h2>Resposta do servidor:</h2>
        <pre>{{ resposta }}</pre>
    </div>
    
</template>

<script setup>
import BaixarArquivo from './BaixarArquivo.vue';
import EnviarArquivos from './EnviarArquivos.vue';
import { ref } from 'vue';

const mostrarBotaoDownload = ref(false)

const csvInput = ref(null)
const excelInput = ref(null)

const arquivoCsv = ref(null)
const arquivoExcel = ref(null)

const resposta = ref(null)

const abrirCsv = () => csvInput.value.click()
const abrirExcel = () => excelInput.value.click()

const selecionarCsv = (event) => {
    const file = event.target.files[0]
    if (file && file.name.endsWith('.csv')){
        arquivoCsv.value = file
    } else {
        alert('Arquivo CSV invalido')
        arquivoCsv.value = null
    }
}

const selecionarExcel = (event) => {
    const file = event.target.files[0]
    if(file && /\.(xls|xlsx)$/i.test(file.name)) {
        arquivoExcel.value = file
    } else {
        alert('Arquivo Excel inválido')
        arquivoExcel.value = null
    }
}

</script>

<style scoped>
.progress-bar {
  height: 20px;
  width: 100%;
  background: linear-gradient(90deg, #3498db 0%, #85c1e9 50%, #3498db 100%);
  background-size: 200% 100%;
  animation: carregando 1s linear infinite;
  border-radius: 4px;
  margin-bottom: 15px; 
}

@keyframes carregando {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

</style>