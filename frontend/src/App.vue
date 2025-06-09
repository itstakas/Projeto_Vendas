<script setup>
import { ref } from 'vue';
import EnviarCsvExcel from './components/EnviarCsvExcel.vue';
import Dashboard from './components/Dashboard.vue'

const mostrarDashboard = ref(false)
const dadosVendedores = ref([])

const exibirDashboard = (payload) => {
  dadosVendedores.value = payload
  mostrarDashboard.value = true
}
</script>

<template>  
<div>
    <EnviarCsvExcel @dadosProntos="exibirDashboard" />

    <Dashboard
        v-if="mostrarDashboard"
        :dados="dadosVendedores"
    />
</div>
</template>

<style scoped>
.container{
    padding:2rem;    
}
</style>