from controladores.Classes import ProcessaDados
from rapidfuzz import fuzz
from datetime import date
import pandas as pd


def comparar_e_preencher(processador: ProcessaDados):
    nome_csv_usados = set()
    nome_excel_usados = set()
    processador.data_atual = date.today()

    for idx_excel, row_excel in processador.excel_df.iterrows():
        nome_excel = str(row_excel['NOME']).strip().upper()
        encontrado = False

        for idx_csv, row_csv in processador.csv_df.iterrows():
            nome_csv = str(row_csv['Id Cliente']).strip().upper()

            similaridade = fuzz.WRatio(nome_csv, nome_excel)  
            print(f"Comparando: '{nome_excel}' <-> '{nome_csv}' => Similaridade: {similaridade}")

            if similaridade >= 90:
                processador.excel_df.at[idx_excel, 'CRM'] = nome_csv
                processador.excel_df.at[idx_excel, 'ESTADO'] = None
                processador.excel_df.at[idx_excel, 'VENDEDOR_TELE'] = row_csv['Vendedor']
                processador.excel_df.at[idx_excel, 'CATEGORIA'] = row_csv['Origem (categoria)']
                processador.excel_df.at[idx_excel, 'SUBCATEGORIA'] = row_csv['Suborigem (subcategoria)']
                encontrado = True
                if encontrado:
                    # adiciona os nomes conferidos em nome csv usados e esxel usados para comparativo mais tarde
                    nome_csv_usados.add(nome_csv)
                    nome_excel_usados.add(nome_excel)
                break
        
    for idx_csv, row_csv in processador.csv_df.iterrows():
        nome_csv = str(row_csv['Id Cliente']).strip().upper()

        # ESSES DOIS IF PEGUEI DO CHAT, SE FUNCIONAR EU DOU UM MORTAL PRA TRAS
        if nome_csv not in nome_csv_usados:

            nomes_existentes = processador.excel_df['NOME'].astype(str).str.strip().str.upper()
            if nome_csv in nomes_existentes.values: 
                continue

            # ADICIONAR OS NOMES DE CSV QUE Ñ ESTÃO NO EXCEL, NO FINAL DO EXCEL, PQ Ñ DEU TEMPO DO CADASTRO
            # FINALIZAR
            nova_linha = pd.DataFrame([{

                'NOME': nome_csv,
                'VENDEDOR': None,
                'DATA_CONTRATO': processador.data_atual,
                'CATEGORIA': row_csv['Origem (categoria)'],
                'SUBCATEGORIA': row_csv['Suborigem (subcategoria)'],
                'VENDEDOR_TELE': row_csv['Vendedor'],
                'CRM': None,
                'ESTADO': None
            }])

            # PD CONCAT É PRA CONCATENAR O EXCEL COM O CODIGO DIGITADO ACIMA
            processador.excel_df = pd.concat([processador.excel_df, nova_linha], ignore_index=True)
            nome_csv_usados.add(nome_csv) #MARCA COMO USADO PARA NÃO REPETIR
            print(f"Adicionando novo cliente: {nome_csv}")

    return processador
