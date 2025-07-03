# Arquivo: controladores/Classes.py
import pandas as pd
import os

class ProcessaDados:
    def preencher_novas_colunas(self):
        self.excel_df['CRM'] = None
        self.excel_df['VENDEDOR_TELE'] = None
        self.excel_df['CATEGORIA'] = None
        self.excel_df['SUBCATEGORIA'] = None

    def salvar_excel_preenchido(self, caminho_saida):
        df_para_salvar = self.excel_df.copy()
        for col in ['DATA_CONTRATO', 'DATA_ADESAO']:
            if col in df_para_salvar.columns and pd.api.types.is_datetime64_any_dtype(df_para_salvar[col]):
                df_para_salvar[col] = df_para_salvar[col].dt.strftime('%d/%m/%Y').replace('NaT', '')
        
        df_para_salvar.to_excel(caminho_saida, index=False, engine='xlsxwriter')
        print(f"Arquivo salvo em: {caminho_saida}")
