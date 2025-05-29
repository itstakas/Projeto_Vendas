import pandas as pd
from datetime import datetime
# from openpyxl.utils.dataframe import dataframe_to_rows
# from openpyxl.styles import numbers
# from openpyxl import load_workbook
# import openpyxl


class ProcessaDados:
    def __init__(self, csv_path, excel_path):
        self.csv_df = pd.read_csv(csv_path, sep=";")
        self.excel_df = pd.read_excel(excel_path)

        # self.excel_df['DATA_CONTRATO'] = pd.to_datetime(
        #     self.excel_df['DATA_CONTRATO'],
        #     dayfirst=True,
        #     errors='coerce'  # transforma inválidos em NaT
        # )

        for data in self.excel_df['DATA_CONTRATO']:
            print(f"Formato da data: {type(data)} | Valor: {data}")

        self.preencher_novas_colunas()
        
    def preencher_novas_colunas(self):
        self.excel_df['CRM'] = None
        self.excel_df['VENDEDOR_TELE'] = None
        self.excel_df['CATEGORIA'] = None
        self.excel_df['SUBCATEGORIA'] = None

    def salvar_excel_preenchido(self, caminho_saida):
        self.excel_df.to_excel(caminho_saida, index=False)
