# backend/main.py

from flask import Flask
from flask_cors import CORS
import os
import sys

# --- INÍCIO: AJUSTES DE PATH CRUCIAIS PARA IMPORTAÇÕES E PYINSTALLER ---
# Obtém o caminho do diretório onde main.py está (ex: .../Projeto_Vendas/backend)
current_script_dir = os.path.dirname(os.path.abspath(__file__))

# Sobe um nível para chegar na raiz do projeto (ex: .../Projeto_Vendas)
project_root_path = os.path.abspath(os.path.join(current_script_dir, '..'))

# Adiciona o diretório raiz do projeto ao sys.path.
# Isso permite que Python encontre pacotes como 'backend' se o import fosse 'from backend.routes import views'.
if project_root_path not in sys.path:
    sys.path.append(project_root_path)

# Adiciona o próprio diretório 'backend' ao sys.path.
# ISSO É CRÍTICO para que 'from routes.views import views' funcione,
# pois 'routes' é uma subpasta direta de 'backend'.
if current_script_dir not in sys.path:
    sys.path.append(current_script_dir)
# --- FIM: AJUSTES DE PATH CRUCIAIS ---

# Define o caminho para a pasta 'dist' do frontend construído.
# Usa o 'project_root_path' para garantir que o caminho seja sempre relativo à raiz do projeto,
# o que funciona bem com o '--add-data' do PyInstaller.
FRONTEND_DIST_PATH = os.path.join(project_root_path, 'frontend', 'dist')

# Inicializa a aplicação Flask.
# Configura 'static_folder' para apontar para a pasta 'dist' do frontend,
# e 'static_url_path' como '/' para servir o frontend na raiz do servidor.
app = Flask(__name__,
            static_folder=FRONTEND_DIST_PATH,
            static_url_path='/')

# Habilita CORS para permitir comunicação entre o frontend (Vue.js) e o backend (Flask).
# Essencial para desenvolvimento e deployments onde frontend e backend estão em portas/domínios diferentes.
CORS(app)

# Importa o blueprint 'views' que contém todas as suas rotas da API.
# Este import deve funcionar agora devido aos ajustes no sys.path acima.
from routes.views import views

# Registra o blueprint 'views' na aplicação Flask.
app.register_blueprint(views)

# Rota principal que serve o arquivo index.html do frontend.
# Quando o usuário acessa a raiz do seu aplicativo (ex: http://localhost:5000/),
# esta rota é responsável por enviar o arquivo principal do frontend.
@app.route('/')
def serve_index():
    return app.send_static_file('index.html')

# Bloco principal de execução do servidor Flask.
# Isso garante que o servidor só inicie quando o script é executado diretamente.
if __name__ == "__main__":
    # Inicia o servidor Flask.
    # 'debug=True' é útil para desenvolvimento (recarga automática e mensagens de erro detalhadas).
    # 'host='127.0.0.1'' e 'port=5000' definem o endereço e a porta do servidor.
    app.run(debug=True, host='127.0.0.1', port=5000)