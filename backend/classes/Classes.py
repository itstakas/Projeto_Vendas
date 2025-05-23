import pandas as pd
from rapidfuzz import fuzz

class ProcessaDados:
    def __init__(self, csv_path, excel_path):
        self.csv_df = pd.read_csv(csv_path, sep=";")
        self.excel_df = pd.read_excel(excel_path)
        self.preencher_novas_colunas()

    def preencher_novas_colunas(self):
        self.excel_df['CRM'] = None
        self.excel_df['VENDEDOR_TELE'] = None
        self.excel_df['CATEGORIA'] = None
        self.excel_df['SUBCATEGORIA'] = None

    def comparar_e_preencher(self):
        for idx_excel, row_excel in self.excel_df.iterrows():
            nome_excel = str(row_excel['NOME'])
            encontrado = False

            for idx_csv, row_csv in self.csv_df.iterrows():
                nome_csv = str(row_csv['Cliente'])

                similaridade = fuzz.ratio(nome_excel, nome_csv)

                if similaridade >= 80:
                    self.excel_df.at[idx_excel, 'CRM'] = nome_csv
                    self.excel_df.at[idx_excel, 'VENDEDOR_TELE'] = row_csv['Vendedor']
                    self.excel_df.at[idx_excel, 'CATEGORIA'] = row_csv['Origem (categoria)']
                    self.excel_df.at[idx_excel, 'SUBCATEGORIA'] = row_csv['Suborigem (subcategoria)']
                    encontrado = True
                    break

            if not encontrado:
                print(f"Cliente não encontrado: {nome_excel}")

    def salvar_excel_preenchido(self, caminho_saida):
        self.excel_df.to_excel(caminho_saida, index=False)