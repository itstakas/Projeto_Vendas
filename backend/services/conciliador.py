import pandas as pd
from rapidfuzz import process, fuzz
from datetime import date, datetime

# Puxa as configurações necessárias do "painel de controle" (config.py).
from backend.config import (
    NOVOS_CLIENTES_MANUAIS, COLUNA_NOME_EXCEL, COLUNA_ID_CLIENTE_CSV,
    COLUNA_UNIDADE_CSV, COLUNA_DATA_CRIACAO_CSV, COLUNA_ORIGEM_CSV
)

class ConciliadorVendas:
    """
    Esta classe é o nosso "Detetive de Dados". Sua missão é receber os dados já limpos e fazer o trabalho de cruzar as
    informações, encontrar clientes correspondentes, atualizar dados e adicionar novos clientes.
    """
    def __init__(self, df_excel: pd.DataFrame, df_csv: pd.DataFrame):
        """
        Prepara o Detetive para a investigação. Recebe as "evidências" (os DataFrames) e faz cópias para não alterar os originais.
        """
        self.df_excel = df_excel.copy()
        self.df_csv = df_csv.copy()
        # O "caderno de anotações" do detetive, para guardar os pares encontrados.
        self.matches = {}

        # Padroniza os nomes das colunas que vamos usar, pegando do config e convertendo para maiúsculas. Isso garante que o código não quebre se houver diferenças de maiúsculas/minúsculas.
        self.col_nome_excel = COLUNA_NOME_EXCEL.upper()
        self.col_id_csv = COLUNA_ID_CLIENTE_CSV.upper()
        self.col_unidade_csv = COLUNA_UNIDADE_CSV.upper()
        self.col_data_criacao_csv = COLUNA_DATA_CRIACAO_CSV.upper()
        self.col_origem_csv = COLUNA_ORIGEM_CSV.upper()

    def _normalizar_nomes(self):
        """Cria colunas temporárias com nomes de clientes "limpos" para uma comparação mais justa."""
        # Remove espaços em branco do início e do fim dos nomes.
        self.df_excel['NOME_NORM'] = self.df_excel[self.col_nome_excel].astype(str).str.strip()
        self.df_csv['ID_CLIENTE_NORM'] = self.df_csv[self.col_id_csv].astype(str).str.strip()

    def _encontrar_correspondentes(self, limite_similaridade=90):
        """Usa a "lupa de similaridade" (rapidfuzz) para encontrar os pares de clientes."""
        nomes_excel = self.df_excel['NOME_NORM'].tolist()
        nomes_csv = self.df_csv['ID_CLIENTE_NORM'].unique().tolist()
        match_list = []

        # Para cada nome do Excel, procura o nome mais parecido na lista do CSV.
        for nome_excel in nomes_excel:
            # A função `extractOne` busca a melhor correspondência que tenha uma "nota" de similaridade acima de 90.
            best_match = process.extractOne(nome_excel, nomes_csv, scorer=fuzz.WRatio, score_cutoff=limite_similaridade)
            # Se encontrou um bom par, guarda no "caderno de anotações".
            if best_match:
                match_list.append((nome_excel, best_match[0]))
        
        self.matches = dict(match_list)

    def _atualizar_clientes_existentes_vetorizado(self):
        """Preenche as informações dos clientes que deram "match", de forma rápida."""
        if not self.matches: return

        # Cria um "mapa" para saber qual cliente do Excel corresponde a qual cliente do CSV.
        mapa_excel_para_csv = pd.Series(self.matches)
        self.df_excel['CSV_MATCH'] = self.df_excel['NOME_NORM'].map(mapa_excel_para_csv)

        # Cria uma "lista telefônica" com os dados do CSV para busca instantânea.
        df_csv_unico = self.df_csv.drop_duplicates(subset=['ID_CLIENTE_NORM'], keep='first')
        csv_mapeamento = df_csv_unico.set_index('ID_CLIENTE_NORM')
        
        # Usa o mapa para "puxar" as informações do CSV para as colunas do Excel de uma só vez.
        self.df_excel['VENDEDOR_TELE'] = self.df_excel['CSV_MATCH'].map(csv_mapeamento[self.col_unidade_csv])
        self.df_excel['CATEGORIA'] = self.df_excel['CSV_MATCH'].map(csv_mapeamento[self.col_data_criacao_csv])
        self.df_excel['SUBCATEGORIA'] = self.df_excel['CSV_MATCH'].map(csv_mapeamento[self.col_origem_csv])
        self.df_excel['CRM'] = self.df_excel['CSV_MATCH'].map(csv_mapeamento[self.col_id_csv])

    def _adicionar_novos_clientes(self):
        """Encontra clientes que estão no CSV mas não no Excel e os adiciona ao final."""
        # Pega todos os nomes do CSV e subtrai os que já demos "match".
        nomes_csv_matched = set(self.matches.values())
        todos_nomes_csv = set(self.df_csv['ID_CLIENTE_NORM'].unique())
        novos_nomes_csv = todos_nomes_csv - nomes_csv_matched
        if not novos_nomes_csv: return
        
        # Cria uma lista de "fichas" para os novos clientes.
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
        
        # Adiciona todas as novas fichas de uma vez só no final do relatório.
        if novas_linhas:
            self.df_excel = pd.concat([self.df_excel, pd.DataFrame(novas_linhas)], ignore_index=True)

    def _adicionar_clientes_manuais(self):
        """Adiciona a lista de clientes fixos que está no arquivo config.py."""
        if not NOVOS_CLIENTES_MANUAIS: return
        df_manuais = pd.DataFrame(NOVOS_CLIENTES_MANUAIS)
        if 'DATA_CONTRATO' in df_manuais.columns:
            df_manuais['DATA_CONTRATO'] = pd.to_datetime(df_manuais['DATA_CONTRATO'], dayfirst=True, errors='coerce')
        self.df_excel = pd.concat([self.df_excel, df_manuais], ignore_index=True)

    def _limpar_colunas_temporarias(self):
        """Apaga as colunas de "rascunho" usadas durante a investigação."""
        self.df_excel.drop(columns=['NOME_NORM', 'CSV_MATCH'], inplace=True, errors='ignore')

    def enriquecer_dados(self) -> pd.DataFrame:
        """
        O método principal que executa a "investigação" completa, chamando todas as tarefas internas na ordem correta.
        """
        print("\n--- Iniciando Conciliação (Detetive) ---")
        self._normalizar_nomes()
        self._encontrar_correspondentes()
        self._atualizar_clientes_existentes_vetorizado()
        self._adicionar_novos_clientes()
        self._adicionar_clientes_manuais()
        self._limpar_colunas_temporarias()
        print("--- Conciliação concluída! ---\n")
        return self.df_excel
