from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from classes.Classes import ProcessaDados
import pandas as pd
from flask import send_file

app = Flask(__name__)
CORS(app)  # habilita o cors e permite requisições no front

# config para upload de arquivos
UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'uploads'))
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def hello_world():
    return 'Olá, backend do Flask'


@app.route('/upload', methods=["POST"])
def upload_files():

    # pega os objetos de requisição
    csv_file = request.files.get('csv')
    excel_file = request.files.get('excel')

    # Verifica se 'csv_file' e 'excel_file' estão sendo requisitados
    if 'csv' not in request.files or 'excel' not in request.files:
        # Retorna uma mensagem de erro
        return jsonify({'error': 'Nenhum arquivo CSV ou Excel foi enviado'}), 400

    # Verifica se os nomes dos arquivos não estão vazios (o que significa que um arquivo foi realmente selecionado)
    if csv_file.filename == '' or excel_file.filename == '':
        # Retorna uma mensagem de erro
        return jsonify({'error': 'Nome de arquivo vazio'}), 400

    try:
        # Confere os nomes dos arquivos para segurança
        csv_filename = secure_filename(csv_file.filename)
        excel_filename = secure_filename(excel_file.filename)

        # Cria os caminhos completos para salvar os arquivos na pasta UPLOAD_FOLDER
        csv_path = os.path.join(app.config['UPLOAD_FOLDER'], csv_filename)
        excel_path = os.path.join(app.config['UPLOAD_FOLDER'], excel_filename)

        # Salva os arquivos no disco
        csv_file.save(csv_path)
        excel_file.save(excel_path)

        processador = ProcessaDados(csv_path, excel_path)
        processador.comparar_e_preencher()
        caminho_saida = os.path.join(
            app.config['UPLOAD_FOLDER'], 'Fechamento_preenchido.xlsx')
        
        processador.salvar_excel_preenchido(caminho_saida)

        return jsonify({
            'message': 'Processamento concluido com sucesso',
            'arquivo_gerado': True
        })

    except Exception as e:

        print(f"Erro ao processar arquivos: {str(e)}")
        # Se algo falhou que não foi pego pelas verificações anteriores
        return jsonify({'error': f'Erro desconhecido ao processar o upload dos arquivos: {str(e)}'}), 500


@app.route("/download", methods=["GET"])
def download_excel():
    caminho_arquivo = os.path.join(
        app.config['UPLOAD_FOLDER'], 'Fechamento_preenchido.xlsx')
    
    if os.path.exists(caminho_arquivo):
        return send_file(
            caminho_arquivo,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='Fechamento_preenchido.xlsx'
        )
    else:
        return jsonify({'error': 'Arquivo ainda não foi gerado'}), 404


if __name__ == "__main__":
    app.run(debug=True)
