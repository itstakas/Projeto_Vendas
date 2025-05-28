import pandas as pd
from datetime import datetime
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import numbers
from openpyxl import load_workbook
import openpyxl


class ProcessaDados:
    def __init__(self, csv_path, excel_path):
        self.csv_df = pd.read_csv(csv_path, sep=";")
        self.excel_df = pd.read_excel(excel_path)

        # Filtrar por mês atual
        self.filtrar_mes_atual()

        self.preencher_novas_colunas()

    def filtrar_mes_atual(self):
        hoje = datetime.today()
        self.csv_df['Data de criação'] = pd.to_datetime(self.csv_df['Data de criação'], errors='coerce')
        self.csv_df = self.csv_df[
            (self.csv_df['Data de criação'].dt.month == hoje.month) &
            (self.csv_df['Data de criação'].dt.year == hoje.year)
        ]
        
    def preencher_novas_colunas(self):
        self.excel_df['CRM'] = None
        self.excel_df['VENDEDOR_TELE'] = None
        self.excel_df['CATEGORIA'] = None
        self.excel_df['SUBCATEGORIA'] = None

    def salvar_excel_preenchido(self, caminho_saida):
        self.excel_df.to_excel(caminho_saida, index=False)
