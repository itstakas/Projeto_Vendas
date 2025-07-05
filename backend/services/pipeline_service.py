import pandas as pd
from ..processamento_de_dados.processador_vendas import ProcessadorVendas
from ..services.conciliador import ConciliadorVendas
from ..config import COLUNA_DATA_CONTRATO_EXCEL, COLUNA_DATA_ADESAO_EXCEL

def executar_pipeline_completo(csv_path: str, excel_path: str, caminho_saida: str):
    """
    Orquestra as grandes etapas do processamento de dados com depuração.
    """
    print("--- INICIANDO PIPELINE DE DADOS ---")

    # Estágio 1: Processamento
    processador = ProcessadorVendas(csv_path, excel_path)
    processador.executar()
    
    if processador.df_excel is None:
        print("ERRO: df_excel não foi criado pelo Processador.")
        return False
    
    # --- DEBUG PONTO 1 ---
    print("\n[DEBUG 1] Após o Processador.executar(), como está a coluna de data?")
    print("Primeiras 5 linhas da coluna DATA_CONTRATO:")
    print(processador.df_excel[COLUNA_DATA_CONTRATO_EXCEL.upper()].head())
    print(f"Tipo da coluna (dtype): {processador.df_excel[COLUNA_DATA_CONTRATO_EXCEL.upper()].dtype}\n")
    # ---------------------

    # Estágio 2: Conciliação
    conciliador = ConciliadorVendas(processador.df_excel, processador.df_csv)
    dataframe_final = conciliador.enriquecer_dados()

    # --- DEBUG PONTO 2 ---
    print("\n[DEBUG 2] Após o Conciliador.enriquecer_dados(), como está a coluna?")
    print("Primeiras 5 linhas da coluna DATA_CONTRATO:")
    print(dataframe_final[COLUNA_DATA_CONTRATO_EXCEL.upper()].head())
    print(f"Tipo da coluna (dtype): {dataframe_final[COLUNA_DATA_CONTRATO_EXCEL.upper()].dtype}\n")
    # ---------------------

    # --- ETAPA DE FORMATAÇÃO FINAL ---
    print("-> Formatando datas para o arquivo de saída...")
    colunas_de_data_final = [COLUNA_DATA_CONTRATO_EXCEL.upper(), COLUNA_DATA_ADESAO_EXCEL.upper()]
    
    for col in colunas_de_data_final:
        if col in dataframe_final.columns:
            # --- DEBUG PONTO 3 ---
            print(f"\n[DEBUG 3] Formatando a coluna '{col}'.")
            
            dataframe_final[col] = pd.to_datetime(dataframe_final[col], errors='coerce').dt.strftime('%d/%m/%Y').fillna('')
            
            # --- DEBUG PONTO 4 ---
            print(f"[DEBUG 4] Após a formatação, veja as primeiras 5 linhas da coluna '{col}':")
            print(dataframe_final[col].head(), "\n")

    # Estágio 3: Salvar o resultado
    try:
        dataframe_final.to_excel(caminho_saida, index=False, engine='xlsxwriter')
        print(f"--- PIPELINE CONCLUÍDO. Resultado salvo em: {caminho_saida} ---")
        return True
    except Exception as e:
        print(f"ERRO AO SALVAR O ARQUIVO EXCEL: {e}")
        return False