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
      <button type="button" @click="baixarExcel" v-if="resposta && resposta.message">📥 Baixar Excel</button>

    </form>

    <div v-if="resposta">
      <h2>Resposta ao servidor:</h2>
      <pre>{{ resposta }}</pre>
    </div>
  </div>
  <div v-if="linkExcel">
  <a :href="linkExcel" target="_blank" download>📥 Baixar planilha preenchida</a>
</div>
</template>

<script>
  import axios from 'axios'

  export default{
    data(){
      return {
        arquivoCsv: null,
        arquivoExcel: null,
        resposta: null,
        linkExcel: null
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
          formData.append('csv', this.arquivoCsv)
          formData.append('excel', this.arquivoExcel)

          const response = await axios.post('http://127.0.0.1:5000/upload', formData, {headers: {
            'Content-Type': 'multipart/form-data'
          }
        })

        this.resposta = response.data
        } catch (error){
          console.error(error)
          this.resposta = 'Erro ao enviar arquivos'
        }
      },


      async baixarExcel() {
        try {
          const response = await axios.get('http://127.0.0.1:5000/download', {
            responseType: 'blob'
          });

          const blob = new Blob([response.data], {
            type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
          });

          const url = window.URL.createObjectURL(blob);

          const link = document.createElement('a')
          link.href = url;

          link.setAttribute('download', 'resultado.xlsx');

          document.body.appendChild(link);
          link.click();

          document.body.removeChild(link);

          window.URL.revokeObjectURL(url);
        } catch (error) {
          console.error('Erro ao baixar planilha:', error);
          alert('Não foi possível gerar o Excel. Envie os arquivos primeiro.');
        }
      },
  }}

</script>
 