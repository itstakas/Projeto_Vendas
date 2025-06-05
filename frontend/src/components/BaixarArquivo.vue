<template>
  <button v-if="visivel" @click="baixar">
    Baixar resultado.xlsx
  </button>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  visivel: Boolean
})

const baixar = () => {
  // Isso abre a rota do backend diretamente para iniciar o download
  window.open('http://127.0.0.1:5000/download', '_blank')
}
</script>
