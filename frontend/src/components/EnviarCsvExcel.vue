
<template>
    <div class="container">
        <h1>Upload de arquivos: </h1>
        <button @click="triggerCsvUpload">Enviar CSV</button>
        <button @click="triggerExcelUpload">Enviar EXCEL</button>
        <p>
            <button type="submit">Enviar</button>
        </p>

    <input 
        type="file"
        ref="csvInput"
        accept=".csv"
        @change="handleCsvFile"
        style="display: none;"
    />

    <input 
        type="file"
        ref="excelInput"
        accept=".xlsx, .xls"
        @change="handleExcelFile"
        style="display: none;"
    />
    </div>
    <EnviarArquivos/>
</template>

<script setup>
import EnviarArquivos from './EnviarArquivos.vue';
import { ref } from 'vue';

const csvInput = ref(null)
const excelInput = ref(null)

const triggerCsvUpload = ()=>{
    csvInput.value.click(); 
}

const triggerExcelUpload = ()=>{
    excelInput.value.click();
}

const handleCsvFile = (event)=>{
    const file = event.target.files[0];
}

const handleExcelFile = (event)=>{
    const file = event.target.file[0]
}

</script>