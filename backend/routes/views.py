# Este arquivo é o "Garçom" da nossa aplicação.
# Ele define todas as "páginas" (rotas) da nossa API e decide qual
# serviço chamar para responder a cada pedido do frontend.

from flask import request, jsonify, send_file, Blueprint, current_app as app
from werkzeug.utils import secure_filename
import os
import traceback
import sys

# O Garçom conhece os serviços da "cozinha" e as configurações.
from backend.services import pipeline_service
from backend.services.relatorio_service import RelatorioService
from backend.config import NOMES_PORTA_A_PORTA, NOMES_EXTERNA

# --- Instância Única do Serviço de Relatório ---
# Criamos nosso "Assistente de Pesquisa com Memória Fotográfica" aqui. Ele é criado apenas uma vez quando o servidor liga.
relatorio_service = RelatorioService()

# Cria o "caderno de pedidos" (Blueprint) para organizar as rotas.
views = Blueprint('views', __name__)


# --- ROTA DE PROCESSAMENTO ---
@views.route('/upload', methods=['POST'])
def upload_files():
    """
    Recebe os arquivos do frontend, salva-os e dispara o pipeline de processamento.
    """
    try:
        csv_file = request.files.get('csv')
        excel_file = request.files.get('excel')

        if not csv_file or not excel_file:
            return jsonify({'error': 'Arquivos não enviados'}), 400

        # Salva os arquivos enviados em uma pasta temporária.
        upload_folder = os.path.join(os.path.dirname(sys.argv[0]), 'uploads_app')
        os.makedirs(upload_folder, exist_ok=True)
        app.config['UPLOAD_FOLDER'] = upload_folder
        csv_path = os.path.join(upload_folder, secure_filename(csv_file.filename))
        excel_path = os.path.join(upload_folder, secure_filename(excel_file.filename))
        csv_file.save(csv_path)
        excel_file.save(excel_path)
        caminho_resultado = os.path.join(upload_folder, 'resultado.xlsx')

        # Chama o serviço de pipeline para fazer todo o trabalho pesado.
        pipeline_service.executar_pipeline_completo(csv_path, excel_path, caminho_resultado)

        # Manda nosso serviço de relatório carregar os novos dados na memória.
        relatorio_service.carregar_dados(caminho_resultado)

        return jsonify({'status': 'sucesso', 'mensagem': 'Arquivos processados com sucesso!'}), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'Ocorreu um erro no servidor: {e}'}), 500


# --- ROTA DE DOWNLOAD ---
@views.route('/download', methods=['GET'])
def download():
    """Fornece o arquivo de resultado para o usuário baixar."""
    caminho_arquivo = os.path.join(app.config.get('UPLOAD_FOLDER', ''), 'resultado.xlsx')
    if caminho_arquivo and os.path.exists(caminho_arquivo):
        return send_file(caminho_arquivo, as_attachment=True, download_name='resultado.xlsx')
    return jsonify({'error': 'Arquivo de resultado não encontrado.'}), 404


# --- ROTAS DE CONSULTA (AGORA SIMPLES E RÁPIDAS) ---
# Todas as rotas abaixo apenas pedem a informação para o nosso "Assistente de Pesquisa".

@views.route('/vendedores_tele', methods=['GET'])
def vendedores_tele():
    """Retorna os dados de vendas por vendedor de telemarketing."""
    dados = relatorio_service.obter_vendas_por_tele()
    return jsonify(dados)


@views.route('/vendedor_tele/<nome>', methods=['GET'])
def detalhes_vendedor(nome):
    """Retorna os detalhes de vendas de um vendedor de telemarketing específico."""
    dados = relatorio_service.obter_detalhes_vendedor_tele(nome)
    return jsonify(dados)


@views.route('/vendedores_porta_a_porta', methods=['GET'])
def vendedores_porta_a_porta():
    """Retorna os dados de vendas para vendedores porta a porta e externos."""
    dados = relatorio_service.obter_vendas_porta_a_porta() 
    return jsonify(dados)


@views.route('/vendedores_porta_a_porta/<nome>', methods=['GET'])
def detalhes_vendedor_porta_a_porta(nome):
    """Retorna os detalhes de vendas de um vendedor PaP específico."""
    dados = relatorio_service.obter_detalhes_vendedor_pap(nome)
    return jsonify(dados)
