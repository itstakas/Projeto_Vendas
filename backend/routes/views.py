# Arquivo: backend/routes/views.py

# --- CORREÇÃO NOS IMPORTS ---
# Usamos '..' para subir um nível (da pasta 'routes' para 'backend')
# e então encontrar as pastas 'controladores' e 'utils'.
from flask import request, jsonify, send_file, Blueprint, current_app as app
from werkzeug.utils import secure_filename
from ..processamento_de_dados.processador_vendas import ProcessaDados
from ..processamento_de_dados.comparador import comparar_e_preencher
from ..utils.limpeza import remover_colunas_desnecessarias, remover_clientes_excluidos, filtrar_mes_atual
from ..utils.adicionar_clientes import adicionar_clientes_manualmente
import os
import pandas as pd
import traceback
import sys

# O resto do seu código já estava quase perfeito.
# Mantive as listas de nomes aqui como você definiu.
NOMES_PORTA_A_PORTA = [
    "GLEICI IDALINA PEREIRA RUIZ", "VEND.SILAS DE OLIVEIRA", "MARIA ROSELI",
    "ANA BEATRIZ DO PRADO SCAVONE", "ELIZABETE ALVES", "TALITA JUNIA DA CONCEICAO SILVA"
]
NOMES_EXTERNA = [
    "ANDRE MENOSSI", "MARIO ANTONIO DELGADO MOREL", "NATANAEL DE SOUZA BRASIL",
    "ANA GRACIELA BENITEZ", "DIANA ELIZABETH FERREIRA PALACIOS", "DEMETRIO FIDEL INSFRAN BALBUENA"
]

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
        if getattr(sys, 'frozen', False):
            application_path = sys._MEIPASS
        else:
            application_path = os.path.abspath(os.path.join(
                os.path.dirname(os.path.abspath(__file__)), '..'))

        upload_folder = os.path.join(os.path.dirname(
            os.path.abspath(sys.argv[0])), 'uploads_app')
        os.makedirs(upload_folder, exist_ok=True)
        app.config['UPLOAD_FOLDER'] = upload_folder

        csv_path = os.path.join(upload_folder, secure_filename(csv_file.filename))
        excel_path = os.path.join(upload_folder, secure_filename(excel_file.filename))

        csv_file.save(csv_path)
        excel_file.save(excel_path)

        # A lógica principal, que já está correta
        processador = ProcessaDados(csv_path, excel_path)
        processador.csv_df = filtrar_mes_atual(processador.csv_df)
        processador = comparar_e_preencher(processador)
        processador.excel_df = remover_colunas_desnecessarias(processador.excel_df)
        processador.excel_df = remover_clientes_excluidos(processador.excel_df)
        
        caminho_resultado = os.path.join(upload_folder, 'resultado.xlsx')
        processador.salvar_excel_preenchido(caminho_resultado)
        
        adicionar_clientes_manualmente(caminho_resultado)

        if not os.path.exists(caminho_resultado):
            return jsonify({'error': 'Erro ao salvar o arquivo final'}), 500

        return jsonify({'download_path': '/download'}), 200


    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# --- O RESTO DAS SUAS ROTAS (QUE JÁ ESTAVAM CORRETAS) ---

@views.route('/download', methods=['GET'])
def download():
    # ... seu código de download ...
    caminho_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], 'resultado.xlsx')
    if os.path.exists(caminho_arquivo):
        return send_file(caminho_arquivo, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name='resultado.xlsx')
    return jsonify({'error': 'Arquivo ainda não foi gerado'}), 404



@views.route('/vendedores_tele', methods=['GET'])
def vendedores_tele():
    # ... seu código de vendedores_tele ...
    caminho = os.path.join(app.config['UPLOAD_FOLDER'], "resultado.xlsx")
    if not os.path.exists(caminho):
        return jsonify({'error': 'Arquivo resultado.xlsx não encontrado!'}), 404
    df = pd.read_excel(caminho, dtype=str, engine='openpyxl')
    if 'DATA_CONTRATO' not in df.columns or 'VENDEDOR_TELE' not in df.columns:
        return jsonify({'error': 'Colunas esperadas não encontradas no Excel'}), 400
    df['DATA_CONTRATO'] = pd.to_datetime(df['DATA_CONTRATO'], errors='coerce', dayfirst=True)
    df_vendedores = df.dropna(subset=['VENDEDOR_TELE']).copy()
    df_vendedores['MES'] = df_vendedores['DATA_CONTRATO'].dt.to_period('M').astype(str)
    vendas_por_vendedor = df_vendedores.groupby(['VENDEDOR_TELE', 'MES']).size().reset_index(name='QTD_VENDAS')
    resultado = []
    for vendedor in vendas_por_vendedor['VENDEDOR_TELE'].unique():
        vendas = vendas_por_vendedor[vendas_por_vendedor['VENDEDOR_TELE'] == vendedor]
        resultado.append({'nome': vendedor, 'total_vendas': int(vendas['QTD_VENDAS'].sum()), 'vendas_mensais': vendas[['MES', 'QTD_VENDAS']].to_dict(orient='records')})
    return jsonify(resultado)



@views.route('/vendedor_tele/<nome>', methods=['GET'])
def detalhes_vendedor(nome):
    # ... seu código de detalhes_vendedor ...
    caminho = os.path.join(app.config['UPLOAD_FOLDER'], "resultado.xlsx")
    if not os.path.exists(caminho):
        return jsonify([])
    df = pd.read_excel(caminho, dtype=str, engine='openpyxl')
    if 'NOME' not in df.columns or 'DATA_CONTRATO' not in df.columns or 'VENDEDOR_TELE' not in df.columns:
        return jsonify([])
    nome_normalizado = nome.strip().lower()
    df['VENDEDOR_TELE'] = df['VENDEDOR_TELE'].fillna('').str.strip().str.lower()
    df_vendedor = df[df['VENDEDOR_TELE'] == nome_normalizado].copy()
    df_vendedor['DATA_CONTRATO'] = pd.to_datetime(df_vendedor['DATA_CONTRATO'], errors='coerce', dayfirst=True)
    df_vendedor['DATA_CONTRATO'] = df_vendedor['DATA_CONTRATO'].dt.strftime('%d/%m/%Y').fillna("Data Inválida")
    resultado = df_vendedor[['NOME', 'DATA_CONTRATO']].copy()
    return jsonify(resultado.to_dict(orient='records'))



@views.route('/vendedores_porta_a_porta', methods=['GET'])
def vendedores_porta_a_porta():
    # ... seu código de vendedores_porta_a_porta ...
    caminho = os.path.join(app.config['UPLOAD_FOLDER'], "resultado.xlsx")
    if not os.path.exists(caminho):
        return jsonify({'error': 'Arquivo resultado.xlsx não encontrado!'}), 404
    df = pd.read_excel(caminho, dtype=str, engine='openpyxl')
    if 'DATA_CONTRATO' not in df.columns or 'VENDEDOR' not in df.columns:
        return jsonify({'error': 'Colunas esperadas não encontradas no Excel'}), 400
    df['DATA_CONTRATO'] = pd.to_datetime(df['DATA_CONTRATO'], errors='coerce', dayfirst=True)
    df_vendedores = df.dropna(subset=['VENDEDOR']).copy()
    df_vendedores['MES'] = df_vendedores['DATA_CONTRATO'].dt.to_period('M').astype(str)
    vendas_por_vendedor = df_vendedores.groupby(['VENDEDOR', 'MES']).size().reset_index(name='QTD_VENDAS')
    resultado = []
    for vendedor in vendas_por_vendedor['VENDEDOR'].unique():
        vendas = vendas_por_vendedor[vendas_por_vendedor['VENDEDOR'] == vendedor]
        tipo = 'Outro'
        if vendedor.upper() in [nome.upper() for nome in NOMES_PORTA_A_PORTA]:
            tipo = 'porta'
        elif vendedor.upper() in [nome.upper() for nome in NOMES_EXTERNA]:
            tipo = 'externa'
        resultado.append({'nome': vendedor, 'total_vendas': int(vendas['QTD_VENDAS'].sum()), 'vendas_mensais': vendas[['MES', 'QTD_VENDAS']].to_dict(orient='records'), 'tipo_vendedor': tipo})
    return jsonify(resultado)



@views.route('/vendedores_porta_a_porta/<nome>', methods=['GET'])
def detalhes_vendedor_porta_a_porta(nome):
    # ... seu código de detalhes_vendedor_porta_a_porta ...
    caminho = os.path.join(app.config['UPLOAD_FOLDER'], "resultado.xlsx")
    if not os.path.exists(caminho):
        return jsonify([])
    df = pd.read_excel(caminho, dtype=str, engine='openpyxl')
    if 'NOME' not in df.columns or 'DATA_CONTRATO' not in df.columns or 'VENDEDOR' not in df.columns:
        return jsonify([])
    nome_normalizado = nome.strip().lower()
    df['VENDEDOR_NORMALIZADO'] = df['VENDEDOR'].fillna('').str.strip().str.lower()
    df_vendedor = df[df['VENDEDOR_NORMALIZADO'] == nome_normalizado].copy()
    df_vendedor['DATA_CONTRATO'] = pd.to_datetime(df_vendedor['DATA_CONTRATO'], errors='coerce', dayfirst=True)
    df_vendedor['DATA_CONTRATO'] = df_vendedor['DATA_CONTRATO'].dt.strftime('%d/%m/%Y').fillna("Data Inválida")
    resultado = df_vendedor[['NOME', 'DATA_CONTRATO']].copy()
    return jsonify(resultado.to_dict(orient='records'))
