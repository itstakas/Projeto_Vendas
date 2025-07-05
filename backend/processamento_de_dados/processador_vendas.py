import pandas as pd
from datetime import datetime

# Puxa as ferramentas e configurações de outros arquivos.
from backend.utils.formatadores import corrigir_data_inteligentemente
from backend.config import (
    COLUNAS_PARA_REMOVER, NOMES_EXCLUIR, COLUNA_DATA_CONTRATO_EXCEL,
    COLUNA_DATA_ADESAO_EXCEL, COLUNA_NOME_EXCEL, COLUNA_RESPONSAVEL_CSV
)

# Listas de colunas usadas apenas por esta classe.
NOVAS_COLUNAS = ['CRM', 'VENDEDOR_TELE', 'CATEGORIA', 'SUBCATEGORIA']
COLUNAS_DE_DATA = [COLUNA_DATA_CONTRATO_EXCEL, COLUNA_DATA_ADESAO_EXCEL]


class ProcessadorVendas:
    """
    Esta classe é o nosso "Chef Preparador". Sua única missão é pegar os arquivos de dados brutos (CSV e Excel) e fazer toda a limpeza e preparação inicial.
    """

    def __init__(self, csv_path: str, excel_path: str):
        """
        Prepara o Chef para o trabalho, apenas anotando onde estão os ingredientes.
        """
        self.csv_path = csv_path
        self.excel_path = excel_path

        # As "bancadas de trabalho" começam vazias.
        self.df_csv = None
        self.df_excel = None

    def _carregar_dados(self):
        """Carrega os arquivos CSV e Excel para a memória."""
        self.df_csv = pd.read_csv(self.csv_path, sep=";", encoding='utf-8-sig', on_bad_lines='skip')
        self.df_excel = pd.read_excel(self.excel_path, dtype=str)
        # Logo após carregar, já padroniza os nomes das colunas.
        self._normalizar_nomes_colunas()

    def _normalizar_nomes_colunas(self):
        """
        Faz uma "faxina" nos nomes das colunas para evitar erros.
        Remove espaços e converte tudo para maiúsculas.
        """
        self.df_excel.columns = [str(col).strip().upper() for col in self.df_excel.columns]
        self.df_csv.columns = [str(col).strip().upper() for col in self.df_csv.columns]

    def _filtrar_csv_por_mes_atual(self):
        """Filtra a tabela do CSV, mantendo apenas os registros do mês e ano atuais."""
        coluna_filtro = COLUNA_RESPONSAVEL_CSV.upper()

        # Se a coluna de data não existir, pula esta etapa.
        if coluna_filtro not in self.df_csv.columns:
            return
        
        hoje = datetime.today()
        # Converte a coluna de texto para um formato de data real.
        datas_da_coluna = pd.to_datetime(self.df_csv[coluna_filtro], errors='coerce')

        # Cria um "filtro" (máscara) que é Verdadeiro apenas para as linhas do mês/ano corretos.
        mascara = (datas_da_coluna.dt.month == hoje.month) & (datas_da_coluna.dt.year == hoje.year)

        # Aplica o filtro, mantendo somente as linhas onde a máscara é Verdadeira.
        self.df_csv = self.df_csv[mascara].copy()

    def _corrigir_datas(self):
        """Usa nossa função inteligente para corrigir as datas no arquivo Excel."""
        for col in COLUNAS_DE_DATA:
            if col in self.df_excel.columns:
                self.df_excel[col] = self.df_excel[col].apply(corrigir_data_inteligentemente)

    def _preencher_novas_colunas(self):
        """Adiciona colunas vazias que serão preenchidas na próxima etapa do processo."""
        for col in NOVAS_COLUNAS:
            if col not in self.df_excel.columns:
                self.df_excel[col] = None

    def _remover_colunas_desnecessarias(self):
        """Apaga as colunas listadas no arquivo config.py."""
        colunas_encontradas = [col for col in COLUNAS_PARA_REMOVER if col in self.df_excel.columns]
        if colunas_encontradas:
            self.df_excel.drop(columns=colunas_encontradas, inplace=True)

    def _remover_clientes_excluidos(self):
        """Remove os clientes que estão na "lista negra" do arquivo config.py."""
        if COLUNA_NOME_EXCEL in self.df_excel.columns:
            self.df_excel = self.df_excel[~self.df_excel[COLUNA_NOME_EXCEL].str.upper().isin(NOMES_EXCLUIR)].copy()

    def executar(self):
        """
        O método principal que executa a "receita" de preparação, chamando todas as tarefas internas na ordem correta.
        """
        print("\n--- Iniciando Processamento (Chef) ---")
        self._carregar_dados()
        self._filtrar_csv_por_mes_atual()
        self._corrigir_datas()
        self._preencher_novas_colunas()
        self._remover_clientes_excluidos()
        self._remover_colunas_desnecessarias()
        print("--- Processamento do Chef concluído! ---\n")
