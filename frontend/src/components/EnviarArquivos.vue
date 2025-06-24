<template>
  <div class="enviar-container">
    <button
      @click="enviarArquivos"
      :disabled="!arquivoCsv || !arquivoExcel || carregando"
      class="btn-enviar"
    >
      <span v-if="carregando" class="loader"></span>
      {{ carregando ? 'Enviando...' : '📤 Enviar arquivos' }}
    </button>
  </div>
</template>


<script setup>
import axios from 'axios'
import { ref } from 'vue';

const props = defineProps({
    arquivoCsv: File,
    arquivoExcel: File,
})

const emit = defineEmits(['respostaRecebida', 'arquivoPronto', 'vendedoresAtualizados'])

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
        )
        resposta.value = response.data
        console.log('Resposta do back: ', resposta.value)

        emit('respostaRecebida', resposta.value)
        emit('arquivoPronto', true)

        const vendedoresRes = await axios.get('http://127.0.0.1:5000/vendedores_tele')
        console.log('Vendedores recebidos: ', vendedoresRes.data)

        emit('vendedoresAtualizados', vendedoresRes.data)
    } catch(error) {
        console.error('Erro no envio: ', error)
        resposta.value = error?.response?.data || 'Erro desconhecido'
    } finally {
        carregando.value = false
    }

}

</script>

<style scoped>
.enviar-container {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
}

.btn-enviar {
  background-color: #10b981;
  color: white;
  font-size: 1rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.btn-enviar:hover {
  background-color: #059669;
}

.btn-enviar:disabled {
  background-color: #d1d5db;
  cursor: not-allowed;
}

.loader {
  border: 3px solid #f3f3f3;
  border-top: 3px solid #ffffff;
  border-radius: 50%;
  width: 16px;
  height: 16px;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

</style>