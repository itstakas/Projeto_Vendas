from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
from werkzeug.utils import secure_filename
from rapidfuzz import fuzz

app = Flask(__name__)
CORS(app)  # habilita o cors e permite requisições no front (que não foi feita AINDA)

# config para upload de arquivos
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def hello_world():
    return 'Olá, backend do Flask'


@app.route('/upload', methods=['POST'])
def upload_files():

    # Verifica se 'csv_file' e 'excel_file' estão sendo requisitados
    if 'csv_file' not in request.files or 'excel_file' not in request.files:
        # Retorna uma mensagem de erro
        return jsonify({'error': 'Nenhum arquivo CSV ou Excel foi enviado'}), 400

    # pega os objetos de requisição
    csv_file = request.files.get['csv']
    excel_file = request.files.get['excel']

    # Verifica se os nomes dos arquivos não estão vazios (o que significa que um arquivo foi realmente selecionado)
    if csv_file.filename == '' or excel_file.filename == '':
        # Retorna uma mensagem de erro
        return jsonify({'error': 'Nome de arquivo vazio'}), 400

    try:
        # Confere os nomes dos arquivos para segurança
        csv_filename = secure_filename(csv_file.filename)
        excel_filename = secure_filename(excel_file.filename)

        # Cria os caminhos completos para salvar os arquivos na pasta UPLOAD_FOLDER
        csv_filepath = os.path.join(
            app.config['UPLOAD_FOLDER'], csv_file.filename)
        excel_filepath = os.path.join(
            app.config['UPLOAD_FOLDER'], excel_file.filename)

        # Salva os arquivos no disco
        csv_file.save(csv_filepath)
        excel_file.save(excel_filepath)

        # Utilizando o pandas para ler os dois arquivos
        csv_file = pd.read_csv("uploads/csv.csv", sep=";")
        excel_file = pd.read_excel("uploads/Planilha1.xlsx")

        # Compara a string da coluna 'cliente' do csv com a coluna 'NOME' do excel e mostra a probabilidade de serem iguais
        for nome_csv in csv_file['Cliente']:
            for nome_excel in excel_file['NOME']:
                ratio = fuzz.ratio(str(nome_csv), str(nome_excel))
                if ratio > 90:
                    return jsonify({'message': 'Os nomes batem'})
                else:
                    return jsonify({'message': 'Os nomes não batem'})

    except Exception as e:
        # Se algo falhou que não foi pego pelas verificações anteriores
        return jsonify({'error': f'Erro desconhecido ao processar o upload dos arquivos: {str(e)}'}), 500


if __name__ == "__main__":
    app.run(debug=True)
