# Arquivo: backend/main.py

# Importações básicas do Flask e CORS para permitir comunicação com o frontend
from flask import Flask, send_from_directory
from flask_cors import CORS
import os
import sys
import webbrowser
import time

# Importa minhas rotas definidas separadamente no blueprint
from backend.routes.views import views

# --- CONFIGURAÇÃO DO FRONTEND ---

# Aqui eu defino a pasta onde o Vue gera os arquivos finais após o build. Isso garante que o Flask saiba onde está o frontend "compilado".
STATIC_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'dist'))

# Crio a aplicação Flask sem o gerenciador automático de arquivos estáticos,porque quero controlar isso manualmente com mais precisão.
app = Flask(__name__, static_folder=None)

# Ativo o CORS para evitar problemas de comunicação entre frontend e backend
CORS(app)

# Registro o blueprint onde estão as rotas da minha API
app.register_blueprint(views)

# --- ROTA PARA SERVIR O FRONTEND ---

# Essa rota cuida de todas as requisições do frontend SPA (Single Page Application) Se o caminho requisitado for um arquivo existente (ex: /assets/logo.png), ele será servido Caso contrário (ex: /vendedores), ele carrega o index.html para o Vue assumir a navegação
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(STATIC_FOLDER, path)):
        return send_from_directory(STATIC_FOLDER, path)
    else:
        return send_from_directory(STATIC_FOLDER, 'index.html')

# --- EXECUÇÃO LOCAL ---

# Essa parte só roda se eu executar o main.py diretamente Serve para iniciar o servidor localmente e abrir o navegador automaticamente
if __name__ == "__main__":
    url = "http://127.0.0.1:5000"
    print(f"Servidor Flask tentando iniciar em {url}...")

    try:
        webbrowser.open_new(url)
    except Exception:
        print("Não foi possível abrir o navegador. Acesse a URL manualmente.")

    # Inicia o servidor Flask na porta 5000
    app.run(debug=False, host='127.0.0.1', port=5000)
