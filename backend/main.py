# Arquivo: backend/main.py

# Seus imports, mas agora vamos usar o 'send_from_directory' que é mais robusto
from flask import Flask, send_from_directory
from flask_cors import CORS
import os
import sys
import webbrowser
import time

# Importa o seu blueprint de rotas
from .routes.views import views

# --- LÓGICA DE CAMINHOS CORRIGIDA PARA O SERVIDOR ---

# Define a pasta onde o frontend "assado" (build) está.
# Esta forma é mais robusta em um servidor.
STATIC_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'dist'))

# Cria a aplicação Flask, mas agora dizemos a ela para NÃO gerenciar os arquivos estáticos automaticamente.
# Nós vamos fazer isso manualmente na rota principal para ter mais controle.
app = Flask(__name__, static_folder=None)

# Configuração final do CORS e das rotas
CORS(app)
app.register_blueprint(views)


# --- ROTA PRINCIPAL CORRIGIDA ---

# Esta rota agora vai lidar com a página inicial e todos os outros caminhos do frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    # Se o caminho existir dentro da nossa pasta de frontend, entrega o arquivo correspondente
    if path != "" and os.path.exists(os.path.join(STATIC_FOLDER, path)):
        return send_from_directory(STATIC_FOLDER, path)
    # Se não, ou se for a rota raiz, entrega o index.html (a porta de entrada do site)
    else:
        return send_from_directory(STATIC_FOLDER, 'index.html')


# Bloco que só roda quando a gente executa este arquivo diretamente no nosso PC
if __name__ == "__main__":
    url = "http://127.0.0.1:5000"
    print(f"Servidor Flask tentando iniciar em {url}...")
    
    # Esta parte de abrir o navegador não é necessária no servidor, mas não atrapalha.
    try:
        webbrowser.open_new(url)
    except Exception:
        print("Não foi possível abrir o navegador. Acesse a URL manualmente.")

    app.run(debug=False, host='127.0.0.1', port=5000)
