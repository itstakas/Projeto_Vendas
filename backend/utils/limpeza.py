import pandas as pd
from datetime import datetime


def remover_colunas_desnecessarias(df: pd.DataFrame) -> pd.DataFrame:
    """Remove colunas irrelevantes se existirem."""
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


def remover_clientes_excluidos(df: pd.DataFrame) -> pd.DataFrame:
    """Remove registros de clientes que não devem ser considerados."""
    nomes_excluir = {
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
        'THAÍS FONTANA DA CUNHA',
        'GISLAINE LOPES DA SILVA',
        'LUCAS HENRIQUE',
        'SÔNIA GREFFE CHAVES'
    }

    if 'NOME' in df.columns:
        return df[~df['NOME'].isin(nomes_excluir)]
    return df


def filtrar_mes_atual(df: pd.DataFrame) -> pd.DataFrame:
    """Filtra registros pela coluna 'Responsável por indicar' no mês atual."""
    if 'Responsável por indicar' not in df.columns:
        return df

    hoje = datetime.today()
    df['Responsável por indicar'] = pd.to_datetime(
        df['Responsável por indicar'], format='%d/%m/%Y', errors='coerce'
    )
    return df[
        (df['Responsável por indicar'].dt.month == hoje.month) &
        (df['Responsável por indicar'].dt.year == hoje.year)
    ]
