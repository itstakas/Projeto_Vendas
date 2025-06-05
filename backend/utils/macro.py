import pythoncom
import win32com.client as win32
import datetime 
import pandas as pd
import tempfile
import os
import gc
import time
from main import app
import shutil

def colar_e_executar_macro(df, caminho_macro):
    pythoncom.CoInitialize()
    temp_dir = tempfile.gettempdir()
    caminho_saida = os.path.join(temp_dir, 'arquivo_macro_temp.xlsx')
    temp_macro_path = os.path.join(temp_dir, 'temp_macro.xlsm')

    try:
        # Copia o arquivo macro para um temporário
        shutil.copy(caminho_macro, temp_macro_path)

        excel = win32.gencache.EnsureDispatch('Excel.Application')
        excel.Visible = False
        excel.DisplayAlerts = False

        wb = excel.Workbooks.Open(temp_macro_path)
        ws = wb.Sheets('Vendas')

        ws.Range("A2:Z1000").ClearContents()

        # Escreve os dados no Excel
        for i, col in enumerate(df.columns):
            ws.Cells(1, i + 1).Value = col

        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                value = df.iat[row, col]
                if isinstance(value, (datetime.date, pd.Timestamp)):
                    value = value.strftime('%d/%m/%Y')
                elif pd.isna(value):
                    value = ''
                ws.Cells(row + 2, col + 1).Value = value

        # Executa a macro, com o nome e módulo corretos
        excel.Application.Run("Módulo3.LocalizarESubstituirVariasCelulas")

        wb.Sheets('Vendas').Activate()
        wb.SaveAs(caminho_saida, FileFormat=51)

        wb.Close(SaveChanges=True)
        excel.Quit()

        if os.path.getsize(caminho_saida) > 0:
            df_resultante = pd.read_excel(caminho_saida)
        else:
            df_resultante = pd.DataFrame()

    finally:
        pythoncom.CoUninitialize()

    return df_resultante, caminho_saida
