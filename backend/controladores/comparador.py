from controladores.Classes import ProcessaDados
from rapidfuzz import fuzz, process
from datetime import date
import pandas as pd

def comparar_e_preencher(processador: ProcessaDados):
    processador.data_atual = date.today()
    
    # Pré-processamento: criar dicionários e conjuntos para acesso rápido
    csv_nomes = {str(nome).strip().upper(): idx 
                for idx, nome in enumerate(processador.csv_df['Cliente'])}
    excel_nomes = {str(nome).strip().upper(): idx 
                  for idx, nome in enumerate(processador.excel_df['NOME'])}
    
    # Conjuntos para controle
    nomes_csv_usados = set()
    nomes_excel_usados = set()

    # Primeira passada: encontrar correspondências com alta similaridade
    for nome_excel, idx_excel in excel_nomes.items():
        # Usa rapidfuzz.process para encontrar a melhor correspondência
        melhor_match = process.extractOne(
            nome_excel, 
            csv_nomes.keys(),
            scorer=fuzz.WRatio,
            score_cutoff=90  # Só considera matches com similaridade >= 90
        )
        
        if melhor_match:
            nome_csv, score, _ = melhor_match
            idx_csv = csv_nomes[nome_csv]
            
            # Atualiza o DataFrame do Excel
            row_csv = processador.csv_df.iloc[idx_csv]
            processador.excel_df.at[idx_excel, 'CRM'] = nome_csv
            processador.excel_df.at[idx_excel, 'ESTADO'] = None
            processador.excel_df.at[idx_excel, 'VENDEDOR_TELE'] = row_csv['Vendedor']
            processador.excel_df.at[idx_excel, 'CATEGORIA'] = row_csv['Origem (categoria)']
            processador.excel_df.at[idx_excel, 'SUBCATEGORIA'] = row_csv['Suborigem (subcategoria)']
            
            nomes_csv_usados.add(nome_csv)
            nomes_excel_usados.add(nome_excel)
    
    # Segunda passada: adicionar clientes não encontrados
    for nome_csv, idx_csv in csv_nomes.items():
        if nome_csv not in nomes_csv_usados and nome_csv not in excel_nomes:
            row_csv = processador.csv_df.iloc[idx_csv]
            
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
            
            processador.excel_df = pd.concat(
                [processador.excel_df, nova_linha], 
                ignore_index=True
            )
            print(f"Adicionando novo cliente: {nome_csv}")
    
    return processador