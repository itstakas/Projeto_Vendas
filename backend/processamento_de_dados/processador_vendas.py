# Arquivo: controladores/Classes.py
import pandas as pd
from datetime import datetime
from ..utils.formatadores import corrigir_data_inteligentemente
from ..config import COLUNAS_PARA_REMOVER, NOMES_EXCLUIR

"""Os prints são mais para saber se algo der errado no codigo, onde exatamente estavamos, lembrete: Apagar os prints(opcional)"""

COLUNAS_DE_DATA = ['DATA_CONTRATO', 'DATA_ADESAO']
NOVAS_COLUNAS = ['CRM', 'VENDEDOR_TELE', 'CATEGORIA', 'SUBCATEGORIA']


class ProcessadorVendas:
    """
        Classe responsavel por carregar, limpar, processar e salvar dados de vendas do arquivo csv e excel
    """

    def __init__(self, csv_path: str, excel_path: str):
        """
            Inicializa o processaor com os caminhos dos arquivos, nenhum dado é carregado ou processado aqui
        """
        print("Objeto ProcessadorVendas criado")
        self.csv_path = csv_path
        self.excel_path = excel_path

        # O estado (os dataframes) iniciam com Nnone, so sera preenchido quando o processamento for executado
        self.csv_path = None
        self.excel_path = None

    def _carregar_dados(self):
        """
        Metodo privado para carregar os arquivos nos dataframes
        """
        print("Iniciando carregamento dos arquivos...")

        self.csv_df = pd.read_csv(
            self.csv_path, sep=";", encoding='utf-8-sig', on_bad_lines='skip')
        self.excel_df = pd.read_excel(self.excel_path, dtype=str)

        print("Arquivos carregados com sucesso!")

    def _corrigir_datas(self):
        """
        Aplica a correção inteligente nas colunas de data
        """
        print("Aplicando correção inteligente nas coluanas de datas...")

        for col in COLUNAS_DE_DATA:
            if col in self.excel_df.columns:
                self.excel_df[col] = self.excel_df[col].apply(
                    corrigir_data_inteligentemente)

        print("Datas corrigidas")

    def _preecnher_novas_colunas(self):
        """
        Adiciona colunas vazias no datafram e do excel, as colunas que usaremos para o relatorio, 'CRM', 'VENDEDOR_TELE', 'CATEGORIA', 'SUBCATEGORIA
        '"""
        print("Adicionando colunas")

        for col in NOVAS_COLUNAS:
            self.excel_df[col] = None

        print("Novas colunas adicionadas")

    def executar(self):
        """
        Orquestra todo o processo de ETL (Extract, transform, Load). Este é o metodo principal a ser chamado, tanto que ele não tem o _ ou seja, não é privado
        """

        print("Iniciando processamento: ")

        self._carregar_dados()
        self._corrigir_datas()
        self._preecnher_novas_colunas()

        print("Processamento concluido com sucesso!")

    def salvar_resultado(self, caminho_saida: str):
        """
        Salva o dataframe processado em um novo arquivo excel, formatando as datas de volta para o formato brasileiro padrão DD/MM/AAAA
        """

        print("salvando os arquivos...")

        if self.excel_df is None:
            print(
                "Erro: Nenhum dado foi processado. Execute o method .executar() primeiro")
            return

        print(f"Salvando arquivos em: {caminho_saida}")

        df_para_salvar = self.excel_df.copy()
        # USANDO A CONSTANTE AQUI TAMBEM (PRINCIPIO DRY)

        for col in COLUNAS_DE_DATA:
            if col in df_para_salvar.columns and pd.api.types.is_datetime64_any_dtype(df_para_salvar[col]):
                df_para_salvar[col] = df_para_salvar[col].dt.strftime(
                    '%d/%m/%Y').replace('NaT', '')

        df_para_salvar.to_excel(
            caminho_saida, index=False, engine='xlsxwriter')

        print("Arquivo salvo com sucesso")
