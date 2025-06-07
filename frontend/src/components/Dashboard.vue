<template>
    <div class="dashboard-container">
        <h2>Dashboard de vendas e clientes</h2>
        <div v-if="loading">Carregando dados</div>
        <ul v-else>
            <li v-for="vendedor in dados" v-bind:key="vendedor.vendedor">
                <strong>{{ vendedor.vendedor }} - {{ vendedor.qtd_clientes }} clientes</strong>
                <ul>
                    <li v-for="cliente in vendedor.clientes" :key="cliente">{{ cliente }}</li>
                </ul>
            </li>
        </ul>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const dados = ref([])
const loading = reg (true)

onMounted(async() => {
    try {
        const res = await axios.get('http://localhost:5000/api/dashboard')
        dados.value = res.data
    } catch (err) {
        console.log('Erro ao carregar dados: ', err)
    } finally {
        loading.value = false
    }
})
</script>

<style scoped>
.dashboard-container{
    background-color: 1e1e1e;
    color: #fff;
    padding: 20px;
    border-radius: 10px;
}    
ul {
    list-style-type: none;
    padding-left: 0;
}
li {
    margin-bottom: 10px;
}

</style>