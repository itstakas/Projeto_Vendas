from flask import Flask
from flask_cors import CORS
import os

def create_app():

    app = Flask(__name__)
    CORS(app)  # Habilita CORS para a aplicação (libera o acesso entre domínios, essencial para o front-end se comunicar com a API)

    # config de uploads
    UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'uploads'))
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    from routes.views import views_bp
    from routes.api import api_bp

    app.register_blueprint(api_bp)
    app.register_blueprint(views_bp)

    return app

# Inicia o servidor Flask em modo debug (para ver erros no terminal)
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
