from main import app
from flask import request, jsonify
from werkzeug.utils import secure_filename
from controladores.Classes import ProcessaDados
from controladores.comparador import comparar_e_preencher
import pandas as pd
from flask import send_file
import os
from utils.limpeza import remover_colunas_denecessarias, contratos_pagos_em_abril, filtrar_mes_atual
from utils.macro import colar_e_executar_macro


# Rota raiz, apenas para teste de funcionamento do backend Flask
@app.route("/")
def hello_world():
    return 'Olá, backend do Flask'


# Rota para upload dos arquivos CSV e Excel via POST
@app.route('/upload', methods=["POST"])
def upload_files():

    # Pega os arquivos enviados na requisição, com os nomes 'csv' e 'excel'
    csv_file = request.files.get('csv')
    excel_file = request.files.get('excel')

    # Verifica se os arquivos CSV e Excel foram enviados na requisição
    if 'csv' not in request.files or 'excel' not in request.files:
        # Caso não tenha enviado um dos arquivos, retorna erro 400 com mensagem
        return jsonify({'error': 'Nenhum arquivo CSV ou Excel foi enviado'}), 400

    # Verifica se os nomes dos arquivos não estão vazios, para garantir que o usuário escolheu os arquivos
    if csv_file.filename == '' or excel_file.filename == '':
        # Caso algum nome esteja vazio, retorna erro 400 com mensagem
        return jsonify({'error': 'Nome de arquivo vazio'}), 400

    try:
        # Sanitiza os nomes dos arquivos para evitar problemas de segurança
        csv_filename = secure_filename(csv_file.filename)
        excel_filename = secure_filename(excel_file.filename)

        # Cria os caminhos completos para salvar os arquivos na pasta configurada UPLOAD_FOLDER
        csv_path = os.path.join(app.config['UPLOAD_FOLDER'], csv_filename)
        excel_path = os.path.join(app.config['UPLOAD_FOLDER'], excel_filename)

        # Salva os arquivos no disco no local definido
        csv_file.save(csv_path)
        excel_file.save(excel_path)

        # Cria uma instância da classe ProcessaDados, que irá processar os arquivos, passando os caminhos
        processador = ProcessaDados(csv_path, excel_path)

        # Filtra os dados do CSV para manter apenas os registros do mês atual
        processador.csv_df = filtrar_mes_atual(processador.csv_df)    

        # Executa a função que compara os dados entre CSV e Excel e preenche as informações necessárias
        processador = comparar_e_preencher(processador)
        
        # Remove colunas desnecessárias do DataFrame do Excel para limpeza dos dados antes de salvar
        processador.excel_df = remover_colunas_denecessarias(processador.excel_df)

        # Remove os clientes que já foram pagos no mês de abril (filtro específico)
        processador.excel_df = contratos_pagos_em_abril(processador.excel_df)

        #caminho da macro
        caminho_macro = r'C:\Users\Pax Primavera\Documents\MeusProjetos\Projeto_Vendas\Macro\Macro - Troca de Data.xlsm'

        #pega o arquivo excel ja tratado e aplica a macro
        processador.excel_df = colar_e_executar_macro(processador.excel_df, caminho_macro)

        # Caso queira formatar datas do formato mm/dd/aaaa para dd/mm/aaaa (comentado aqui)
        # processador.excel_df = formatar_mes_atual(processador.excel_df)
         
        # Define o caminho onde o arquivo Excel final será salvo após o processamento
        caminho_saida = os.path.join(app.config['UPLOAD_FOLDER'], 'Fechamento_preenchido.xlsx')

        # Salva o DataFrame Excel processado em um arquivo no caminho definido
        processador.salvar_excel_preenchido(caminho_saida)

        # Retorna uma resposta JSON confirmando o sucesso do processamento e que o arquivo foi gerado
        return jsonify({
            'message': 'Processamento concluido com sucesso',
            'arquivo_gerado': True
        })

    except Exception as e:
        # Caso aconteça algum erro inesperado, imprime no console e retorna mensagem de erro 500
        print(f"Erro ao processar arquivos: {str(e)}")
        return jsonify({'error': f'Erro desconhecido ao processar o upload dos arquivos: {str(e)}'}), 500


# Rota para fazer download do arquivo Excel gerado após processamento
@app.route("/download", methods=["GET"])
def download_excel():
    # Define o caminho do arquivo gerado
    caminho_arquivo = os.path.join(
        app.config['UPLOAD_FOLDER'], 'Fechamento_preenchido.xlsx')

    # Verifica se o arquivo existe
    if os.path.exists(caminho_arquivo):
        # Envia o arquivo para download com o nome definido
        return send_file(
            caminho_arquivo,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='Fechamento_preenchido.xlsx'
        )
    else:
        # Se o arquivo não existir, retorna erro 404 com mensagem
        return jsonify({'error': 'Arquivo ainda não foi gerado'}), 404
