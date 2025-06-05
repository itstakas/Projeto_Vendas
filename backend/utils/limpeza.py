import pandas as pd
from routes.views import *
from datetime import datetime

def remover_colunas_denecessarias(df: pd.DataFrame) -> pd.DataFrame:
    #Lista de colunas que devem ser removidas, se existirem no DataFrame
    colunas_para_remover = [
        'DATA_CADASTRO',
        'ULTIMO_PAGAMENTO',
        'ULT_MES_REF_PAGO',
        'PAGOU',
        'EM_ATRASO',
        'DATA_CONFIRMACAO',
        'VALOR_CONFIRM',
        'ENDERECO_COB'
    ]

    # Remove as colunas que estiverem no DataFrame, ignorando erros caso alguma não exista
    return df.drop(columns=[col for col in colunas_para_remover if col in df.columns], errors='ignore')

def contratos_pagos_em_abril(df: pd.DataFrame) -> pd.DataFrame:
    # Conjunto de nomes a serem excluídos do DataFrame
    apagar_nome = {
            'DORALINA',
            'MARINALVA DE OLIVEIRA SOBRINHO',
            'JENIFER GABRIELLY DE ARAUJO REQUENA',
            'LUCIANA BRITES DO NASCIMENTO',
            'VILMA DE ARAUJOEPHANIE LOREN PUERTA COSME',
            'FELIPE TOMPOROSKI PEREZ',
            'JULIANA PIMENTEL MOLINA FIEL',
            'FABIANA DIAS BARROSO',
            'SILVIO ALEXANDRE LOPES FORTALEZA',
            'ROSENI MARTINS DOS SANTOS',
            'VILMAR PEREIRA DE JESUS',
            'KHISLEY MARESSA SILVA DIAS',
            'MARIA DE FÁTIMA RAMOS DA SILVA OLIVEIRA',
            'GEANNE DA SILVA BORGES',
            'SANDRA MARIA DA SILVA SANTOS',
            'MILCE FERREIRA DA COSTA',
            'THAÍS FONTANA DA CUNHA'
        }
    
    # Se a coluna 'NOME' existir, remove as linhas cujo nome esteja na lista de exclusão
    if 'NOME' in df.columns:
        df = df[~df['NOME'].isin(apagar_nome)]

    return df

# def filtrar_maio_2025(df):

#     # Obtém o mês e o ano atuais
#     mes_atual = datetime.now().month
#     ano_atual = datetime.now().year

#     # Converte a coluna 'Responsável por indicar' para datetime
#     df['Responsável por indicar'] = pd.to_datetime(df['Responsável por indicar'], format='%d/%m/%Y', errors='coerce')
    
#     # Filtra os registros que pertencem ao mês 05 (maio) e ano 2024
#     df = df[
#         (df['Responsável por indicar'].dt.month == mes_atual) &
#         (df['Responsável por indicar'].dt.year == ano_atual)
#     ]
#     return df

# Função que filtra os dados do DataFrame apenas para o mês atual
def filtrar_mes_atual(df):
    # Obtém a data atual
    hoje = datetime.today()
    # Converte a coluna 'Responsável por indicar' para datetime
    df['Responsável por indicar'] = pd.to_datetime(df['Responsável por indicar'], format='%d/%m/%Y', errors='coerce')
    
    # Filtra os registros que pertencem ao mês e ano atuais
    df = df[
        (df['Responsável por indicar'].dt.month == hoje.month) &
        (df['Responsável por indicar'].dt.year == hoje.year)
    ]
    return df
