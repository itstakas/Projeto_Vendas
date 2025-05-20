from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # habilita o cors e permite requisições no front

# config para upload de arquivos, ainda opcional
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def hello_world():
    return 'Olá, backend do Flask'

@app.route('/upload', methods=['POST'])
def upload_files():

     # Verifica se 'csv_file' e 'excel_file' estão na requisição de arquivos
    if 'csv_file' not in request.files or 'excel_file' not in request.files:
          # Retorna uma mensagem de erro e um código de status HTTP 400 (Bad Request)
        return jsonify({'error': 'Nenhum arquivo CSV ou Excel foi enviado'}), 400

    #pega os objetos de requisição
    csv_file = request.files['csv_file']
    excel_file = request.files['excel_file']

    # Verifica se os nomes dos arquivos não estão vazios (o que significa que um arquivo foi realmente selecionado)
    if csv_file.filename == '' or excel_file.filename == '':
        # Retorna uma mensagem de erro e um código de status HTTP 400
        return jsonify({'error': 'Nome de arquivo vazio'}), 400

    try:
        # Sanitiza os nomes dos arquivos para segurança
        csv_filename = secure_filename(csv_file.filename)
        excel_filename = secure_filename(excel_file.filename)

        # Cria os caminhos completos para salvar os arquivos na pasta UPLOAD_FOLDER
        csv_filepath = os.path.join(app.config['UPLOAD_FOLDER'], csv_file.filename)
        excel_filepath = os.path.join(app.config['UPLOAD_FOLDER'], excel_file.filename)

        # Salva os arquivos no disco
        csv_file.save(csv_filepath)
        excel_file.save(excel_filepath)

        # Retorna uma resposta de sucesso com os caminhos dos arquivos
        return jsonify({'message': 'Arquivos CSV e Excel enviados com sucesso.', 'csv_filepath': csv_filepath, 'excel_filepath': excel_filepath}), 200

    except Exception as e:
        # Se algo falhou que não foi pego pelas verificações anteriores
        return jsonify({'error':f'Erro desconhecido ao processar o upload dos arquivos: {str(e)}'}), 500

if __name__ == "__main__":
    app.run(debug=True)
