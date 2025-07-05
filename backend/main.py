# Arquivo: backend/main.py
# Este é o arquivo principal que liga e roda o servidor.

# --- Importações ---
# Aqui, nós "puxamos" as ferramentas que o programa precisa para funcionar.
from flask import Flask, send_from_directory
from flask_cors import CORS
import os
import webbrowser

# Puxa todas as nossas "páginas" da API, que estão definidas em outro arquivo.
from backend.routes.views import views


# --- Configuração da Aplicação ---
# Nesta parte, nós preparamos e configuramos o nosso programa.

# Diz ao programa onde encontrar a pasta com os arquivos do site (o frontend).
STATIC_FOLDER = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'frontend', 'dist'))

# Cria o nosso "servidor" web usando a ferramenta Flask.
app = Flask(__name__, static_folder=None)

# Permite que o site (frontend) possa conversar com este programa (backend) sem erros.
CORS(app)

# Avisa ao servidor sobre todas as páginas da API que importamos.
app.register_blueprint(views)


# --- Rota para Servir o Frontend ---
# Esta parte é responsável por entregar o seu site para o navegador do usuário.

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    """
    Esta rota "pega-tudo" serve o site. Se o navegador pede um arquivo (como uma imagem), ela entrega o arquivo. Se pede uma página (como /vendedores), ela entrega a "casca" do site (index.html) para o Vue.js poder trabalhar.
    """
    # Se o que o navegador pediu for um arquivo de verdade (CSS, JS, imagem)...
    if path != "" and os.path.exists(os.path.join(STATIC_FOLDER, path)):
        # ...entrega esse arquivo.
        return send_from_directory(STATIC_FOLDER, path)
    # Se não, entrega a página principal do site.
    else:
        return send_from_directory(STATIC_FOLDER, 'index.html')


# --- Bloco de Execução Principal ---
# O código aqui só roda quando você executa "python -m backend.main" no terminal.
if __name__ == "__main__":
    url = "http://127.0.0.1:5000"
    print(f"Servidor ligando no endereço: {url}")

    # Tenta abrir o site no navegador automaticamente para facilitar.
    try:
        webbrowser.open_new(url)
    except Exception:
        print("Não consegui abrir o navegador. Pode abrir manualmente.")

    # Liga o servidor e o deixa rodando para receber "visitas" (requisições).
    app.run(debug=False, host='127.0.0.1', port=5000)
