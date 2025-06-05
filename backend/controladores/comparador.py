from controladores.Classes import ProcessaDados
from rapidfuzz import fuzz #função fuzz da biblioteca rapidfuzz, utilizada para calcular similaridade entre strings
from datetime import date #função date para capturar a data atual
import pandas as pd 


def comparar_e_preencher(processador: ProcessaDados):
    # Cria dois conjuntos para armazenar os nomes que já foram comparados e utilizados
    nome_csv_usados = set()
    nome_excel_usados = set()
    # Define a data atual no objeto processador
    processador.data_atual = date.today()

    # Percorre cada linha do DataFrame Excel
    for idx_excel, row_excel in processador.excel_df.iterrows():
        # Extrai e padroniza o nome da linha do Excel (removendo espaços e deixando em maiúsculo)
        nome_excel = str(row_excel['NOME']).strip().upper()
        encontrado = False

         # Percorre cada linha do DataFrame CSV
        for idx_csv, row_csv in processador.csv_df.iterrows():
            # Extrai e padroniza o nome da linha do CSV
            nome_csv = str(row_csv['Id Cliente']).strip().upper()

            similaridade = fuzz.WRatio(nome_csv, nome_excel)  
            #print(f"Comparando: '{nome_excel}' <-> '{nome_csv}' => Similaridade: {similaridade}")

            # Se a similaridade for maior ou igual a 90, considera que os nomes correspondem
            if similaridade >= 93:
                # Preenche os campos do Excel com dados correspondentes do CSV
                processador.excel_df.at[idx_excel, 'CRM'] = nome_csv
                processador.excel_df.at[idx_excel, 'ESTADO'] = None
                processador.excel_df.at[idx_excel, 'VENDEDOR_TELE'] = row_csv['Unidade']
                processador.excel_df.at[idx_excel, 'CATEGORIA'] = row_csv['Data de criação']
                processador.excel_df.at[idx_excel, 'SUBCATEGORIA'] = row_csv['Origem (categoria)']
                encontrado = True
                if encontrado:
                    # adiciona os nomes conferidos em nome csv usados e esxel usados para comparativo mais tarde
                    nome_csv_usados.add(nome_csv)
                    nome_excel_usados.add(nome_excel)
                break

    # Se o nome do CSV já estiver presente no Excel, pula para o próximo    
    for idx_csv, row_csv in processador.csv_df.iterrows():
        nome_csv = str(row_csv['Id Cliente']).strip().upper()

        # ESSES DOIS IF PEGUEI DO CHAT, SE FUNCIONAR EU DOU UM MORTAL PRA TRAS
        if nome_csv not in nome_csv_usados:
            
            # Se o nome do CSV já estiver presente no Excel, pula para o próximo
            nomes_existentes = processador.excel_df['NOME'].astype(str).str.strip().str.upper()
            if nome_csv in nomes_existentes.values: 
                continue

           # Se o nome do CSV não está no Excel, cria uma nova linha com os dados mínimos
            nova_linha = pd.DataFrame([{

                'NOME': nome_csv,
                'VENDEDOR': None,
                'DATA_CONTRATO': processador.data_atual,
                'CATEGORIA': row_csv['Data de criação'],
                'SUBCATEGORIA': row_csv['Origem (categoria)'],
                'VENDEDOR_TELE': row_csv['Unidade'],
                'CRM': None,
                'ESTADO': None
            }])

            # Adiciona a nova linha ao final do DataFrame do Excel
            processador.excel_df = pd.concat([processador.excel_df, nova_linha], ignore_index=True)
            # Marca o nome como usado para evitar duplicatas
            nome_csv_usados.add(nome_csv) 
            print(f"Adicionando novo cliente: {nome_csv}")

    return processador
