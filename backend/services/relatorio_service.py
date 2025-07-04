import pandas as pd
from ..config import NOMES_PORTA_A_PORTA, NOMES_EXTERNA

class RelatorioService:
    """
    Nosso "Assistente com Memória Fotográfica".
    Carrega o DataFrame do resultado uma vez e fornece métodos para consultá-lo.
    """
    def __init__(self):
        self.df = None
        print("Serviço de Relatório criado. Aguardando dados...")

    def carregar_dados(self, caminho_arquivo: str):
        """
        Lê o arquivo Excel e o armazena na memória (em self.df).
        Este método deve ser chamado uma vez, logo após o pipeline principal rodar.
        """
        try:
            self.df = pd.read_excel(caminho_arquivo, dtype=str, engine='openpyxl')
            # Já converte a coluna de data aqui, uma única vez!
            self.df['DATA_CONTRATO'] = pd.to_datetime(self.df['DATA_CONTRATO'], errors='coerce', dayfirst=True)
            print(f"Serviço de Relatório: Dados de '{caminho_arquivo}' carregados com sucesso na memória.")
        except FileNotFoundError:
            self.df = None
            print(f"AVISO: Arquivo de resultado '{caminho_arquivo}' não encontrado.")
        except Exception as e:
            self.df = None
            print(f"ERRO ao carregar dados para o serviço de relatório: {e}")

    def obter_vendas_por_tele(self) -> list:
        """Lógica que antes estava na rota /vendedores_tele."""
        if self.df is None or 'VENDEDOR_TELE' not in self.df.columns:
            return []
        
        df_vendedores = self.df.dropna(subset=['VENDEDOR_TELE']).copy()
        df_vendedores['MES'] = df_vendedores['DATA_CONTRATO'].dt.to_period('M').astype(str)
        vendas_por_vendedor = df_vendedores.groupby(['VENDEDOR_TELE', 'MES']).size().reset_index(name='QTD_VENDAS')
        
        resultado = []
        for vendedor in vendas_por_vendedor['VENDEDOR_TELE'].unique():
            vendas = vendas_por_vendedor[vendas_por_vendedor['VENDEDOR_TELE'] == vendedor]
            resultado.append({'nome': vendedor, 'total_vendas': int(vendas['QTD_VENDAS'].sum()), 'vendas_mensais': vendas[['MES', 'QTD_VENDAS']].to_dict(orient='records')})
        return resultado

    def obter_detalhes_vendedor_tele(self, nome: str) -> list:
        """Lógica que antes estava na rota /vendedor_tele/<nome>."""
        if self.df is None or 'VENDEDOR_TELE' not in self.df.columns:
            return []

        nome_normalizado = nome.strip().lower()
        df_temp = self.df.copy()
        df_temp['VENDEDOR_TELE'] = df_temp['VENDEDOR_TELE'].fillna('').str.strip().str.lower()
        df_vendedor = df_temp[df_temp['VENDEDOR_TELE'] == nome_normalizado]
        
        # A data já foi convertida, só precisamos formatar para string
        df_vendedor['DATA_CONTRATO_STR'] = df_vendedor['DATA_CONTRATO'].dt.strftime('%d/%m/%Y').fillna("Data Inválida")
        return df_vendedor[['NOME', 'DATA_CONTRATO_STR']].to_dict(orient='records')

    # Você adicionaria aqui os outros métodos para 'porta a porta', etc.
    # Exemplo: def obter_vendas_porta_a_porta(self) -> list: ...