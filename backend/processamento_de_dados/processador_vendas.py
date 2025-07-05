import pandas as pd
from datetime import datetime
from ..utils.formatadores import corrigir_data_inteligentemente
from ..config import COLUNAS_PARA_REMOVER, NOMES_EXCLUIR, COLUNA_DATA_CONTRATO_EXCEL, COLUNA_DATA_ADESAO_EXCEL, COLUNA_NOME_EXCEL, COLUNA_RESPONSAVEL_CSV

NOVAS_COLUNAS = ['CRM', 'VENDEDOR_TELE', 'CATEGORIA', 'SUBCATEGORIA']
COLUNAS_DE_DATA = [COLUNA_DATA_CONTRATO_EXCEL, COLUNA_DATA_ADESAO_EXCEL]

class ProcessadorVendas:
    def __init__(self, csv_path: str, excel_path: str):
        self.csv_path = csv_path
        self.excel_path = excel_path
        self.df_csv = None
        self.df_excel = None

    def _carregar_dados(self):
        self.df_csv = pd.read_csv(self.csv_path, sep=";", encoding='utf-8-sig', on_bad_lines='skip')
        self.df_excel = pd.read_excel(self.excel_path, dtype=str)
        self._normalizar_nomes_colunas()

    def _normalizar_nomes_colunas(self):
        self.df_excel.columns = [str(col).strip().upper() for col in self.df_excel.columns]
        self.df_csv.columns = [str(col).strip().upper() for col in self.df_csv.columns]

    def _filtrar_csv_por_mes_atual(self):
        """Filtra do DataFrame do CSV para manter apenas registro do mes e do ano atuais"""

        print("Etapa de limpeza: Filtrando CSV por mes atual")
        coluna_filtro = COLUNA_RESPONSAVEL_CSV.upper()

        if coluna_filtro not in self.df_csv.columns:
            print(f"Aviso: Colunas '{coluna_filtro}' não encontrada no CSV. Pulando filtro")
            return
        
        hoje = datetime.today()
        data_da_coluna = pd.to_datetime(self.df_csv[coluna_filtro], errors='coerce')

        mascara_mes_ano_correto = (data_da_coluna.dt.month == hoje.month) & (data_da_coluna.dt.year == hoje.year)

        linhas_antes = len(self.df_csv)
        self.df_csv = self.df_csv[mascara_mes_ano_correto].copy()

        print(f"CSV filtrado. {linhas_antes - len(self.df_csv)} linhas de meses anteriores ou invalidas removidas")

    def _corrigir_datas(self):
        for col in COLUNAS_DE_DATA:
            if col in self.df_excel.columns:
                self.df_excel[col] = self.df_excel[col].apply(corrigir_data_inteligentemente)

    def _preencher_novas_colunas(self):
        for col in NOVAS_COLUNAS:
            if col not in self.df_excel.columns: self.df_excel[col] = None

    def _remover_colunas_desnecessarias(self):
        colunas_encontradas = [col for col in COLUNAS_PARA_REMOVER if col in self.df_excel.columns]
        if colunas_encontradas: self.df_excel.drop(columns=colunas_encontradas, inplace=True)

    def _remover_clientes_excluidos(self):
        if COLUNA_NOME_EXCEL in self.df_excel.columns:
            self.df_excel = self.df_excel[~self.df_excel[COLUNA_NOME_EXCEL].str.upper().isin(NOMES_EXCLUIR)].copy()

    def executar(self):
        print("\n--- Iniciando Processamento (Chef) ---")
        self._carregar_dados()
        self._filtrar_csv_por_mes_atual()
        self._corrigir_datas()
        self._preencher_novas_colunas()
        self._remover_clientes_excluidos()
        self._remover_colunas_desnecessarias()
        print("--- Processamento do Chef concluído! ---\n")