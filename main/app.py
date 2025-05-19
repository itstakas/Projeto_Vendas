from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app) #habilita o cors e permite requisições no front

#config para upload de arquivos, ainda opcional
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


