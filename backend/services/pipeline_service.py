# Este serviço contém o fluxo completo de processamento, agindo como o "Gerente da Fábrica" que comanda as outras classes.

import pandas as pd

# O gerente conhece seus "chefes de setor": o Processador e o Conciliador.
from backend.processamento_de_dados.processador_vendas import ProcessadorVendas
from backend.services.conciliador import ConciliadorVendas
# Puxa as configurações de nomes de colunas para a etapa final de formatação.
from backend.config import COLUNA_DATA_CONTRATO_EXCEL, COLUNA_DATA_ADESAO_EXCEL


def executar_pipeline_completo(csv_path: str, excel_path: str, caminho_saida: str):
    """
    Orquestra as grandes etapas do processamento de dados, delegando o trabalho pesado para as classes de serviço.
    """
    print("--- INICIANDO PIPELINE DE DADOS ---")

    # --- ESTÁGIO 1: O "Chef" prepara os dados ---
    # Cria uma instância do Processador e manda ele executar toda a sua "receita" de limpeza.
    processador = ProcessadorVendas(csv_path, excel_path)
    processador.executar()
    
    # Verificação de segurança para garantir que a primeira etapa funcionou.
    if processador.df_excel is None or processador.df_csv is None:
        print("ERRO: Falha no estágio de processamento inicial. Pipeline abortado.")
        return False

    # --- ESTÁGIO 2: O "Detetive" faz a conciliação ---
    # Pega os dados já limpos pelo Processador e entrega para o Conciliador fazer o cruzamento.
    conciliador = ConciliadorVendas(processador.df_excel, processador.df_csv)
    dataframe_final = conciliador.enriquecer_dados()

    # --- ETAPA DE FORMATAÇÃO FINAL ---
    # Antes de salvar, garantimos que as colunas de data fiquem no formato DD/MM/YYYY.
    print("-> Formatando datas para o arquivo de saída...")
    colunas_de_data_final = [COLUNA_DATA_CONTRATO_EXCEL.upper(), COLUNA_DATA_ADESAO_EXCEL.upper()]
    
    for col in colunas_de_data_final:
        if col in dataframe_final.columns:
            # Força a conversão para data e depois para texto no formato desejado.
            dataframe_final[col] = pd.to_datetime(dataframe_final[col], errors='coerce').dt.strftime('%d/%m/%Y').fillna('')

    # --- ESTÁGIO 3: O Pipeline salva o resultado final ---
    try:
        dataframe_final.to_excel(caminho_saida, index=False, engine='xlsxwriter')
        print(f"--- PIPELINE CONCLUÍDO. Resultado salvo em: {caminho_saida} ---")
        return True
    except Exception as e:
        print(f"ERRO AO SALVAR O ARQUIVO EXCEL: {e}")
        return False
