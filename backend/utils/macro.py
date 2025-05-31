import pythoncom
import win32com.client as win32
import datetime 
import pandas as pd
import tempfile
import os
import gc
import time

def colar_e_executar_macro(df, caminho_macro):
    # Inicializa COM manualmente
    pythoncom.CoInitialize()

    # Cria arquivo temporário para salvar após macro
    temp_dir = tempfile.gettempdir()
    caminho_saida = os.path.join(temp_dir, 'arquivo_macro_temp.xlsx')

    try:
        excel = win32.gencache.EnsureDispatch('Excel.Application')
        excel.Visible = True
        excel.DisplayAlerts = False  # evita janelas de confirmação

        # Abre o arquivo com macro
        wb = excel.Workbooks.Open(caminho_macro)
        ws = wb.Sheets('Vendas')

        ws.Range("A2:Z1000").ClearContents()

        for i, col in enumerate(df.columns):
            ws.Cells(1, i + 1).Value = col

        # Cola os dados
        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                value = df.iat[row, col]

                # Se for data, formata como string dd/mm/aaaa
                if isinstance(value, (datetime.date, pd.Timestamp)):
                    value = value.strftime('%d/%m/%Y')

                # Evita erro com NaN
                elif pd.isna(value):
                    value = ''

                ws.Cells(row + 2, col + 1).Value = value

        try:
            excel.Application.Run("LocalizarESubstituirVariasCelulas")

        except Exception as e:
            print(f"Erro ao executar a macro: {e}")

        # Salva e fecha
        wb.SaveAs(caminho_saida, FileFormat=51)

        wb.Close(SaveChanges=True)
        excel.Quit()

        time.sleep(1)

        df_resultante = pd.read_excel(caminho_saida)

    finally:
        # Libera a COM
        ws = None
        wb = None
        excel = None
        gc.collect()
        pythoncom.CoUninitialize()

    return df_resultante

def colar_macro(caminho_entrada, caminho_saida):

    pythoncom.CoInitialize()

    try:
        excel = win32.gencache.EnsureDispatch("Excel.Apllication")
        excel.Visible = False
        excel.DisplayAlerts = False

        #Abre o arquivo original com macro aplicada
        wb_origem = excel.Workbooks.Open(caminho_entrada)
        ws_origem = wb_origem.Worksheets(1)

        ultima_linha = ws_origem.UsedRange.Rows.Count
        ultima_coluna = ws_origem.UsedRange.Columns.Count
        intervalo = ws_origem.Range(ws_origem.Cells(1, 1), ws_origem(ultima_linha, ultima_coluna))

        intervalo.Copy()

        # Cria planilha onde os dados formatados serão colados
        wb_destino

    finally:

        pythoncom.CoInitialize()
