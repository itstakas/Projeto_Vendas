import pandas as pd

# CLASSE FEITA POR I.A, SE DER CERTO DOU UM MORTAL PRA TRAS
class DataCorreta:
    def __init__(self, ano='2025'):
        self.substituicoes = self.troca_data(ano)

    def troca_data(self, ano):
        substituicoes = {}
        for dia in range (1, 31):
            for mes in range (1,12):
                dd = f"{dia:02d}"
                mm = f"{mes:02d}"
                original = f"{mm}/{dd}/{ano}"
                corrigido = f"{dd}/{mm}/{ano}"
                substituicoes[original] = corrigido
        return substituicoes

    def corrigir_coluna(self, df, coluna):
         # Primeiro converte para string
        df[coluna] = df[coluna].astype(str)
        # Substitui strings mm/dd/yyyy -> dd/mm/yyyy
        df[coluna] = df[coluna].apply(lambda x: self.substituicoes.get(x.strip(), x.strip()) if pd.notnull(x) else x)
        return df
