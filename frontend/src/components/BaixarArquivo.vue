<template>
  <div class="download-container">
    <button
      @click="baixar"
      class="download-button"
    >
      Baixar resultado.xlsx
    </button>
  </div>
</template>

<script setup>
function baixar() {
  const link = document.createElement('a')
  link.href = '/download'
  link.setAttribute('download', 'resultado.xlsx')
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}
</script>

<style scoped>
.download-container {
  text-align: center; /* Centraliza o botão */
  margin-top: 1rem; /* Margem superior */
}

.download-button {
  background-color: #10b981; /* Verde */
  color: white;
  font-weight: 600;
  padding: 10px 20px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: background-color 0.2s ease, transform 0.1s ease;
  font-size: 1rem;
}

.download-button:hover {
  background-color: #059669; /* Verde mais escuro no hover */
  transform: translateY(-1px); /* Pequeno efeito de elevação */
}
</style>