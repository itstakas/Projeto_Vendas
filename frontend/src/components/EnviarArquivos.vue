<template>
    <button
        v-on:click="enviarArquivos"
        :disabled="!arquivoCsv || !arquivoExcel || carregando"
    >
        <span v-if="carregando" class="loader"></span>
       <!-- // <span v-if="carregando" classe="progress-bar"></span> -->
        {{ carregando ? 'Enviando...' : 'Enviar arquivos' }}
    </button>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue';

const props = defineProps({
    arquivoCsv: File,
    arquivoExcel: File,
})

const emit = defineEmits(['respostaRecebida', 'arquivoPronto'])

const carregando = ref(false)
const resposta = ref(null)

const enviarArquivos = async()=>{
    carregando.value = true
    resposta.value = null

    try{
            
        const formData = new FormData()

        if(props.arquivoCsv){
            formData.append('csv', props.arquivoCsv)
        }
        if(props.arquivoExcel){
            formData.append('excel', props.arquivoExcel)
        }

        const response = await axios.post(
            'http://127.0.0.1:5000/upload',
            formData, 
            // {
            //     headers: {
            //         'Content-Type': 'multipart/form-data'
            //     }
            // }
        )
        resposta.value = response.data
        console.log('Resposta do back: ', resposta.value)

        emit('respostaRecebida', resposta.data)
        emit('arquivoPronto', true)
    } catch(error) {
        console.error('Erro no envio: ', error)
        resposta.value = error?.response?.data || 'Erro desconhecido'
    } finally {
        carregando.value = false
    }

}

</script>

<style scoped>
button{
    position: relative;
    padding: 0.5rem 1rem;
    font-weight: bold;
}
.loader{
    border: 2px solid #f3f3f3;
    border-top: 2px solid #3498db;
    border-radius: 50%;
    width: 16px;
    height: 16px;
    animation: spin 1s linear infinite;
    display: inline-block;
    margin-right: 8px;
    vertical-align: middle;
}

@keyframes spin{
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

</style>