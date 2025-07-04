# Arquivo: backend/controladores/comparador.py
from .processador_vendas import ProcessaDados
from rapidfuzz import process, fuzz
from datetime import date
import pandas as pd

def comparar_e_preencher(processador: ProcessaDados):
    print("Iniciando a comparação otimizada de dados...")
    
    # Garante que as colunas de nome sejam do tipo string para evitar erros
    processador.excel_df['NOME_NORM'] = processador.excel_df['NOME'].astype(str).str.strip().str.upper()
    processador.csv_df['Id Cliente_NORM'] = processador.csv_df['Id Cliente'].astype(str).str.strip().str.upper()

    # --- Otimização 1: Encontrar correspondências de uma vez ---
    # Em vez de loops aninhados, usamos o rapidfuzz para encontrar a melhor correspondência
    # para cada nome do Excel na lista de nomes do CSV.
    
    limite_similaridade = 90
    matches = []
    
    # Pega as listas de nomes normalizados
    nomes_excel = processador.excel_df['NOME_NORM'].tolist()
    nomes_csv = processador.csv_df['Id Cliente_NORM'].unique().tolist()

    # Usa o process.extract para encontrar as melhores correspondências
    # Isso é muito mais rápido que um loop for dentro de outro.
    for nome_excel in nomes_excel:
        # Encontra o melhor match para o nome do excel na lista de nomes do csv
        best_match = process.extractOne(nome_excel, nomes_csv, scorer=fuzz.WRatio, score_cutoff=limite_similaridade)
        if best_match:
            # Se encontrou um match bom, guarda o par (nome_excel, nome_csv)
            matches.append((nome_excel, best_match[0]))

    # Converte os matches para um dicionário para busca rápida: {nome_csv: nome_excel}
    match_dict_csv_to_excel = {csv_name: excel_name for excel_name, csv_name in matches}
    
    # Atualiza o DataFrame do Excel com os dados do CSV onde houve match
    for _, row_csv in processador.csv_df.iterrows():
        nome_csv_norm = row_csv['Id Cliente_NORM']
        if nome_csv_norm in match_dict_csv_to_excel:
            nome_excel_correspondente = match_dict_csv_to_excel[nome_csv_norm]
            # Encontra o índice no excel_df para atualizar
            idx_excel = processador.excel_df[processador.excel_df['NOME_NORM'] == nome_excel_correspondente].index
            if not idx_excel.empty:
                processador.excel_df.loc[idx_excel, 'CRM'] = row_csv['Id Cliente']
                processador.excel_df.loc[idx_excel, 'VENDEDOR_TELE'] = row_csv['Unidade']
                processador.excel_df.loc[idx_excel, 'CATEGORIA'] = row_csv['Data de criação']
                processador.excel_df.loc[idx_excel, 'SUBCATEGORIA'] = row_csv['Origem (categoria)']

    # --- Otimização 2: Adicionar novos clientes de forma eficiente ---
    
    # Pega todos os nomes que já existem no Excel (depois dos matches)
    nomes_existentes_set = set(processador.excel_df['NOME_NORM'])
    
    # Pega os nomes do CSV que não tiveram correspondência
    nomes_csv_matched = set(match_dict_csv_to_excel.keys())
    novos_nomes_csv = set(processador.csv_df['Id Cliente_NORM'].unique()) - nomes_csv_matched
    
    novas_linhas = []
    for nome_novo in novos_nomes_csv:
        if nome_novo not in nomes_existentes_set:
            # Pega a primeira linha do CSV correspondente a este novo nome
            row_csv = processador.csv_df[processador.csv_df['Id Cliente_NORM'] == nome_novo].iloc[0]
            novas_linhas.append({
                'NOME': row_csv['Id Cliente'],
                'VENDEDOR': None,
                'DATA_CONTRATO': pd.to_datetime(date.today()),
                'CATEGORIA': row_csv['Data de criação'],
                'SUBCATEGORIA': row_csv['Origem (categoria)'],
                'VENDEDOR_TELE': row_csv['Unidade'],
                'CRM': None,
                'ESTADO': None
            })

    # Adiciona todas as novas linhas de uma só vez no final
    if novas_linhas:
        novos_clientes_df = pd.DataFrame(novas_linhas)
        processador.excel_df = pd.concat([processador.excel_df, novos_clientes_df], ignore_index=True)
        print(f"Adicionados {len(novas_linhas)} novos clientes.")

    # Remove a coluna temporária
    processador.excel_df.drop(columns=['NOME_NORM'], inplace=True)
    
    print("Comparação e preenchimento otimizados concluídos.")
    return processador
