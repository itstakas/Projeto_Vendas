import pandas as pd

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
