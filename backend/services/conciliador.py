import pandas as pd
from rapidfuzz import process, fuzz
from datetime import date, datetime

# Importando a lista de clientes manuais do nosso arquivo de configuração
from ..config import NOVOS_CLIENTES_MANUAIS

class ConciliadorVendas:
    """
    Nosso "Detetive de Dados".
    Responsável por conciliar os dataframes do Excel e CSV,
    atualizando clientes existentes e adicionando novos.
    """
    def __init__(self, df_excel: pd.DataFrame, df_csv: pd.DataFrame):
        self.df_excel = df_excel.copy()
        self.df_csv = df_csv.copy()
        self.matches = {}

    def _normalizar_nomes(self):
        """Cria colunas temporárias com nomes normalizados para comparação."""
        print("-> Normalizando nomes para comparação...")
        self.df_excel['NOME_NORM'] = self.df_excel['NOME'].astype(str).str.strip().str.upper()
        self.df_csv['Id Cliente_NORM'] = self.df_csv['Id Cliente'].astype(str).str.strip().str.upper()

    def _encontrar_correspondentes(self, limite_similaridade=90):
        """Usa rapidfuzz para encontrar correspondências entre os nomes."""
        print(f"-> Encontrando correspondências com similaridade > {limite_similaridade}%...")
        nomes_excel = self.df_excel['NOME_NORM'].tolist()
        nomes_csv = self.df_csv['Id Cliente_NORM'].unique().tolist()
        match_list = []

        # Para cada nome do Excel, procura o par mais similar na lista do CSV,
        # considerando apenas correspondências com mais de 90% de similaridade.
        for nome_excel in nomes_excel:
            best_match = process.extractOne(
                nome_excel, nomes_csv,
                scorer=fuzz.WRatio,
                score_cutoff=limite_similaridade
            )
            if best_match:
                match_list.append((nome_excel, best_match[0]))
        
        self.matches = dict(match_list)
        print(f"   {len(self.matches)} correspondências encontradas.")

    def _atualizar_clientes_existentes_vetorizados(self):
        """
        Atualiza os dados usando a abordagem vetorizada (rápida) do pandas.
        """
        print("-> Atualizando clientes existentes...")
        if not self.matches:
            print("   Nenhuma correspondência para atualizar.")
            return

        mapa_excel_para_csv = pd.Series(self.matches)
        self.df_excel['csv_match'] = self.df_excel['NOME_NORM'].map(mapa_excel_para_csv)

        # Antes de criar o índice, removemos as duplicatas do CSV,
        # mantendo apenas a primeira ocorrência de cada cliente.
        df_csv_unico = self.df_csv.drop_duplicates(subset=['Id Cliente_NORM'], keep='first')

        # Agora, criamos o mapeamento a partir do DataFrame JÁ SEM duplicatas.
        csv_mapeamento = df_csv_unico.set_index('Id Cliente_NORM')
        
        # O resto do código continua igual...
        self.df_excel['VENDEDOR_TELE'] = self.df_excel['csv_match'].map(csv_mapeamento['Unidade'])
        self.df_excel['CATEGORIA'] = self.df_excel['csv_match'].map(csv_mapeamento['Data de criação'])
        self.df_excel['SUBCATEGORIA'] = self.df_excel['csv_match'].map(csv_mapeamento['Origem (categoria)'])
        self.df_excel['CRM'] = self.df_excel['csv_match'].map(csv_mapeamento['Id Cliente'])

    def _adicionar_novos_clientes(self):
        """Adiciona clientes que estão no CSV mas não tiveram correspondência no Excel."""
        print("-> Verificando novos clientes do CSV...")
        nomes_csv_matched = set(self.matches.values())
        todos_nomes_csv = set(self.df_csv['Id Cliente_NORM'].unique())
        novos_nomes_csv = todos_nomes_csv - nomes_csv_matched

        if not novos_nomes_csv:
            print("   Nenhum cliente novo para adicionar.")
            return
        
        novas_linhas = []
        df_novos = self.df_csv[self.df_csv['Id Cliente_NORM'].isin(novos_nomes_csv)].drop_duplicates(subset=['Id Cliente_NORM'])

        for _, row_csv in df_novos.iterrows():
            novas_linhas.append({
                'NOME': row_csv['Id Cliente'],
                'DATA_CONTRATO': pd.to_datetime(date.today()),
                'CATEGORIA': row_csv['Data de criação'],
                'SUBCATEGORIA': row_csv['Origem (categoria)'],
                'VENDEDOR_TELE': row_csv['Unidade']
            })
        
        if novas_linhas:
            novos_clientes_df = pd.DataFrame(novas_linhas)
            self.df_excel = pd.concat([self.df_excel, novos_clientes_df], ignore_index=True)
            print(f"   Adicionados {len(novas_linhas)} novos clientes.")

    def _adicionar_clientes_manuais(self):
        """Adiciona uma lista pré-definida de clientes do arquivo de configuração."""
        print("-> Etapa Extra: Adicionando clientes da lista manual...")
        if not NOVOS_CLIENTES_MANUAIS:
            print("   Nenhum cliente manual para adicionar na configuração.")
            return

        df_manuais = pd.DataFrame(NOVOS_CLIENTES_MANUAIS)
        
        if 'DATA_CONTRATO' in df_manuais.columns:
            df_manuais['DATA_CONTRATO'] = pd.to_datetime(df_manuais['DATA_CONTRATO'], dayfirst=True, errors='coerce')
        
        self.df_excel = pd.concat([self.df_excel, df_manuais], ignore_index=True)
        print(f"   {len(df_manuais)} clientes manuais adicionados.")

    def _limpar_colunas_temporarias(self):
        """Remove as colunas auxiliares utilizadas no processo."""
        print("-> Limpando colunas temporárias...")
        self.df_excel.drop(columns=['NOME_NORM', 'csv_match'], inplace=True, errors='ignore')

    def enriquecer_dados(self) -> pd.DataFrame:
        """Método principal que orquestra todo o processo de enriquecimento."""
        print("\n--- Iniciando Conciliação (Investigação do Detetive) ---")
        self._normalizar_nomes()
        self._encontrar_correspondentes()
        self._atualizar_clientes_existentes_vetorizados()
        self._adicionar_novos_clientes()
        self._adicionar_clientes_manuais() # <-- Etapa integrada aqui
        self._limpar_colunas_temporarias()
        print("--- Conciliação concluída com sucesso! ---\n")
        return self.df_excel