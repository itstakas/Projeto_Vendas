<template>
  <div class="container">
    <h1>Upload de arquivos</h1>

    <!-- Formulário para upload, evita recarregar a página com @submit.prevent -->
    <form @submit.prevent="enviarArquivos">

      <!-- Exibe mensagem de carregamento enquanto arquivos são processados -->
      <div v-if="loading" class="loading">Carregando arquivos, por favor aguarde...</div>

      <div>
        <label>Arquivo CSV:</label>
        <!-- Input para selecionar arquivo CSV, chama handleCsvChange ao alterar -->
        <input type="file" @change="handleCsvChange" accept=".csv" />
      </div> 

      <div>
        <label>Arquivo Excel:</label>
        <!-- Input para selecionar arquivo Excel, chama handleExcelChange ao alterar -->
        <input type="file" @change="handleExcelChange" accept=".xlsx, .xls" />
      </div>

      <!-- Botão para enviar arquivos -->
      <button type="submit">Enviar</button>

      <!-- Botão para baixar o Excel gerado, só aparece se backend respondeu com chave 'message' -->
      <button type="button" @click="baixarExcel" v-if="resposta && resposta.message">
        📥 Baixar Excel
      </button>
    </form>

    <!-- Mostra a resposta do backend em formato JSON, se existir -->
    <div v-if="resposta">
      <h2>Resposta ao servidor:</h2>
      <pre>{{ resposta }}</pre>
    </div>

    <!-- Link alternativo para baixar o arquivo Excel gerado, se existir -->
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
      arquivoCsv: null,      // Guarda o arquivo CSV selecionado pelo usuário
      arquivoExcel: null,    // Guarda o arquivo Excel selecionado pelo usuário
      resposta: null,        // Guarda a resposta JSON do backend após upload
      linkExcel: null,       // Link direto para download do Excel (opcional)
      loading: false         // Variável para indicar se está carregando/processando
    }
  },

  methods: {
    // Método chamado quando o usuário seleciona o arquivo CSV
    handleCsvChange(event) {
      this.arquivoCsv = event.target.files[0]  // Guarda o primeiro arquivo selecionado
    },

    // Método chamado quando o usuário seleciona o arquivo Excel
    handleExcelChange(event) {
      this.arquivoExcel = event.target.files[0]  // Guarda o primeiro arquivo selecionado
    },

    // Método para enviar os arquivos ao backend via POST usando axios
    async enviarArquivos() {
      this.loading = true;  // Ativa o indicador de carregamento
      try {
        // Cria um FormData para enviar arquivos via multipart/form-data
        const formData = new FormData()
        formData.append('csv', this.arquivoCsv)       // Adiciona o arquivo CSV
        formData.append('excel', this.arquivoExcel)   // Adiciona o arquivo Excel

        // Faz o POST para o endpoint /upload do backend Flask
        const response = await axios.post(
          'http://127.0.0.1:5000/upload',
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data'  // Define o header para upload de arquivos
            }
          }
        )

        this.resposta = response.data  // Armazena a resposta JSON do backend

      } catch (error) {
        console.error(error)
        this.resposta = 'Erro ao enviar arquivos'  // Mensagem em caso de erro
      }
      finally {
        this.loading = false;  // Desativa o indicador de carregamento
      }
    },

    // Método para baixar o Excel gerado no backend
    async baixarExcel() {
      try {
        // Faz a requisição GET para baixar o arquivo Excel como blob (binário)
        const response = await axios.get('http://127.0.0.1:5000/download', {
          responseType: 'blob'   // Recebe o arquivo como blob para download
        })

        // Cria um Blob com o conteúdo recebido e o tipo MIME correto
        const blob = new Blob([response.data], {
          type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        })

        // Cria uma URL temporária para o blob (arquivo em memória)
        const url = window.URL.createObjectURL(blob)

        // Cria um elemento <a> invisível para simular o clique de download
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', 'resultado.xlsx')  // Nome do arquivo para download
        document.body.appendChild(link)
        link.click()  // Executa o clique para disparar o download

        // Remove a URL temporária da memória para liberar recursos
        window.URL.revokeObjectURL(url)

      } catch (error) {
        console.error('Erro ao baixar planilha:', error)
        alert('Não foi possível gerar o Excel. Envie os arquivos primeiro.')
      }
    }
  }
}
</script>
