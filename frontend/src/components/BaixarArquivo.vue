<!-- BaixarArquivo.vue -->
<template>
  <div class="mt-4">
    <button
      @click="baixar"
      class="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
    >
      Baixar resultado.xlsx
    </button>
  </div>
</template>

<script setup>
function baixar() {
  const link = document.createElement('a')
  link.href = 'http://127.0.0.1:5000/download'
  link.setAttribute('download', 'resultado.xlsx')
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}
</script>
