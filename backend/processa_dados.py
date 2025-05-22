from rapidfuzz import fuzz
import app
import pandas as pd
import os

print(os.path.exists("../uploads/csv.csv"))

# pega os arquivos da pasta upload
caminho_csv = "../uploads/csv.csv"
caminho_excel = "../uploads/Planilha1.xlsx"

# utiliza da biblioteca pandas para ler esse aquivos e armazena no df_excel e df_csv
df_csv = pd.read_csv(caminho_csv, sep=";")
df_excel = pd.read_excel(caminho_excel)

# ratio utiliza duas palavras chaves e compara as duas mostrando a taxa de sucesso
fuzz.ratio(df_csv['Cliente'], df_excel['NOME'])
print(ratio)