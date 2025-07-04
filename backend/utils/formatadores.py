import pandas as pd
from datetime import datetime
# NOTE QUE NÃO HÁ NENHUMA OUTRA LINHA DE 'import' AQUI

def corrigir_data_inteligentemente(data_str: str) -> pd.Timestamp:
    """
    Corrige uma string de data, lidando com múltiplos formatos e uma
    regra de negócio para datas ambíguas (onde dia e mês podem estar invertidos).
    """
    # 1. Tratamento de valores vazios ou nulos
    if pd.isna(data_str):
        return pd.NaT
    
    # 2. Limpeza inicial da string para remover horas
    data_str = str(data_str).split(' ')[0]

    # --- TENTATIVA 1: Formato ISO (YYYY-MM-DD) ---
    try:
        # Fatiamento da string para extrair ano, mês e dia
        ano = int(data_str[0:4])
        possivel_mes = int(data_str[5:7])
        possivel_dia = int(data_str[8:10])

        # Lógica de negócio para datas ambíguas
        if possivel_dia <= 12 and possivel_mes <= 12:
            # Se AMBOS podem ser mês, consideramos que estão invertidos
            data_correta = datetime(year=ano, month=possivel_dia, day=possivel_mes)
            return pd.to_datetime(data_correta)
        else:
            # Se não for ambíguo, confiamos no formato original
            return pd.to_datetime(data_str, format='%Y-%m-%d')

    except (ValueError, TypeError, IndexError):
        # Se a TENTATIVA 1 falhou, o formato não era YYYY-MM-DD.
        # --- TENTATIVA 2: Formato Brasileiro (DD/MM/YYYY) ---
        try:
            return pd.to_datetime(data_str, format='%d/%m/%Y')
        except (ValueError, TypeError):
            # Se todas as tentativas falharem, retorna o valor nulo de data.
            return pd.NaT