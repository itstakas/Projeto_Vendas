import pandas as pd
from routes.views import *
from datetime import datetime

def remover_colunas_denecessarias(df: pd.DataFrame) -> pd.DataFrame:

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

    return df.drop(columns=[col for col in colunas_para_remover if col in df.columns], errors='ignore')

def contratos_pagos_em_abril(df: pd.DataFrame) -> pd.DataFrame:

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
    if 'NOME' in df.columns:
        df = df[~df['NOME'].isin(apagar_nome)]

    return df



def filtrar_mes_atual(df):
    hoje = datetime.today()
    df['Responsável por indicar'] = pd.to_datetime(df['Responsável por indicar'], format='%d/%m/%Y', errors='coerce')
    df = df[
        (df['Responsável por indicar'].dt.month == hoje.month) &
        (df['Responsável por indicar'].dt.year == hoje.year)
    ]
    return df

def formatar_mes_atual(df):
        
    return df
   