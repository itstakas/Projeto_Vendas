# Arquivo: services/pipeline_service.py
# Este serviço contém o fluxo completo de processamento,
# agindo como o "Gerente da Fábrica".

# O gerente só precisa conhecer seus "chefes de setor".
from ..processamento_de_dados.processador_vendas import ProcessadorVendas
from .conciliador import ConciliadorVendas

def executar_pipeline_completo(csv_path: str, excel_path: str, caminho_saida: str):
    """
    Orquestra as grandes etapas do processamento de dados,
    delegando o trabalho pesado para as classes de serviço.
    """
    print("--- INICIANDO PIPELINE DE DADOS ---")

    # --- ESTÁGIO 1: O "Chef" faz todo o trabalho de preparação e limpeza. ---
    # Uma única chamada para executar todas as etapas de processamento.
    processador = ProcessadorVendas(csv_path, excel_path)
    processador.executar()
    
    # Verificação de segurança para garantir que a primeira etapa funcionou
    if processador.df_excel is None or processador.df_csv is None:
        print("ERRO: Falha no estágio de processamento inicial. Pipeline abortado.")
        # Retornar False pode ajudar a rota da API a saber que algo deu errado
        return False

    # --- ESTÁGIO 2: O "Detetive" faz todo o trabalho de conciliação. ---
    # Uma única chamada para executar todas as etapas de enriquecimento.
    conciliador = ConciliadorVendas(df_excel=processador.df_excel, df_csv=processador.df_csv)
    dataframe_final = conciliador.enriquecer_dados()

    # --- ESTÁGIO 3: O Pipeline apenas salva o resultado final. ---
    # A operação de salvar é a última coisa que acontece.
    dataframe_final.to_excel(caminho_saida, index=False)
    
    print(f"--- PIPELINE CONCLUÍDO. Resultado salvo em: {caminho_saida} ---")
    return True