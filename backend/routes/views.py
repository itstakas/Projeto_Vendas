# Importa tudo que a gente precisa:
# - 'views' é pra criar a rota (o "endereço" da página)
# - 'request' pra pegar os arquivos que o usuário envia
# - 'jsonify' pra mandar respostas em formato JSON (que o navegador entende)
# - 'os' e 'sys' pra mexer com pastas e caminhos de arquivos
# - 'secure_filename' pra deixar os nomes dos arquivos mais seguros
# - 'traceback' pra mostrar erros detalhados pra gente no terminal
# - E as nossas próprias funções que fazem o trabalho pesado

from flask import request, jsonify, send_file, Blueprint, current_app as app
from werkzeug.utils import secure_filename
from controladores.Classes import ProcessaDados
from controladores.comparador import comparar_e_preencher
from utils.limpeza import remover_colunas_desnecessarias, remover_clientes_excluidos, filtrar_mes_atual
from utils.macro import colar_e_executar_macro
from utils.adicionar_clientes import adicionar_clientes_manualmente
from excel_processador import localizar_e_substituir_celulas
import os
import pandas as pd
import traceback
from unidecode import unidecode
import re
import sys

views = Blueprint('views', __name__)


@views.route('/upload', methods=['POST'])
def upload_files():
    print("Recebendo arquivos...")

    # Pega o arquivo 'csv' e o 'excel' que o usuário enviou pelo site
    csv_file = request.files.get('csv')
    excel_file = request.files.get('excel')

    # Checa se os arquivos realmente vieram. Se não, manda um erro.
    if not csv_file or not excel_file:
        return jsonify({'error': 'Nenhum arquivo CSV ou Excel foi enviado'}), 400

    # Checa se os arquivos não têm nome vazio.
    if csv_file.filename == '' or excel_file.filename == '':
        return jsonify({'error': 'Nome de arquivo vazio'}), 400

    try:
        # Descobre onde o nosso programa está rodando. Isso é importante pra achar os arquivos.
        if getattr(sys, 'frozen', False):
            # Se for um programa .exe (depois que a gente "empacota" com PyInstaller)
            application_path = sys._MEIPASS
        else:
            # Se a gente estiver rodando o script Python normalmente (no desenvolvimento)
            application_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

        # Define o nome da pasta onde vamos salvar os uploads e os resultados
        upload_folder = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'uploads_app')
        # Cria essa pasta, caso ela ainda não exista
        os.makedirs(upload_folder, exist_ok=True)
        # Guarda o caminho dessa pasta nas configurações do app
        app.config['UPLOAD_FOLDER'] = upload_folder

        # Define o caminho completo e o nome seguro para os arquivos que o usuário enviou
        csv_path = os.path.join(upload_folder, secure_filename(csv_file.filename))
        excel_path = os.path.join(upload_folder, secure_filename(excel_file.filename))

        # Salva os arquivos do usuário nessa pasta
        csv_file.save(csv_path)
        excel_file.save(excel_path)

        # Cria nosso "ajudante" (o ProcessaDados) que vai carregar e organizar os dados pra gente
        processador = ProcessaDados(csv_path, excel_path)

        # Define onde está o nosso arquivo de "regras" (o antigo arquivo da macro)
        caminho_macro = os.path.join(application_path, 'Macro - Troca de Data.xlsm')

        # Aqui a gente aplica todas as nossas regras de negócio na planilha
        processador.csv_df = filtrar_mes_atual(processador.csv_df)
        processador = comparar_e_preencher(processador)
        processador.excel_df = remover_colunas_desnecessarias(processador.excel_df)
        processador.excel_df = remover_clientes_excluidos(processador.excel_df)

        # Define o nome e o caminho do nosso arquivo final
        caminho_resultado = os.path.join(upload_folder, 'resultado.xlsx')
        # Salva a planilha, já com os dados preparados, no arquivo 'resultado.xlsx'
        processador.salvar_excel_preenchido(caminho_resultado)

        localizar_e_substituir_celulas(caminho_resultado, caminho_macro)

        adicionar_clientes_manualmente(caminho_resultado)

        if not os.path.exists(caminho_resultado):
            return jsonify({'error': 'Erro ao salvar o arquivo final'}), 500

        return jsonify({'download_path': '/download'}), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@views.route('/download', methods=['GET'])
def download():
    caminho_arquivo = os.path.join(
        app.config['UPLOAD_FOLDER'], 'resultado.xlsx')
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
    df_vendedores['MES'] = df_vendedores['DATA_CONTRATO'].dt.to_period(
        'M').astype(str)

    vendas_por_vendedor = df_vendedores.groupby(
        ['VENDEDOR_TELE', 'MES']).size().reset_index(name='QTD_VENDAS')

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
    df['VENDEDOR_TELE'] = df['VENDEDOR_TELE'].fillna(
        '').str.strip().str.lower()
    df_vendedor = df[df['VENDEDOR_TELE'] == nome_normalizado].copy()

    df_vendedor['DATA_CONTRATO'] = pd.to_datetime(
        df_vendedor['DATA_CONTRATO'], errors='coerce')

    # Trata datas inválidas como string vazia
    df_vendedor['DATA_CONTRATO'] = df_vendedor['DATA_CONTRATO'].dt.strftime(
        '%d/%m/%Y')
    df_vendedor['DATA_CONTRATO'] = df_vendedor['DATA_CONTRATO'].fillna(
        "03/06/2025")

    resultado = df_vendedor[['NOME', 'DATA_CONTRATO']].copy()
    return jsonify(resultado.to_dict(orient='records'))


@views.route('/vendedores_porta_a_porta', methods=['GET'])
def vendedores_porta_a_porta():
    caminho = os.path.join(app.config['UPLOAD_FOLDER'], "resultado.xlsx")
    if not os.path.exists(caminho):
        return jsonify({'error': 'Arquivo resultado.xlsx não encontrado!'}), 404

    df = pd.read_excel(caminho, dtype=str, engine='openpyxl')

    if 'DATA_CONTRATO' not in df.columns or 'VENDEDOR' not in df.columns:
        return jsonify({'error': 'Colunas esperadas não encontradas no Excel'}), 400

    df['DATA_CONTRATO'] = pd.to_datetime(df['DATA_CONTRATO'], errors='coerce')
    df_vendedores = df.dropna(subset=['VENDEDOR']).copy()
    df_vendedores['MES'] = df_vendedores['DATA_CONTRATO'].dt.to_period(
        'M').astype(str)

    vendas_por_vendedor = df_vendedores.groupby(
        ['VENDEDOR', 'MES']).size().reset_index(name='QTD_VENDAS')

    resultado = []
    for vendedor in vendas_por_vendedor['VENDEDOR'].unique():
        vendas = vendas_por_vendedor[vendas_por_vendedor['VENDEDOR'] == vendedor]
        resultado.append({
            'nome': vendedor,
            'total_vendas': int(vendas['QTD_VENDAS'].sum()),
            'vendas_mensais': vendas[['MES', 'QTD_VENDAS']].to_dict(orient='records')
        })

    return jsonify(resultado)


@views.route('/vendedores_porta_a_porta/<nome>', methods=['GET'])
def detalhes_vendedor_porta_a_porta(nome):
    caminho = os.path.join(app.config['UPLOAD_FOLDER'], "resultado.xlsx")
    if not os.path.exists(caminho):
        return jsonify([])

    df = pd.read_excel(caminho, dtype=str, engine='openpyxl')

    if 'NOME' not in df.columns or 'DATA_CONTRATO' not in df.columns or 'VENDEDOR' not in df.columns:
        return jsonify([])

    nome_normalizado = nome.strip().lower()
    df['VENDEDOR'] = df['VENDEDOR'].fillna('').str.strip().str.lower()
    df_vendedor = df[df['VENDEDOR'] == nome_normalizado].copy()

    df_vendedor['DATA_CONTRATO'] = pd.to_datetime(
        df_vendedor['DATA_CONTRATO'], errors='coerce')

    # Trata datas inválidas como string vazia
    df_vendedor['DATA_CONTRATO'] = df_vendedor['DATA_CONTRATO'].dt.strftime(
        '%d/%m/%Y')
    df_vendedor['DATA_CONTRATO'] = df_vendedor['DATA_CONTRATO'].fillna(
        "03/06/2025")

    resultado = df_vendedor[['NOME', 'DATA_CONTRATO']].copy()
    return jsonify(resultado.to_dict(orient='records'))
