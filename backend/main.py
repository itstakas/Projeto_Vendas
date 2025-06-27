from .routes.views import views
from flask import Flask
from flask_cors import CORS
import os
import sys
import webbrowser                   # Ferramenta para abrir o navegador
import time                         # Ferramenta para dar pausas (esperar)


if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
    # o site (frontend) vai estar DENTRO dessa pasta temporária.
    FRONTEND_DIST_PATH = os.path.join(application_path, 'frontend', 'dist')
else:
    # o "endereço da garagem" (__file__) para se localizar.
    application_path = os.path.dirname(os.path.abspath(__file__))
    # E para achar o site, ele volta um nível ('..') e entra na pasta 'frontend/dist'.
    FRONTEND_DIST_PATH = os.path.join(
        application_path, '..', 'frontend', 'dist')


project_root = os.path.abspath(os.path.join(application_path, '..'))
if project_root not in sys.path:
    sys.path.append(project_root)


app = Flask(__name__,
            # A parte visual do site (HTML, CSS) está NESTA pasta.
            static_folder=FRONTEND_DIST_PATH,
            # Quando alguém acessar o site, a URL principal ('/') corresponde a essa pasta.
            static_url_path='/')

CORS(app)

app.register_blueprint(views)


@app.route('/')
def serve_index():
    # entrega a "porta de entrada" do site, o arquivo index.html.
    return app.send_static_file('index.html')


# Este bloco só roda quando executa este arquivo 'main.py' diretamente.
if __name__ == "__main__":
    url = "http://127.0.0.1:5000"
    print(f"Servidor Flask tentando iniciar em {url}. Aguardando 3 segundos para abrir o navegador...")
    time.sleep(3)

    # Abre o site automaticamente
    webbrowser.open_new(url)

    app.run(debug=False, host='127.0.0.1', port=5000)
