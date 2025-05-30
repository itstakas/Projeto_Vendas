from flask import Flask
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Habilita CORS para a aplicação (libera o acesso entre domínios, essencial para o front-end se comunicar com a API)

from routes.views import *

# Define o caminho absoluto da pasta de uploads, criando o caminho a partir do diretório atual (__file__)
UPLOAD_FOLDER = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'uploads'))
# Verifica se a pasta de uploads existe; se não, cria ela
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
# Configura a aplicação para reconhecer o caminho de upload de arquivos
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Inicia o servidor Flask em modo debug (para ver erros no terminal)
if __name__ == "__main__":
    app.run(debug=True)
