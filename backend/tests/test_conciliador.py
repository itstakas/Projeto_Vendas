# Testa a classe ConciliadorVendas


# Arquivo: tests/test_conciliador.py

import pandas as pd
import numpy as np  # Usamos numpy para valores nulos
from services.conciliador import ConciliadorVendas

# O nome da função de teste deve começar com "test_"
def test_conciliador_atualiza_cliente_existente_com_match_fuzzy():
    """
    Testa o cenário principal: um cliente com nome similar nos dois arquivos
    deve ter suas informações atualizadas no DataFrame final.
    """
    # 1. Arrange (Organizar): Criamos nossos DataFrames de teste "na mão".
    
    # DataFrame do Excel (entrada): Cliente com dados faltando.
    dados_excel = {
        'NOME': ['JOAO DA SILVA'],
        'DATA_CONTRATO': [pd.to_datetime('2025-01-15')],
        'CRM': [None],
        'VENDEDOR_TELE': [None],
        'CATEGORIA': [None],
        'SUBCATEGORIA': [None]
    }
    df_excel_input = pd.DataFrame(dados_excel)

    # DataFrame do CSV (fonte da verdade): Cliente com nome um pouco diferente e com os dados corretos.
    dados_csv = {
        'Id Cliente': ['JOAO SILVA'],
        'Unidade': ['TELEFONE-SP'],
        'Data de criação': ['Alguma Categoria'],
        'Origem (categoria)': ['Alguma Subcategoria']
    }
    df_csv_input = pd.DataFrame(dados_csv)

    # DataFrame Esperado (saída): Como o df_excel deve ficar APÓS a conciliação.
    dados_esperados = {
        'NOME': ['JOAO DA SILVA'],
        'DATA_CONTRATO': [pd.to_datetime('2025-01-15')],
        'CRM': ['JOAO SILVA'],  # <-- Esperamos que este campo seja preenchido
        'VENDEDOR_TELE': ['TELEFONE-SP'], # <-- Esperamos que este campo seja preenchido
        'CATEGORIA': ['Alguma Categoria'], # <-- Esperamos que este campo seja preenchido
        'SUBCATEGORIA': ['Alguma Subcategoria'] # <-- Esperamos que este campo seja preenchido
    }
    df_esperado = pd.DataFrame(dados_esperados)


    # 2. Act (Agir): Executamos a nossa classe com os dados de teste.
    conciliador = ConciliadorVendas(df_excel=df_excel_input, df_csv=df_csv_input)
    resultado_obtido = conciliador.enriquecer_dados()


    # 3. Assert (Afirmar/Verificar): Comparamos o DataFrame resultante com o nosso gabarito.
    # Usamos a função de teste do próprio pandas, que é feita para isso.
    # Ela dá erros muito mais detalhados se algo estiver diferente.
    pd.testing.assert_frame_equal(resultado_obtido, df_esperado)

