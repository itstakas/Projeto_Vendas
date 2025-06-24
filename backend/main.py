# backend/main.py

from flask import Flask
from flask_cors import CORS
import os
import sys
import webbrowser
import time # Adicione para a pausa

# --- INÍCIO: AJUSTES DE PATH CRUCIAIS PARA IMPORTAÇÕES E PYINSTALLER ---
current_script_dir = os.path.dirname(os.path.abspath(__file__))
project_root_path = os.path.abspath(os.path.join(current_script_dir, '..'))

if project_root_path not in sys.path:
    sys.path.append(project_root_path)

if current_script_dir not in sys.path:
    sys.path.append(current_script_dir)
# --- FIM: AJUSTES DE PATH CRUCIAIS ---

# --- NOVO AJUSTE: CAMINHO DA PASTA ESTÁTICA PARA O FLASK ---
# Define o caminho para a pasta 'dist' do frontend construído,
# adaptando para ambiente de desenvolvimento ou executável PyInstaller.
if getattr(sys, 'frozen', False): # Se estiver rodando como executável PyInstaller
    # Quando empacotado, 'frontend/dist' é o subdiretório dentro do sys._MEIPASS (o diretório temporário)
    FRONTEND_DIST_PATH = os.path.join(sys._MEIPASS, 'frontend', 'dist')
else:
    # Em ambiente de desenvolvimento, o caminho é relativo à raiz do projeto
    FRONTEND_DIST_PATH = os.path.join(project_root_path, 'frontend', 'dist')
# --- FIM NOVO AJUSTE ---


# Inicializa a aplicação Flask.
app = Flask(__name__,
            static_folder=FRONTEND_DIST_PATH,
            static_url_path='/')

CORS(app)

from routes.views import views

app.register_blueprint(views)

@app.route('/')
def serve_index():
    # Flask automaticamente procura por index.html no static_folder
    # e o serve para static_url_path='/'
    return app.send_static_file('index.html')

if __name__ == "__main__":
    url = "http://127.0.0.1:5000"

    # Inicia o Flask em uma thread separada ou com Waitress para não bloquear o navegador.
    # Para um único executável e PyInstaller, o mais simples é dar uma pequena pausa.
    # O Flask com debug=True já possui um reloader que pode causar problemas se não houver delay.
    # Vamos aumentar a pausa para garantir que o Flask esteja de pé.
    print(f"Servidor Flask tentando iniciar em {url}. Aguardando 3 segundos para abrir o navegador...")
    time.sleep(3) # Aumentar a pausa

    webbrowser.open_new(url)

    # O app.run com debug=True já gerencia o servidor.
    app.run(debug=True, host='127.0.0.1', port=5000)