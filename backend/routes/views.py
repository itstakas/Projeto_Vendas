from main import app
from flask import request, jsonify
from werkzeug.utils import secure_filename
from controladores.Classes import ProcessaDados
from controladores.comparador import comparar_e_preencher
import pandas as pd
from flask import send_file, abort
import uuid
import os
from utils.limpeza import remover_colunas_denecessarias, contratos_pagos_em_abril


@app.route("/")
def hello_world():
    return 'Olá, backend do Flask'


@app.route('/upload', methods=["POST"])
def upload_files():
    # Verificação inicial dos arquivos
    if 'csv' not in request.files or 'excel' not in request.files:
        return jsonify({'error': 'Nenhum arquivo CSV ou Excel foi enviado'}), 400
    
    csv_file = request.files['csv']
    excel_file = request.files['excel']
    
    if csv_file.filename == '' or excel_file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400

    # Verificação de extensões
    if not (csv_file.filename.lower().endswith('.csv') and 
            excel_file.filename.lower().endswith(('.xls', '.xlsx'))):
        return jsonify({'error': 'Formatos de arquivo inválidos. Esperado: CSV e Excel'}), 400

    try:
        # Criar diretório seguro para processamento
        process_id = str(uuid.uuid4())
        temp_dir = os.path.join(app.config['UPLOAD_FOLDER'], process_id)
        os.makedirs(temp_dir, exist_ok=True)

        # Salvar arquivos com nomes seguros
        csv_path = os.path.join(temp_dir, secure_filename(csv_file.filename))
        excel_path = os.path.join(temp_dir, secure_filename(excel_file.filename))
        csv_file.save(csv_path)
        excel_file.save(excel_path)

        # Processamento principal
        try:
            processador = ProcessaDados(csv_path, excel_path)
            processador = comparar_e_preencher(processador)
            
            # Aplicar transformações
            processador.excel_df = remover_colunas_denecessarias(processador.excel_df)
            processador.excel_df = contratos_pagos_em_abril(processador.excel_df)
            
            # Gerar arquivo de saída
            output_filename = f'Fechamento_preenchido_{process_id}.xlsx'
            caminho_saida = os.path.join(temp_dir, output_filename)
            processador.salvar_excel_preenchido(caminho_saida)
            
            # Mover arquivo final para área pública de download
            final_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            os.rename(caminho_saida, final_path)
            
            return jsonify({
                'message': 'Processamento concluído com sucesso',
                'arquivo_gerado': True,
                'download_id': process_id
            })
            
        except pd.errors.EmptyDataError:
            abort(400, description="Arquivo CSV ou Excel está vazio")
        except KeyError as e:
            abort(400, description=f"Coluna obrigatória não encontrada: {str(e)}")
        except Exception as e:
            app.logger.error(f"Erro no processamento: {str(e)}", exc_info=True)
            abort(500, description="Erro durante o processamento dos dados")
            
    except Exception as e:
        app.logger.error(f"Erro no upload: {str(e)}", exc_info=True)
        return jsonify({'error': 'Erro interno no servidor'}), 500
        
    finally:
        # Limpeza dos arquivos temporários
        try:
            if 'temp_dir' in locals():
                for filename in os.listdir(temp_dir):
                    file_path = os.path.join(temp_dir, filename)
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                os.rmdir(temp_dir)
        except Exception as e:
            app.logger.error(f"Erro na limpeza: {str(e)}")


@app.route("/download/<string:file_id>", methods=["GET"])
def download_excel(file_id):
    filename = f'Fechamento_preenchido_{file_id}.xlsx'
    caminho_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(caminho_arquivo):
        return jsonify({'error': 'Arquivo não encontrado ou expirado'}), 404
        
    try:
        return send_file(
            caminho_arquivo,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='Fechamento_preenchido.xlsx'
        )
    except Exception as e:
        app.logger.error(f"Erro no download: {str(e)}")
        return jsonify({'error': 'Erro ao enviar arquivo'}), 500
