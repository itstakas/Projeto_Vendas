import pandas as pd
from rapidfuzz import process, fuzz
from datetime import date

class ConciliadorVendas:
    """
    Responsavel por conciliar os dataframes do excel e CSV, atualizando clientes existentes e adicionando novos
    """
    def __init__(self, df_excel: pd.DataFrame, df_csv: pd.DataFrame):
        self.df_excel = df_excel.copy()
        self.df_csv = df_csv.copy()
        self.matches = {}

        def _normalizar_nomes(self):
            """
            Cria colunas temporarias com nomes normalizados para comparação
            """
            print("Normalizando nomes para comparação")
            self.df_excel['NOME_NORM']  = self.df_excel['NOME'].astype(str).str.strip().str.upper()
            self.df_csv['Id Cliente_NORM']  = self.df_csv['Id Cliente'].astype(str).str.strip().str.upper()

        def _encontrar_correspondentes(self, limite_similaridade=90):
            """
            Usa o rapidfuzz para encontrar correspondencias entre os nomes
            """

            print(f"Encontrando correspondencias com similaridade > {limite_similaridade}%")

            # Converte as colunas do excel e do csv para uma lista, dai ao inves de percorrer linha a linha de uma coluna, ele percorre a lista, fica muito mais rapido e leve
            nomes_excel = self.df_excel['NOME_NORM'].to_list() 
            nomes_csv = self.df_csv['Id Cliente_NORM'].unique().to_list()

            #lista para armazenar os nomes que são similares
            match_list = []

            # - extractOne: Pega o `nome_excel` e busca a UMA MELHOR correspondência para ele dentro da lista inteira de `nomes_csv`.

            # - scorer=fuzz.WRatio: Define o ALGORITMO que ele usa para calcular a "nota" de similaridade. O `WRatio` é ótimo para nomes, pois lida bem com palavras fora de ordem e pequenas diferenças.

            # - score_cutoff=limite_similaridade: É a "NOTA DE CORTE". A função só vai retornar um resultado se a nota de similaridade for maior ou igual a este valor (90). Caso contrário, retorna 'None'.

            for nome_excel in nomes_excel:
                best_match = process.extractOne(nome_excel, nomes_csv, scorer=fuzz.WRatio, score_cutoff=limite_similaridade)
                if best_match:
                    match_list.append((nome_excel, best_match[0]))



        
# #         # O dicionário mapeia o NOME_NORM do Excel para o NOME_NORM correspondente do CSV
# #         self.matches = dict(match_list)
# #         print(f"   {len(self.matches)} correspondências encontradas.")

# #     def _atualizar_clientes_existentes_vetorizado(self):
# #         """Atualiza os dados usando a abordagem vetorizada (rápida) do pandas."""
# #         print("-> Atualizando clientes existentes...")
# #         if not self.matches:
# #             print("   Nenhuma correspondência para atualizar.")
# #             return

# #         # Inverte o dicionário para mapear do CSV para o Excel, se necessário, ou usa como está
# #         mapa_excel_para_csv = pd.Series(self.matches)
# #         self.df_excel['csv_match'] = self.df_excel['NOME_NORM'].map(mapa_excel_para_csv)

# #         csv_mapeamento = self.df_csv.set_index('Id Cliente_NORM')
        
# #         # Mapeia as colunas usando o nome do CSV correspondente
# #         self.df_excel['VENDEDOR_TELE'] = self.df_excel['csv_match'].map(csv_mapeamento['Unidade'])
# #         self.df_excel['CATEGORIA'] = self.df_excel['csv_match'].map(csv_mapeamento['Data de criação'])
# #         self.df_excel['SUBCATEGORIA'] = self.df_excel['csv_match'].map(csv_mapeamento['Origem (categoria)'])
# #         self.df_excel['CRM'] = self.df_excel['csv_match'].map(csv_mapeamento['Id Cliente'])

# #     def _adicionar_novos_clientes(self):
# #         """Adiciona clientes que estão no CSV mas não tiveram correspondência no Excel."""
# #         print("-> Verificando novos clientes...")
# #         nomes_csv_matched = set(self.matches.values())
# #         todos_nomes_csv = set(self.df_csv['Id Cliente_NORM'].unique())
# #         novos_nomes_csv = todos_nomes_csv - nomes_csv_matched
        
# #         if not novos_nomes_csv:
# #             print("   Nenhum cliente novo para adicionar.")
# #             return

# #         novas_linhas = []
# #         # Filtra o df_csv de uma vez para pegar apenas as primeiras ocorrências dos novos nomes
# #         df_novos = self.df_csv[self.df_csv['Id Cliente_NORM'].isin(novos_nomes_csv)].drop_duplicates(subset=['Id Cliente_NORM'])

# #         for _, row_csv in df_novos.iterrows():
# #             novas_linhas.append({
# #                 'NOME': row_csv['Id Cliente'],
# #                 'DATA_CONTRATO': pd.to_datetime(date.today()),
# #                 'CATEGORIA': row_csv['Data de criação'],
# #                 'SUBCATEGORIA': row_csv['Origem (categoria)'],
# #                 'VENDEDOR_TELE': row_csv['Unidade'],
# #                 # Adicione outras colunas com None se precisar
# #             })

# #         if novas_linhas:
# #             novos_clientes_df = pd.DataFrame(novas_linhas)
# #             self.df_excel = pd.concat([self.df_excel, novos_clientes_df], ignore_index=True)
# #             print(f"   Adicionados {len(novas_linhas)} novos clientes.")

# #     def _limpar_colunas_temporarias(self):
# #         """Remove as colunas auxiliares usadas no processo."""
# #         print("-> Limpando colunas temporárias...")
# #         self.df_excel.drop(columns=['NOME_NORM', 'csv_match'], inplace=True, errors='ignore')

# #     def enriquecer_dados(self) -> pd.DataFrame:
# #         """
# #         Método principal que orquestra todo o processo de enriquecimento.
# #         """
# #         print("\nIniciando o enriquecimento de dados...")
# #         self._normalizar_nomes()
# #         self._encontrar_correspondencias()
# #         self._atualizar_clientes_existentes_vetorizado()
# #         self._adicionar_novos_clientes()
# #         self._limpar_colunas_temporarias()
# #         print("Enriquecimento concluído.\n")
# #         return self.df_excel