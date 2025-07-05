# Este arquivo testa a lógica da classe ConciliadorVendas.

import pandas as pd
# Importamos a classe que queremos testar.
from backend.services.conciliador import ConciliadorVendas

def test_conciliador_atualiza_cliente_existente_com_match_fuzzy():
    """
    Testa o cenário principal: um cliente com nome similar nos dois arquivos deve ter suas informações atualizadas no DataFrame final.
    """
    # --- 1. Arrange (Organizar) ---
    # Criamos nossos DataFrames de teste "na mão", em memória. Não usamos arquivos reais para que o teste seja rápido e independente.
    
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
    # Este é o nosso "gabarito".
    dados_esperados = {
        'NOME': ['JOAO DA SILVA'],
        'DATA_CONTRATO': [pd.to_datetime('2025-01-15')],
        'CRM': ['JOAO SILVA'],  # <-- Esperamos que este campo seja preenchido
        'VENDEDOR_TELE': ['TELEFONE-SP'], # <-- Esperamos que este campo seja preenchido
        'CATEGORIA': ['Alguma Categoria'], # <-- Esperamos que este campo seja preenchido
        'SUBCATEGORIA': ['Alguma Subcategoria'] # <-- Esperamos que este campo seja preenchido
    }
    df_esperado = pd.DataFrame(dados_esperados)


    # --- 2. Act (Agir) ---
    # Executamos a nossa classe com os dados de teste.
    conciliador = ConciliadorVendas(df_excel=df_excel_input, df_csv=df_csv_input)
    resultado_obtido = conciliador.enriquecer_dados()


    # --- 3. Assert (Afirmar/Verificar) ---
    # Comparamos o DataFrame resultante com o nosso gabarito. A função `assert_frame_equal` do pandas é a forma profissional de fazer isso. Ela verifica se as colunas, os dados e os tipos são idênticos.
    pd.testing.assert_frame_equal(resultado_obtido, df_esperado)
