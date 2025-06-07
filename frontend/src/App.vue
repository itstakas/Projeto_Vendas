<script setup>
import { ref } from 'vue';
import EnviarCsvExcel from './components/EnviarCsvExcel.vue';
import Dashboard from './components/Dashboard.vue'

const dadosVendedores = ref([])
const dadosClientes = ref([])
const mostrarDashboard = ref(false)

const exibirDashboard = (clientes, vendedores) => {
    dadosClientes.value = clientes
    dadosVendedores.value = vendedores
    mostrarDashboard.value = true
}

// const receberDados = (payload) => {
//     dadosVendedores.value = payload.vendedores
//     dadosClientes.value = payload.clientes
// }
</script>

<template>  
<div>
    <EnviarCsvExcel @dadosProntos="receberDados" />

    <Dashboard
        v-if="mostrarDashboard"
        :vendedores="dadosVendedores"
        :clientes="dadosClientes"
    />
</div>
</template>

<style scoped>
.container{
    padding:2rem;    
}
</style>