import pandas as pd
from rapidfuzz import process, fuzz
from datetime import date, datetime
from ..config import (
    NOVOS_CLIENTES_MANUAIS, COLUNA_NOME_EXCEL, COLUNA_ID_CLIENTE_CSV,
    COLUNA_UNIDADE_CSV, COLUNA_DATA_CRIACAO_CSV, COLUNA_ORIGEM_CSV
)

class ConciliadorVendas:
    """
    Nosso "Detetive de Dados". Assume que os DataFrames já chegam com os
    nomes das colunas padronizados (maiúsculas).
    """
    def __init__(self, df_excel: pd.DataFrame, df_csv: pd.DataFrame):
        self.df_excel = df_excel.copy()
        self.df_csv = df_csv.copy()
        self.matches = {}

        # --- CORREÇÃO FINAL: Padronizamos os nomes das colunas que vamos usar ---
        # Pegamos os nomes do config e já os convertemos para maiúsculas aqui, uma vez.
        self.col_nome_excel = COLUNA_NOME_EXCEL.upper()
        self.col_id_csv = COLUNA_ID_CLIENTE_CSV.upper()
        self.col_unidade_csv = COLUNA_UNIDADE_CSV.upper()
        self.col_data_criacao_csv = COLUNA_DATA_CRIACAO_CSV.upper()
        self.col_origem_csv = COLUNA_ORIGEM_CSV.upper()

    def _normalizar_nomes(self):
        """Cria colunas temporárias com nomes de clientes normalizados (sem espaços extras)."""
        print("-> Normalizando nomes de clientes para comparação...")
        self.df_excel['NOME_NORM'] = self.df_excel[self.col_nome_excel].astype(str).str.strip()
        self.df_csv['ID_CLIENTE_NORM'] = self.df_csv[self.col_id_csv].astype(str).str.strip()

    def _encontrar_correspondentes(self, limite_similaridade=90):
        """Usa rapidfuzz para encontrar correspondências entre os nomes."""
        print(f"-> Encontrando correspondências com similaridade > {limite_similaridade}%...")
        nomes_excel = self.df_excel['NOME_NORM'].tolist()
        nomes_csv = self.df_csv['ID_CLIENTE_NORM'].unique().tolist()
        match_list = []
        for nome_excel in nomes_excel:
            best_match = process.extractOne(nome_excel, nomes_csv, scorer=fuzz.WRatio, score_cutoff=limite_similaridade)
            if best_match: match_list.append((nome_excel, best_match[0]))
        self.matches = dict(match_list)
        print(f"   {len(self.matches)} correspondências encontradas.")

    def _atualizar_clientes_existentes_vetorizado(self):
        """Atualiza os dados usando a abordagem vetorizada (rápida) do pandas."""
        print("-> Atualizando clientes existentes...")
        if not self.matches: return

        mapa_excel_para_csv = pd.Series(self.matches)
        self.df_excel['CSV_MATCH'] = self.df_excel['NOME_NORM'].map(mapa_excel_para_csv)

        df_csv_unico = self.df_csv.drop_duplicates(subset=['ID_CLIENTE_NORM'], keep='first')
        csv_mapeamento = df_csv_unico.set_index('ID_CLIENTE_NORM')
        
        self.df_excel['VENDEDOR_TELE'] = self.df_excel['CSV_MATCH'].map(csv_mapeamento[self.col_unidade_csv])
        self.df_excel['CATEGORIA'] = self.df_excel['CSV_MATCH'].map(csv_mapeamento[self.col_data_criacao_csv])
        self.df_excel['SUBCATEGORIA'] = self.df_excel['CSV_MATCH'].map(csv_mapeamento[self.col_origem_csv])
        self.df_excel['CRM'] = self.df_excel['CSV_MATCH'].map(csv_mapeamento[self.col_id_csv])

    def _adicionar_novos_clientes(self):
        """Adiciona clientes que estão no CSV mas não tiveram correspondência no Excel."""
        print("-> Verificando novos clientes do CSV...")
        nomes_csv_matched = set(self.matches.values())
        todos_nomes_csv = set(self.df_csv['ID_CLIENTE_NORM'].unique())
        novos_nomes_csv = todos_nomes_csv - nomes_csv_matched
        if not novos_nomes_csv: return
        
        novas_linhas = []
        df_novos = self.df_csv[self.df_csv['ID_CLIENTE_NORM'].isin(novos_nomes_csv)].drop_duplicates(subset=['ID_CLIENTE_NORM'])

        for _, row_csv in df_novos.iterrows():
            novas_linhas.append({
                self.col_nome_excel: row_csv[self.col_id_csv],
                'DATA_CONTRATO': pd.to_datetime(date.today()),
                'CATEGORIA': row_csv[self.col_data_criacao_csv],
                'SUBCATEGORIA': row_csv[self.col_origem_csv],
                'VENDEDOR_TELE': row_csv[self.col_unidade_csv]
            })
        
        if novas_linhas: self.df_excel = pd.concat([self.df_excel, pd.DataFrame(novas_linhas)], ignore_index=True)
        print(f"   Adicionados {len(novas_linhas)} novos clientes.")

    def _adicionar_clientes_manuais(self):
        """Adiciona uma lista pré-definida de clientes do arquivo de configuração."""
        print("-> Etapa Extra: Adicionando clientes da lista manual...")
        if not NOVOS_CLIENTES_MANUAIS: return

        df_manuais = pd.DataFrame(NOVOS_CLIENTES_MANUAIS)
        if 'DATA_CONTRATO' in df_manuais.columns:
            df_manuais['DATA_CONTRATO'] = pd.to_datetime(df_manuais['DATA_CONTRATO'], dayfirst=True, errors='coerce')
        
        self.df_excel = pd.concat([self.df_excel, df_manuais], ignore_index=True)
        print(f"   {len(df_manuais)} clientes manuais adicionados.")

    def _limpar_colunas_temporarias(self):
        """Remove as colunas auxiliares utilizadas no processo."""
        print("-> Limpando colunas temporárias...")
        self.df_excel.drop(columns=['NOME_NORM', 'CSV_MATCH'], inplace=True, errors='ignore')

    def enriquecer_dados(self) -> pd.DataFrame:
        """Método principal que orquestra todo o processo de enriquecimento."""
        print("\n--- Iniciando Conciliação (Detetive) ---")
        self._normalizar_nomes()
        self._encontrar_correspondentes()
        self._atualizar_clientes_existentes_vetorizado()
        self._adicionar_novos_clientes()
        self._adicionar_clientes_manuais()
        self._limpar_colunas_temporarias()
        print("--- Conciliação concluída! ---\n")
        return self.df_excel