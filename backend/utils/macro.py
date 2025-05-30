import pythoncom
import win32com.client as win32
import datetime 
import pandas as pd
import tempfile
import os
import gc

def colar_e_executar_macro(df, caminho_macro):
    # Inicializa COM manualmente
    pythoncom.CoInitialize()

    # Cria arquivo temporário para salvar após macro
    temp_dir = tempfile.gettempdir()
    caminho_saida = os.path.join(temp_dir, 'arquivo_macro_temp.xlsx')

    try:
        excel = win32.gencache.EnsureDispatch('Excel.Application')
        excel.Visible = False
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
        wb.SaveAs(caminho_saida)

        df_resultante = pd.read_excel(caminho_saida, FileFormatt=52)
        return df_resultante

    finally:
        # Libera a COM
        ws = None
        wb = None
        excel.Quit()
        gc.collect()
        pythoncom.CoUninitialize()
