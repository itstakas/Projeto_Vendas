from flask import Flask
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # habilita o cors e permite requisições no front

from views import *

# config para upload de arquivos na pasta uploads
UPLOAD_FOLDER = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'uploads'))
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if __name__ == "__main__":
    app.run(debug=True)
