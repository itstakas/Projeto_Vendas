import pandas as pd
from datetime import datetime
from typing import Union, Optional
from pathlib import Path

class ProcessaDados:
    def __init__(self, csv_path: Union[str, Path], excel_path: Union[str, Path]):
        try:
            self.csv_df = pd.read_csv(csv_path, sep=";")
            self.excel_df = pd.read_excel(excel_path)
            
            self._validar_dataframes()
            self.filtrar_mes_atual()
            self.preencher_novas_colunas()
            
        except Exception as e:
            raise ValueError(f"Erro ao inicializar ProcessaDados: {str(e)}")

    def _validar_dataframes(self):
        """Verifica se os DataFrames têm as colunas necessárias"""
        colunas_csv_necessarias = ['Data de criação', 'Cliente', 'Vendedor', 
                                 'Origem (categoria)', 'Suborigem (subcategoria)']
        colunas_excel_necessarias = ['NOME']
        
        for col in colunas_csv_necessarias:
            if col not in self.csv_df.columns:
                raise ValueError(f"Coluna '{col}' não encontrada no CSV")
        
        for col in colunas_excel_necessarias:
            if col not in self.excel_df.columns:
                raise ValueError(f"Coluna '{col}' não encontrada no Excel")

    def filtrar_mes_atual(self):
        """Filtra o DataFrame para manter apenas registros do mês atual"""
        hoje = datetime.today()
        
        self.csv_df['Data de criação'] = pd.to_datetime(
            self.csv_df['Data de criação'], 
            format='%d/%m/%Y', 
            errors='coerce'
        )
        
        if self.csv_df['Data de criação'].isna().any():
            n_invalidas = self.csv_df['Data de criação'].isna().sum()
            print(f"Aviso: {n_invalidas} datas não puderam ser convertidas")
        
        mask = (
            (self.csv_df['Data de criação'].dt.month == hoje.month) & 
            (self.csv_df['Data de criação'].dt.year == hoje.year)
        )
        self.csv_df = self.csv_df[mask]
        
        if len(self.csv_df) == 0:
            print("Aviso: Nenhum dado encontrado para o mês atual")

    def preencher_novas_colunas(self):
        """Cria novas colunas no DataFrame do Excel com valores padrão"""
        self.excel_df['CRM'] = None
        self.excel_df['VENDEDOR_TELE'] = None
        self.excel_df['CATEGORIA'] = None
        self.excel_df['SUBCATEGORIA'] = None

    def salvar_excel_preenchido(self, caminho_saida: Union[str, Path]) -> None:
        """Salva o DataFrame em um arquivo Excel com configurações adicionais"""
        try:
            writer = pd.ExcelWriter(
                caminho_saida,
                engine='xlsxwriter',
                datetime_format='dd/mm/yyyy',
                date_format='dd/mm/yyyy'
            )
            
            self.excel_df.to_excel(writer, index=False, sheet_name='Dados')
            
            worksheet = writer.sheets['Dados']
            for i, col in enumerate(self.excel_df.columns):
                max_len = max((
                    self.excel_df[col].astype(str).map(len).max(),
                    len(str(col))
                )) + 2
                worksheet.set_column(i, i, max_len)
            
            writer.close()
            
        except Exception as e:
            raise IOError(f"Erro ao salvar arquivo Excel: {str(e)}")