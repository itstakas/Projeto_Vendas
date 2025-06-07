from flask import Blueprint, jsonify
from services.dados import get_clientes, get_vendedores

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/api/dashboard')
def dashboard_data():
    vendedores = get_vendedores()
    clientes = get_clientes()

    data = []
    for _, vendedor in vendedores.iterrows():
        nome = vendedor["nome"]
        qtd = clientes[clientes['vendedor_nome'] == nome].shape[0]
        lista_clientes = clientes[clientes['vendedor_nome'] == nome]['nome'].tolist()

        data.append({
            "vendedor": nome,
            "qtd_clientes": qtd,
            "clientes": lista_clientes
        })

    return jsonify(data)
