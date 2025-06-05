from main import app
from flask import request, jsonify, send_file
from werkzeug.utils import secure_filename
from controladores.Classes import ProcessaDados
from controladores.comparador import comparar_e_preencher
import pandas as pd
import os
from utils.limpeza import remover_colunas_denecessarias, contratos_pagos_em_abril, filtrar_mes_atual
from utils.macro import colar_e_executar_macro

# Rota que processa os dados no back end, recebe csv, recebe excel e executa macro, gerando resultado.xlsx


@app.route('/upload', methods=['POST'])
def upload_files():
    print("Recebendo arquivos...")

    csv_file = request.files.get('csv')
    excel_file = request.files.get('excel')

    if not csv_file or not excel_file:
        print("Erro: CSV ou Excel não enviados")
        return jsonify({'error': 'Nenhum arquivo CSV ou Excel foi enviado'}), 400

    if csv_file.filename == '' or excel_file.filename == '':
        print("Erro: Nome de arquivo vazio")
        return jsonify({'error': 'Nome de arquivo vazio'}), 400

    try:
        csv_filename = secure_filename(csv_file.filename)
        excel_filename = secure_filename(excel_file.filename)

        csv_path = os.path.join(app.config['UPLOAD_FOLDER'], csv_filename)
        excel_path = os.path.join(app.config['UPLOAD_FOLDER'], excel_filename)

        print(f"Salvando CSV em: {csv_path}")
        csv_file.save(csv_path)
        print(f"Salvando Excel em: {excel_path}")
        excel_file.save(excel_path)

        processador = ProcessaDados(csv_path, excel_path)

        print("Filtrando dados do CSV pelo mês atual...")
        processador.csv_df = filtrar_mes_atual(processador.csv_df)
        print(f"CSV filtrado shape: {processador.csv_df.shape}")

        print("Comparando e preenchendo dados...")
        processador = comparar_e_preencher(processador)

        print("Removendo colunas desnecessárias...")
        processador.excel_df = remover_colunas_denecessarias(
            processador.excel_df)

        print("Removendo contratos pagos em abril...")
        processador.excel_df = contratos_pagos_em_abril(processador.excel_df)

        caminho_macro = r'C:\Users\Pax Primavera\Documents\MeusProjetos\Projeto_Vendas\Macro\Macro - Troca de Data.xlsm'

        print("Executando macro...")
        df_macro, caminho_arquivo_macro_gerado = colar_e_executar_macro(
            processador.excel_df, caminho_macro)

        print("DataFrame após macro:")
        print(df_macro.head())
        print(f"Shape: {df_macro.shape}")

        processador.excel_df = df_macro

        # Para simplificar, salvaremos sempre aqui:
        caminho_resultado = os.path.join(
            app.config['UPLOAD_FOLDER'], 'resultado.xlsx')

        print(f"Salvando arquivo final em: {caminho_resultado}")
        processador.salvar_excel_preenchido(caminho_resultado)

        if os.path.exists(caminho_resultado):
            tamanho = os.path.getsize(caminho_resultado)
            print(f"Arquivo salvo com tamanho: {tamanho} bytes")
        else:
            print("Erro: arquivo final não encontrado após salvar!")

        # Retorna o caminho para que o front-end saiba onde baixar
        return jsonify({'download_path': '/download'}), 200

    except Exception as e:
        print(f"Erro ao processar arquivos: {e}")
        return jsonify({'error': str(e)}), 500

# Rota para fazer download do arquivo Excel gerado após processamento


@app.route('/download', methods=['GET'])
def download():
    caminho_arquivo = os.path.join(
        app.config['UPLOAD_FOLDER'], 'resultado.xlsx')

    if os.path.exists(caminho_arquivo):
        print(f"Enviando arquivo: {caminho_arquivo}")
        return send_file(
            caminho_arquivo,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='resultado.xlsx'
        )
    else:
        print("Erro: arquivo para download não encontrado")
        return jsonify({'error': 'Arquivo ainda não foi gerado'}), 404
