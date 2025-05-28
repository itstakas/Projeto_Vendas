<template>
  <div class="container">
    <h1>Upload de arquivos</h1>

    <form @submit.prevent="enviarArquivos">
      <div v-if="loading" class="loading">Carregando arquivos, por favor aguarde...</div>
      <div>
        <label>Arquivo CSV:</label>
        <input type="file" @change="handleCsvChange" accept=".csv" />
      </div> 

      <div>
        <label>Arquivo Excel:</label>
        <input type="file" @change="handleExcelChange" accept=".xlsx, .xls" />
      </div>

      <button type="submit">Enviar</button>

      <!-- Botão para baixar Excel gerado, só aparece se a resposta tiver a chave message -->
      <button type="button" @click="baixarExcel" v-if="resposta && resposta.message">
        📥 Baixar Excel
      </button>
    </form>

    <!-- Mostra resposta do backend, se existir -->
    <div v-if="resposta">
      <h2>Resposta ao servidor:</h2>
      <pre>{{ resposta }}</pre>
    </div>

    <!-- Link alternativo para baixar o Excel (caso esteja disponível diretamente) -->
    <div v-if="linkExcel">
      <a :href="linkExcel" target="_blank" download>📥 Baixar planilha preenchida</a>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      arquivoCsv: null,      // Armazena o arquivo CSV selecionado
      arquivoExcel: null,    // Armazena o arquivo Excel selecionado
      resposta: null,        // Armazena a resposta do backend
      linkExcel: null,        // (Opcional) Link direto para o Excel gerado
      loading: false          //tela de loading instanciada
    }
  },

  methods: {
    // Armazena o arquivo CSV ao selecionar
    handleCsvChange(event) {
      this.arquivoCsv = event.target.files[0]
    },

    // Armazena o arquivo Excel ao selecionar
    handleExcelChange(event) {
      this.arquivoExcel = event.target.files[0]
    },

    // Envia os arquivos para o backend Flask
    async enviarArquivos() {
      this.loading = true; //começa o loading
      try {
        const formData = new FormData()
        formData.append('csv', this.arquivoCsv)
        formData.append('excel', this.arquivoExcel)

        const response = await axios.post(
          'http://127.0.0.1:5000/upload',
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }
        )

        this.resposta = response.data  // Armazena resposta do backend

      } catch (error) {
        console.error(error)
        this.resposta = 'Erro ao enviar arquivos'
      }
      finally{
        this.loading = false; //Finaliza o Loading
      }
    },

    // Baixa o Excel gerado do backend
    async baixarExcel() {
      try {
        // 1. Recebe o arquivo Excel do backend como blob (binário)
        const response = await axios.get('http://127.0.0.1:5000/download', {
          responseType: 'blob'
        })

        // 2. Cria um Blob JavaScript com esse conteúdo
        const blob = new Blob([response.data], {
          type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        })

        // 3. Cria um link TEMPORÁRIO para esse arquivo blob
        const url = window.URL.createObjectURL(blob)

        // 4. Cria um <a> invisível com esse link, e força o clique pra baixar
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', 'resultado.xlsx')  // Nome do arquivo
        document.body.appendChild(link)
        link.click()  // Clica sozinho

        // 5. Remove o link temporário da memória do navegador
        window.URL.revokeObjectURL(url)

      } catch (error) {
        console.error('Erro ao baixar planilha:', error)
        alert('Não foi possível gerar o Excel. Envie os arquivos primeiro.')
      }
    }
  }
}
</script>
