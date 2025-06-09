import pythoncom
import win32com.client as win32
import datetime
import pandas as pd
import tempfile
import os
import gc
import time
import shutil


def colar_e_executar_macro(df, caminho_macro):
    pythoncom.CoInitialize()
    temp_dir = tempfile.gettempdir()
    caminho_saida = os.path.join(temp_dir, 'resultado.xlsx')    
    temp_macro_path = os.path.join(temp_dir, 'temp_macro.xlsm')

    excel = None
    wb = None

    try:
        # Copia o arquivo original da macro para o diretório temporário
        shutil.copy(caminho_macro, temp_macro_path)

        excel = win32.gencache.EnsureDispatch('Excel.Application')
        excel.Visible = False
        excel.DisplayAlerts = False

        wb = excel.Workbooks.Open(temp_macro_path)
        ws = wb.Sheets('Vendas')

        # Limpa a planilha antiga
        ultima_coluna = ws.Cells(1, ws.Columns.Count).End(-4159).Column  # -4159 = xlToLeft
        ultima_linha = ws.Cells(ws.Rows.Count, 1).End(-4162).Row         # -4162 = xlUp
        if ultima_linha > 1 and ultima_coluna > 1:
            ws.Range(ws.Cells(2, 1), ws.Cells(ultima_linha, ultima_coluna)).ClearContents()

        # Escreve os dados do DataFrame no Excel
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

        # Executa a macro
        excel.Application.Run("Módulo3.LocalizarESubstituirVariasCelulas")

        # Salva como .xlsx (sem macros)
        wb.SaveAs(caminho_saida, FileFormat=51)  # 51 = xlOpenXMLWorkbook

        # Leitura do resultado em pandas
        if os.path.exists(caminho_saida) and os.path.getsize(caminho_saida) > 0:
            df_resultante = pd.read_excel(caminho_saida)
        else:
            df_resultante = pd.DataFrame()

    except Exception as e:
        print(f"Erro ao executar macro: {e}")
        df_resultante = pd.DataFrame()
    finally:
        if wb:
            wb.Close(SaveChanges=False)
        if excel:
            excel.Quit()
        pythoncom.CoUninitialize()
        gc.collect()

    return df_resultante, caminho_saida
