from flask import request, jsonify, send_file, Blueprint, current_app as app
from werkzeug.utils import secure_filename
from controladores.Classes import ProcessaDados
from controladores.comparador import comparar_e_preencher
from utils.limpeza import remover_colunas_desnecessarias, remover_clientes_excluidos, filtrar_mes_atual
from utils.macro import colar_e_executar_macro
from utils.adicionar_clientes import adicionar_clientes_manualmente
import os
import pandas as pd
import traceback
from unidecode import unidecode
import re

views = Blueprint('views', __name__)

@views.route('/upload', methods=['POST'])
def upload_files():
    print("Recebendo arquivos...")

    csv_file = request.files.get('csv')
    excel_file = request.files.get('excel')

    if not csv_file or not excel_file:
        return jsonify({'error': 'Nenhum arquivo CSV ou Excel foi enviado'}), 400

    if csv_file.filename == '' or excel_file.filename == '':
        return jsonify({'error': 'Nome de arquivo vazio'}), 400

    try:
        upload_folder = app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)

        csv_path = os.path.join(upload_folder, secure_filename(csv_file.filename))
        excel_path = os.path.join(upload_folder, secure_filename(excel_file.filename))

        csv_file.save(csv_path)
        excel_file.save(excel_path)

        processador = ProcessaDados(csv_path, excel_path)

        # Pré-processamento
        processador.csv_df = filtrar_mes_atual(processador.csv_df)
        processador = comparar_e_preencher(processador)
        processador.excel_df = remover_colunas_desnecessarias(processador.excel_df)
        processador.excel_df = remover_clientes_excluidos(processador.excel_df)

        # Executa macro
        caminho_macro = r'C:\Users\Pax Primavera\Documents\MeusProjetos\Projeto_Vendas\Macro\Macro - Troca de Data.xlsm'
        df_macro, caminho_macro_gerado = colar_e_executar_macro(processador.excel_df, caminho_macro)

        # Salva resultado final
        processador.excel_df = df_macro
        caminho_resultado = os.path.join(upload_folder, 'resultado.xlsx')
        processador.salvar_excel_preenchido(caminho_resultado)
        adicionar_clientes_manualmente(caminho_resultado)

        if not os.path.exists(caminho_resultado):
            return jsonify({'error': 'Erro ao salvar o arquivo final'}), 500

        return jsonify({'download_path': '/download'}), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@views.route('/download', methods=['GET'])
def download():
    caminho_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], 'resultado.xlsx')
    if os.path.exists(caminho_arquivo):
        return send_file(
            caminho_arquivo,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='resultado.xlsx'
        )
    return jsonify({'error': 'Arquivo ainda não foi gerado'}), 404

@views.route('/vendedores_tele', methods=['GET'])
def vendedores_tele():
    caminho = os.path.join(app.config['UPLOAD_FOLDER'], "resultado.xlsx")
    if not os.path.exists(caminho):
        return jsonify({'error': 'Arquivo resultado.xlsx não encontrado!'}), 404

    df = pd.read_excel(caminho, dtype=str, engine='openpyxl')

    if 'DATA_CONTRATO' not in df.columns or 'VENDEDOR_TELE' not in df.columns:
        return jsonify({'error': 'Colunas esperadas não encontradas no Excel'}), 400

    df['DATA_CONTRATO'] = pd.to_datetime(df['DATA_CONTRATO'], errors='coerce')
    df_vendedores = df.dropna(subset=['VENDEDOR_TELE']).copy()
    df_vendedores['MES'] = df_vendedores['DATA_CONTRATO'].dt.to_period('M').astype(str)

    vendas_por_vendedor = df_vendedores.groupby(['VENDEDOR_TELE', 'MES']).size().reset_index(name='QTD_VENDAS')

    resultado = []
    for vendedor in vendas_por_vendedor['VENDEDOR_TELE'].unique():
        vendas = vendas_por_vendedor[vendas_por_vendedor['VENDEDOR_TELE'] == vendedor]
        resultado.append({
            'nome': vendedor,
            'total_vendas': int(vendas['QTD_VENDAS'].sum()),
            'vendas_mensais': vendas[['MES', 'QTD_VENDAS']].to_dict(orient='records')
        })

    return jsonify(resultado)

@views.route('/vendedor_tele/<nome>', methods=['GET'])
def detalhes_vendedor(nome):
    caminho = os.path.join(app.config['UPLOAD_FOLDER'], "resultado.xlsx")
    if not os.path.exists(caminho):
        return jsonify([])

    df = pd.read_excel(caminho, dtype=str, engine='openpyxl')

    if 'NOME' not in df.columns or 'DATA_CONTRATO' not in df.columns or 'VENDEDOR_TELE' not in df.columns:
        return jsonify([])

    nome_normalizado = nome.strip().lower()
    df['VENDEDOR_TELE'] = df['VENDEDOR_TELE'].fillna('').str.strip().str.lower()
    df_vendedor = df[df['VENDEDOR_TELE'] == nome_normalizado].copy()

    df_vendedor['DATA_CONTRATO'] = pd.to_datetime(df_vendedor['DATA_CONTRATO'], errors='coerce')

    # Trata datas inválidas como string vazia
    df_vendedor['DATA_CONTRATO'] = df_vendedor['DATA_CONTRATO'].dt.strftime('%d/%m/%Y')
    df_vendedor['DATA_CONTRATO'] = df_vendedor['DATA_CONTRATO'].fillna("03/06/2025")

    resultado = df_vendedor[['NOME', 'DATA_CONTRATO']].copy()
    return jsonify(resultado.to_dict(orient='records'))


