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
        """Lê o arquivo Excel e o armazena na memória (em self.df)."""
        try:
            self.df = pd.read_excel(caminho_arquivo, dtype=str, engine='openpyxl')
            self.df['DATA_CONTRATO'] = pd.to_datetime(self.df['DATA_CONTRATO'], format='%d/%m/%Y', errors='coerce')
            print(f"Serviço de Relatório: Dados de '{caminho_arquivo}' carregados com sucesso na memória.")
        except Exception as e:
            self.df = None
            print(f"ERRO ao carregar dados para o serviço de relatório: {e}")

    def obter_vendas_por_tele(self) -> list:
        """Lógica que antes estava na rota /vendedores_tele."""
        if self.df is None or 'VENDEDOR_TELE' not in self.df.columns: return []
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
        if self.df is None or 'VENDEDOR_TELE' not in self.df.columns: return []
        nome_normalizado = nome.strip().lower()
        df_temp = self.df.copy()
        df_temp['VENDEDOR_TELE'] = df_temp['VENDEDOR_TELE'].fillna('').str.strip().str.lower()
        df_vendedor = df_temp[df_temp['VENDEDOR_TELE'] == nome_normalizado].copy()
        
        # CORREÇÃO DO WARNING: Usamos .loc para evitar o SettingWithCopyWarning
        df_vendedor.loc[:, 'DATA_CONTRATO_STR'] = df_vendedor['DATA_CONTRATO'].dt.strftime('%d/%m/%Y').fillna("Data Inválida")
        return df_vendedor[['NOME', 'DATA_CONTRATO_STR']].rename(columns={'DATA_CONTRATO_STR': 'DATA_CONTRATO'}).to_dict(orient='records')

    # --- MÉTODOS QUE FALTAVAM ---

    def obter_vendas_porta_a_porta(self) -> list:
        """Lógica que antes estava na rota /vendedores_porta_a_porta."""
        if self.df is None or 'VENDEDOR' not in self.df.columns: return []
        df_vendedores = self.df.dropna(subset=['VENDEDOR']).copy()
        df_vendedores['MES'] = df_vendedores['DATA_CONTRATO'].dt.to_period('M').astype(str)
        vendas_por_vendedor = df_vendedores.groupby(['VENDEDOR', 'MES']).size().reset_index(name='QTD_VENDAS')
        resultado = []
        for vendedor in vendas_por_vendedor['VENDEDOR'].unique():
            vendas = vendas_por_vendedor[vendas_por_vendedor['VENDEDOR'] == vendedor]
            tipo = 'Outro'
            if vendedor.upper() in [nome.upper() for nome in NOMES_PORTA_A_PORTA]:
                tipo = 'porta'
            elif vendedor.upper() in [nome.upper() for nome in NOMES_EXTERNA]:
                tipo = 'externa'
            resultado.append({'nome': vendedor, 'total_vendas': int(vendas['QTD_VENDAS'].sum()), 'vendas_mensais': vendas[['MES', 'QTD_VENDAS']].to_dict(orient='records'), 'tipo_vendedor': tipo})
        return resultado

    def obter_detalhes_vendedor_pap(self, nome: str) -> list:
        """Lógica que antes estava na rota /vendedores_porta_a_porta/<nome>."""
        if self.df is None or 'VENDEDOR' not in self.df.columns: return []
        nome_normalizado = nome.strip().lower()
        df_temp = self.df.copy()
        df_temp['VENDEDOR_NORMALIZADO'] = df_temp['VENDEDOR'].fillna('').str.strip().str.lower()
        df_vendedor = df_temp[df_temp['VENDEDOR_NORMALIZADO'] == nome_normalizado].copy()
        
        df_vendedor.loc[:, 'DATA_CONTRATO_STR'] = df_vendedor['DATA_CONTRATO'].dt.strftime('%d/%m/%Y').fillna("Data Inválida")
        return df_vendedor[['NOME', 'DATA_CONTRATO_STR']].rename(columns={'DATA_CONTRATO_STR': 'DATA_CONTRATO'}).to_dict(orient='records')