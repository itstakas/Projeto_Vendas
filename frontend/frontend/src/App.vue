<template>
  <div class="container">
    <h1>Upload de arquivos</h1>

    <form @submit.prevent="enviarArquivos">
      <div>
        <label>Arquivo CSV:</label>
        <input type="file" @change="handleCsvChange" accept=".csv" />
      </div> 

      <div>
        <label>Arquivo Excel:</label>
        <input type="file" @change="handleExcelChange" accept=".xlsx, .xls" />
      </div>

      <button type="submit">Enviar</button>
    </form>

    <div v-if="resposta">
      <h2>Resposta ao servidor:</h2>
      <pre>{{ resposta }}</pre>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'

  export default{
    data(){
      return {
        arquivoCsv: null,
        arquivoExcel: null,
        resposta: null
      }
    },
    methods: {
      handleCsvChange(event){
        this.arquivoCsv = event.target.files[0]
      },
      handleExcelChange(event){
        this.arquivoExcel = event.target.files[0]
      },
      async enviarArquivos(){
        try{
          const formData = new FormData();
          formData.append('csv', this.csv_file)
          formData.append('excel', this.excel_file)

          const response = await axios.post('http://127.0.0.1:5000/upload', formData, {headers: {
            'content-Type': 'multipart/form-data'
          }
        })

        this.resposta = response.data
        } catch (error){
          console.error(error)
          this.resposta = 'Erro ao enviar arquivos'
        }
      }
    }
  }

</script>
