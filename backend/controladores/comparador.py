from controladores.Classes import ProcessaDados
from rapidfuzz import fuzz
from datetime import date
import pandas as pd

def comparar_e_preencher(self):
    nome_csv_usados = set()
    nome_excel_usados = set()
    self.data_atual = date.today()
    data_em_texto = self.data_atual.strftime('%d/%m/%Y')

    for idx_excel, row_excel in self.excel_df.iterrows():
        nome_excel = str(row_excel['NOME']).strip().upper()
        encontrado = False

        for idx_csv, row_csv in self.csv_df.iterrows():
            nome_csv = str(row_csv['Cliente']).strip().upper()

            similaridade = fuzz.WRatio(nome_csv, nome_excel)  
            print(f"Comparando: '{nome_excel}' <-> '{nome_csv}' => Similaridade: {similaridade}")

            if similaridade >= 90:
                self.excel_df.at[idx_excel, 'CRM'] = nome_csv
                self.excel_df.at[idx_excel, 'ESTADO'] = None
                self.excel_df.at[idx_excel, 'VENDEDOR_TELE'] = row_csv['Vendedor']
                self.excel_df.at[idx_excel, 'CATEGORIA'] = row_csv['Data de criação']
                self.excel_df.at[idx_excel, 'SUBCATEGORIA'] = row_csv['Origem (categoria)']
                encontrado = True
                if encontrado:
                    # adiciona os nomes conferidos em nome csv usados e esxel usados para comparativo mais tarde
                    nome_csv_usados.add(nome_csv)
                    nome_excel_usados.add(nome_excel)
                break

            # if not encontrado:
            #     print(f"Cliente não encontrado: {nome_excel}")
        
    for idx_csv, row_csv in self.csv_df.iterrows():
        nome_csv = str(row_csv['Cliente']).strip().upper()

        # ESSES DOIS IF PEGUEI DO CHAT, SE FUNCIONAR EU DOU UM MORTAL PRA TRAS
        if nome_csv not in nome_csv_usados:

            nomes_existentes = self.excel_df['NOME'].astype(str).str.strip().str.upper()
            if nome_csv in nomes_existentes.values: 
                continue

            # ADICIONAR OS NOMES DE CSV QUE Ñ ESTÃO NO EXCEL, NO FINAL DO EXCEL, PQ Ñ DEU TEMPO DO CADASTRO
            # FINALIZAR
            nova_linha = pd.DataFrame([{
                'NOME': nome_csv,
                'VENDEDOR': None,
                'DATA_CONTRATO': data_em_texto,
                'CATEGORIA': row_csv['Data de criação'],
                'SUBCATEGORIA': row_csv['Origem (categoria)'],
                'VENDEDOR_TELE': row_csv['Vendedor'],
                'CRM': None,
                'ESTADO': None
            }])

            # PD CONCAT É PRA CONCATENAR O EXCEL COM O CODIGO DIGITADO ACIMA
            self.excel_df = pd.concat([self.excel_df, nova_linha], ignore_index=True)
            nome_csv_usados.add(nome_csv) #MARCA COMO USADO PARA NÃO REPETIR
            print(f"Adicionando novo cliente: {nome_csv}")
