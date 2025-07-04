import pandas as pd
from datetime import datetime

def corrigir_data_inteligentemente(data_str: str) -> pd.Timestamp:
    """
        Corrige uma string de data tentando múltiplos formatos e aplicando uma regra de negocio para datas ambíguas (onde dia e mes podem estar invertidos), exemplo: data correta: 05/06/2025, data no arquivo 06/05/2025

        Args:
            data_str: A data em formato de string a ser corrigida
        Returns:
            Um objeto de data (Timestamp) ou NaT (NOT A TIME) se a conversão falhar
    """

    # Se a celular estiver vazia ou for nula, retorna um valor nulo de data
    if pd.isna(data_str):
        return pd.NaT
    
    # Pega apenas a parte da data, ignorando horas (ex: '2025-03-06 00:00:00')
    data_str = str(data_str).split(' ')[0]

    try:
        # O fatiamento é usado para pegar "pedaços" de uma string, a contafem de posições(indice) começa em 0, por exemplo a data: '2025-03-06'
        # caractere: 2 0 2 5 - 0 3 - 0 6
        # indice:    0 1 2 3 4 5 6 7 8 9

        ano = int(data_str[0:4])
        possivel_mes = int(data_str[5:7])
        possivel_dia = int(data_str[8:10])

        if possivel_dia <= 12 and possivel_mes <= 12: 
            # É ambiguo e converte para o formato brasileiro de dia/mes/ano
            data_correta = datetime(year=ano, month=possivel_dia, day=possivel_mes)

            return pd.to_datetime(data_correta)
        else:
            # Não é ambíguo, confia no formato original
            return pd.to_datetime(data_str, format='%Y-%m-%d')
    except (ValueError, TypeError, IndexError): #Se falhar é formato brasileiro
        try:
            return pd.to_datetime(data_str, format='%d/%m/%Y')
        except:
            return pd.NaT #Se mesmo assim tudo falhar, retorna como NaT

