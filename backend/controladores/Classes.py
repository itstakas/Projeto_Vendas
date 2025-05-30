import pandas as pd
from datetime import datetime

# Classe que processa os dados do CSV e Excel
class ProcessaDados:
    # Método construtor: é executado ao criar uma nova instância da classe
    def __init__(self, csv_path, excel_path):
        self.csv_df = pd.read_csv(csv_path, sep=";") # Lê o arquivo CSV com separador ponto e vírgula e armazena no atributo csv_df
        self.excel_df = pd.read_excel(excel_path)   # Lê o arquivo Excel e armazena no atributo excel_df

        # Converte a coluna 'DATA_CONTRATO' e 'DATA_ADESAO' para tipo datetime (data), formatando como dia/mês/ano
        # 'errors="coerce"' converte valores inválidos em NaT (Not a Time)
        self.excel_df['DATA_CONTRATO'] = pd.to_datetime(self.excel_df['DATA_CONTRATO'], format='%d/%m/%Y', errors='coerce')
        self.excel_df['DATA_ADESAO'] = pd.to_datetime(self.excel_df['DATA_ADESAO'], format='%d/%m/%Y', errors='coerce')

        # Loop para verificar o tipo e o valor de cada data na coluna 'DATA_CONTRATO'
        for data in self.excel_df['DATA_CONTRATO']:
            print(f"Formato da data: {type(data)} | Valor: {data}")

        #------------------- AQUI VAI A FUNÇÃO PARA RODAR O MACRO ----------------------------

        # Chama o método para adicionar novas colunas ao DataFrame do Excel
        self.preencher_novas_colunas()
        
    def preencher_novas_colunas(self): # Método que adiciona colunas novas ao DataFrame do Excel, preenchidas com None (valores nulos)
        self.excel_df['CRM'] = None
        self.excel_df['VENDEDOR_TELE'] = None
        self.excel_df['CATEGORIA'] = None
        self.excel_df['SUBCATEGORIA'] = None

    # Método para salvar o DataFrame modificado em um novo arquivo Excel
    def salvar_excel_preenchido(self, caminho_saida):
        # Salva o DataFrame no caminho especificado, sem incluir o índice das linhas
        self.excel_df.to_excel(caminho_saida, index=False)
