# Este arquivo contém todos os testes para a nossa função inteligente de corrigir datas.

import pandas as pd
# Importamos a função que queremos testar a partir de sua localização no projeto.
from backend.utils.formatadores import corrigir_data_inteligentemente

def test_corrige_data_formato_brasileiro_com_sucesso():
    """
    Testa o "caminho feliz": verifica se uma data no formato brasileiro (DD/MM/AAAA) é convertida corretamente.
    """
    # 1. Organizar (Arrange)
    data_de_teste = "04/07/2025"
    resultado_esperado = pd.Timestamp("2025-07-04") 

    # 2. Agir (Act)
    resultado_obtido = corrigir_data_inteligentemente(data_de_teste)

    # 3. Afirmar (Assert)
    assert resultado_obtido == resultado_esperado


def test_corrige_data_formato_iso_nao_ambiguo():
    """
    Testa uma data no formato padrão (AAAA-MM-DD) onde não há dúvida de qual número é o dia e qual é o mês (porque o dia é > 12).
    """
    # 1. Organizar
    data_de_teste = "2025-03-21"
    resultado_esperado = pd.Timestamp("2025-03-21")

    # 2. Agir
    resultado_obtido = corrigir_data_inteligentemente(data_de_teste)

    # 3. Afirmar
    assert resultado_obtido == resultado_esperado


def test_corrige_data_formato_iso_ambiguo_e_inverte():
    """
    Testa a regra de negócio mais importante: uma data ambígua (dia e mês <= 12) deve ter o dia e o mês invertidos para corrigir o erro comum de digitação.
    """
    # 1. Organizar
    # A entrada é 7 de Maio de 2025, no formato AAAA-MM-DD.
    data_de_teste = "2025-05-07"
    # O resultado esperado é 5 de Julho de 2025, pois a função deve inverter dia e mês.
    resultado_esperado = pd.Timestamp("2025-07-05")

    # 2. Agir
    resultado_obtido = corrigir_data_inteligentemente(data_de_teste)

    # 3. Afirmar
    assert resultado_obtido == resultado_esperado


def test_retorna_nat_para_string_invalida():
    """
    Testa o "caminho triste": verifica se a função retorna um valor nulo (NaT) quando recebe um texto que não é uma data.
    """
    # 1. Organizar
    data_de_teste = "Takeshi lindo"
    
    # 2. Agir
    resultado_obtido = corrigir_data_inteligentemente(data_de_teste)

    # 3. Afirmar
    # pd.isna() é a forma correta de verificar se um valor é nulo no pandas.
    assert pd.isna(resultado_obtido)


def test_retorna_nat_para_data_nula_ou_vazia():
    """
    Testa outro "caminho triste": verifica se a função lida corretamente com entradas que são nulas ou apenas um espaço em branco.
    """
    # 1. Organizar
    data_de_teste = " "
    
    # 2. Agir
    resultado_obtido = corrigir_data_inteligentemente(data_de_teste)

    # 3. Afirmar
    assert pd.isna(resultado_obtido)
