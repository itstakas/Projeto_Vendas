import pandas as pd
from datetime import datetime
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import numbers
from openpyxl import load_workbook
import openpyxl
from controladores.troca_data import DataCorreta


class ProcessaDados:
    def __init__(self, csv_path, excel_path):
        self.csv_df = pd.read_csv(csv_path, sep=";")
        self.excel_df = pd.read_excel(excel_path)

        # #CORRIGE AS DATAS ANTES DO COMPARATIVO
        # corretor = DataCorreta()
        # if 'DATA_CONTRATO' in self.excel_df.columns:
        #     self.excel_df = corretor.corrigir_coluna(self.excel_df, 'DATA_CONTRATO')

        # if 'DATA_ADESAO' in self.excel_df.columns:
        #     self.excel_df = corretor.corrigir_coluna(self.excel_df, 'DATA_ADESAO')

        # Converter datas
        # if 'Data de criação' in self.excel_df.columns:
        #self.csv_df['Data de criação'] = pd.to_datetime(self.csv_df['Data de criação'], dayfirst=True,errors='coerce')
        # self.excel_df['DATA_CONTRATO'] = pd.to_datetime(self.excel_df['DATA_CONTRATO'], dayfirst=True, errors='coerce')
        # self.excel_df['DATA_ADESAO'] = pd.to_datetime(self.excel_df['DATA_ADESAO'], dayfirst=True, errors='coerce')

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
