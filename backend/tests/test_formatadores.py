
import pandas as pd

# Importamos a função que queremos testar 
from utils.formatadores import corrigir_data_inteligentemente

def test_corrite_data_formato_brasileiro_com_sucesso(): #IMPORTANTE! O nome da função deve começar com "test"
    """
    Testa se a função converte corretamente a data para o formato DD/MM/YYYY
    """

    # Padrão AAA (Arrange, Act, Assert)

    data_input = "04/07/2025" #Arrange (organizar)
    data_esperada = pd.Timestamp("2025-07-04") 

    resultado_obtido = corrigir_data_inteligentemente(data_input) #Act (Agir)

    assert resultado_obtido == data_esperada #Assert (Verificar/afirmar)


def test_corrige_data_formato_iso_nao_ambiguo():
    """
    Testa se a função converte corretamente uma data no formato YYYY-MM-DD quando NÃO HÁ ambiguidade (dia > 12)
    """

    # Arrange (organizar)
    data_input = "2025-03-21"
    data_esperada = pd.Timestamp("2025-03-21")

    # Act (Agir)
    resultado_obtido = corrigir_data_inteligentemente(data_input)

    # Assert (Correção/Verificação)
    assert resultado_obtido == data_esperada

def test_corrige_data_formato_iso_ambiguo_e_inverte():
    """
    Testa a regra de negocio principal: Uma data ambigua (dia e mes <= 12) no formato YYYY-MM-DD deve ter o dia e o mes invertidos
    """

    # Arrange
    data_input = "2025-05-07" # A entrada é 7 de Maio de 2025
    data_esperada = pd.Timestamp("2025-07-05") # O resultado esperado é 5 de Julho de 2025, pois o dia (07) vira o mês e o mês (05) vira o dia.

    resultado_obtido = corrigir_data_inteligentemente(data_input)

    assert resultado_obtido == data_esperada

def test_verifica_string():

    data_input = "Takeshi lindo"
    resultado_obtido = corrigir_data_inteligentemente(data_input)

    assert pd.isna(resultado_obtido)

def test_data_nula():

    data_input = " "
    resultado_obtido = corrigir_data_inteligentemente(data_input)

    assert pd.isna(resultado_obtido)