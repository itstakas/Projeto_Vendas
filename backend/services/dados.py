import pandas as pd

def get_vendedores():
    return pd.read_excel('uploads/vendedores.xlsx')

def get_clientes():
    return pd.read_excel('uploads/clientes.xlsx')