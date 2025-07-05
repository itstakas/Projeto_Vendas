import pandas as pd
from backend.config import NOMES_PORTA_A_PORTA, NOMES_EXTERNA

class RelatorioService:
    """
    Esta classe é o nosso "Assistente de Pesquisa com Memória Fotográfica". Sua missão é carregar o arquivo de resultado final uma única vez na memória e fornecer métodos rápidos para consultar esses dados, sem precisar ler o arquivo do disco a cada requisição.
    """
    def __init__(self):
        """Prepara o assistente, que começa sem nenhum dado memorizado."""
        self.df = None
        print("Serviço de Relatório criado. Aguardando dados...")

    def carregar_dados(self, caminho_arquivo: str):
        """
        Lê o arquivo Excel e o armazena na memória (em self.df). Este método é chamado uma vez, logo após o pipeline principal rodar.
        """
        try:
            self.df = pd.read_excel(caminho_arquivo, dtype=str, engine='openpyxl')
            # Já converte a coluna de data aqui, uma única vez, de forma robusta.
            self.df['DATA_CONTRATO'] = pd.to_datetime(self.df['DATA_CONTRATO'], errors='coerce')
            print(f"Serviço de Relatório: Dados de '{caminho_arquivo}' carregados com sucesso na memória.")
        except Exception as e:
            self.df = None
            print(f"ERRO ao carregar dados para o serviço de relatório: {e}")

    def obter_vendas_por_tele(self) -> list:
        """Calcula e retorna o total de vendas agrupado por vendedor de telemarketing e por mês."""
        # Se os dados ainda não foram carregados, retorna uma lista vazia.
        if self.df is None or 'VENDEDOR_TELE' not in self.df.columns: return []
        
        # Pega as linhas que têm um vendedor de telemarketing.
        df_vendedores = self.df.dropna(subset=['VENDEDOR_TELE']).copy()
        # Cria uma coluna 'MES' para poder agrupar.
        df_vendedores['MES'] = df_vendedores['DATA_CONTRATO'].dt.to_period('M').astype(str)
        # Agrupa e conta as vendas.
        vendas_por_vendedor = df_vendedores.groupby(['VENDEDOR_TELE', 'MES']).size().reset_index(name='QTD_VENDAS')
        
        resultado = []
        for vendedor in vendas_por_vendedor['VENDEDOR_TELE'].unique():
            vendas = vendas_por_vendedor[vendas_por_vendedor['VENDEDOR_TELE'] == vendedor]
            resultado.append({'nome': vendedor, 'total_vendas': int(vendas['QTD_VENDAS'].sum()), 'vendas_mensais': vendas[['MES', 'QTD_VENDAS']].to_dict(orient='records')})
        return resultado

    def obter_detalhes_vendedor_tele(self, nome: str) -> list:
        """Encontra todos os clientes de um vendedor de telemarketing específico."""
        if self.df is None or 'VENDEDOR_TELE' not in self.df.columns: return []

        nome_normalizado = nome.strip().lower()
        df_temp = self.df.copy()
        df_temp['VENDEDOR_TELE'] = df_temp['VENDEDOR_TELE'].fillna('').str.strip().str.lower()
        df_vendedor = df_temp[df_temp['VENDEDOR_TELE'] == nome_normalizado].copy()
        
        # Formata a data para o formato DD/MM/YYYY para ser exibida no frontend.
        df_vendedor['DATA_CONTRATO_STR'] = df_vendedor['DATA_CONTRATO'].dt.strftime('%d/%m/%Y').fillna("Data Inválida")
        # Renomeia a coluna de volta para o frontend não precisar mudar.
        return df_vendedor[['NOME', 'DATA_CONTRATO_STR']].rename(columns={'DATA_CONTRATO_STR': 'DATA_CONTRATO'}).to_dict(orient='records')

    def obter_vendas_porta_a_porta(self) -> list:
        """Calcula e retorna o total de vendas para vendedores PaP e Externos."""
        if self.df is None or 'VENDEDOR' not in self.df.columns: return []

        df_vendedores = self.df.dropna(subset=['VENDEDOR']).copy()
        df_vendedores['MES'] = df_vendedores['DATA_CONTRATO'].dt.to_period('M').astype(str)
        vendas_por_vendedor = df_vendedores.groupby(['VENDEDOR', 'MES']).size().reset_index(name='QTD_VENDAS')
        
        resultado = []
        for vendedor in vendas_por_vendedor['VENDEDOR'].unique():
            vendas = vendas_por_vendedor[vendas_por_vendedor['VENDEDOR'] == vendedor]
            # Classifica o vendedor usando as listas do arquivo config.py.
            tipo = 'Outro'
            if vendedor.upper() in [nome.upper() for nome in NOMES_PORTA_A_PORTA]:
                tipo = 'porta'
            elif vendedor.upper() in [nome.upper() for nome in NOMES_EXTERNA]:
                tipo = 'externa'
            resultado.append({'nome': vendedor, 'total_vendas': int(vendas['QTD_VENDAS'].sum()), 'vendas_mensais': vendas[['MES', 'QTD_VENDAS']].to_dict(orient='records'), 'tipo_vendedor': tipo})
        return resultado

    def obter_detalhes_vendedor_pap(self, nome: str) -> list:
        """Encontra todos os clientes de um vendedor PaP ou Externo específico."""
        if self.df is None or 'VENDEDOR' not in self.df.columns: return []

        nome_normalizado = nome.strip().lower()
        df_temp = self.df.copy()
        df_temp['VENDEDOR_NORMALIZADO'] = df_temp['VENDEDOR'].fillna('').str.strip().str.lower()
        df_vendedor = df_temp[df_temp['VENDEDOR_NORMALIZADO'] == nome_normalizado].copy()
        
        # Formata a data para o formato DD/MM/YYYY.
        df_vendedor['DATA_CONTRATO_STR'] = df_vendedor['DATA_CONTRATO'].dt.strftime('%d/%m/%Y').fillna("Data Inválida")
        return df_vendedor[['NOME', 'DATA_CONTRATO_STR']].rename(columns={'DATA_CONTRATO_STR': 'DATA_CONTRATO'}).to_dict(orient='records')
