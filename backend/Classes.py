import pandas as pd
from rapidfuzz import fuzz
from datetime import date

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
            nome_excel = str(row_excel['NOME']).strip().upper()
            encontrado = False

            self.data_atual = date.today()
            data_em_texto = self.data_atual.strftime('%d/%m/%Y')

            for idx_csv, row_csv in self.csv_df.iterrows():
                nome_csv = str(row_csv['Id Cliente']).strip().upper()

                similaridade = fuzz.WRatio(nome_csv, nome_excel)
                print(f"Comparando: '{nome_excel}' <-> '{nome_csv}' => Similaridade: {similaridade}")

                if similaridade >=90:
                    self.excel_df.at[idx_excel, 'CRM'] = nome_csv
                    self.excel_df.at[idx_excel,
                                     'VENDEDOR_TELE'] = row_csv['Vendedor']
                    self.excel_df.at[idx_excel,
                                     'CATEGORIA'] = row_csv['Data de criação']
                    self.excel_df.at[idx_excel,
                                     'SUBCATEGORIA'] = row_csv['Origem (categoria)']
                    encontrado = True
                    break

            if not encontrado:
                nova_linha = pd.DataFrame ([{
                    'NOME': nome_csv,
                    'VENDEDOR': None,
                    'DATA_CONTRATO': data_em_texto,
                    'CATEGORIA': row_csv['Data de criação'],
                    'SUBCATEGORIA': row_csv['Origem (categoria)'],
                    'VENDEDOR_TELE': row_csv['Vendedor']
                }])

                self.excel_df = pd.concat([self.excel_df, nova_linha], ignore_index=True)
                print(f"Cliente não encontrado: {nome_excel}")

    def salvar_excel_preenchido(self, caminho_saida):
        self.excel_df.to_excel(caminho_saida, index=False)
