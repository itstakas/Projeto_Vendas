# Este arquivo contém pequenas "ferramentas" de formatação que podem ser
# Usadas em qualquer parte do projeto.

import pandas as pd
from datetime import datetime

def corrigir_data_inteligentemente(data_str: str) -> pd.Timestamp:
    """
    Esta é a nossa função "inteligente" para consertar datas. Ela recebe um texto e tenta, de várias formas, transformá-lo em uma data correta. Sua principal regra é consertar datas ambíguas (ex: 05/07/2025 vs 07/05/2025).
    """
    # 1. Primeira verificação: se a célula estiver vazia, não faz nada.
    if pd.isna(data_str):
        return pd.NaT # Retorna um valor de "data não existente".
    
    # 2. Limpeza inicial: remove a parte da hora, se houver (ex: '2025-07-05 00:00:00').
    data_str = str(data_str).split(' ')[0]

    # --- TENTATIVA 1: Formato Americano/Padrão (AAAA-MM-DD) ---
    # O 'try' tenta executar um código que pode dar erro.
    try:
        # "Fatia" o texto para pegar os pedaços do ano, mês e dia.
        ano = int(data_str[0:4])
        possivel_mes = int(data_str[5:7])
        possivel_dia = int(data_str[8:10])

        # A REGRA DE NEGÓCIO: se tanto o dia quanto o mês forem 12 ou menos, a data é "ambígua".
        if possivel_dia <= 12 and possivel_mes <= 12:
            # Se for ambígua, consideramos que o dia e o mês foram digitados ao contrário. Aqui, nós forçamos a inversão: o que parecia ser o dia vira o mês, e vice-versa.
            data_correta = datetime(year=ano, month=possivel_dia, day=possivel_mes)
            return pd.to_datetime(data_correta)
        else:
            # Se não for ambígua (ex: dia 25), confiamos no formato original.
            return pd.to_datetime(data_str, format='%Y-%m-%d')

    # O 'except' só é executado se o código dentro do 'try' falhou.
    except (ValueError, TypeError, IndexError):
        # Se a Tentativa 1 falhou, o texto não estava no formato AAAA-MM-DD.
        # --- TENTATIVA 2: Formato Brasileiro (DD/MM/AAAA) ---
        try:
            # Tenta ler o texto como uma data no formato brasileiro.
            return pd.to_datetime(data_str, format='%d/%m/%Y')
        except (ValueError, TypeError):
            # Se todas as tentativas falharem, a função desiste. Retorna um valor de "data não existente".
            return pd.NaT
