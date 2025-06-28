# Arquivo: controladores/Classes.py
import pandas as pd
import os

class ProcessaDados:
    def __init__(self, csv_path, excel_path):
        print("Iniciando carregamento e correção inteligente de datas...")
        
        # PASSO 1: Carrega os arquivos, mantendo as datas como texto por enquanto
        self.csv_df = pd.read_csv(csv_path, sep=";", encoding='utf-8-sig', on_bad_lines='skip')
        self.excel_df = pd.read_excel(excel_path, dtype=str)

        # PASSO 2: A FUNÇÃO DE CORREÇÃO INTELIGENTE (A "MACRO" EM PYTHON)
        def corrigir_data_inteligente(data_str):
            # Se a célula estiver vazia, retorna um valor nulo de data
            if pd.isna(data_str):
                return pd.NaT

            data_str = str(data_str).split(' ')[0] # Pega apenas a parte da data, ignorando horas

            try:
                # Tenta ler no formato universal AAAA-MM-DD
                # Ex: '2025-03-06'
                dia = int(data_str[8:10])
                mes = int(data_str[5:7])
                
                # A REGRA: Se o que parece ser o dia (ex: 06) for menor que 13,
                # e o que parece ser o mês (ex: 03) também, é uma data ambígua.
                # Neste caso, a regra de negócio é que eles foram invertidos.
                if dia <= 12 and mes <= 12:
                    # Inverte dia e mês para corrigir
                    return pd.to_datetime(f"{mes}/{dia}/{data_str[:4]}", format='%d/%m/%Y')
                else:
                    # Se não for ambíguo (ex: 2025-06-20), confia no formato
                    return pd.to_datetime(data_str)

            except (ValueError, TypeError, IndexError):
                # Se não for no formato AAAA-MM-DD, tenta o formato brasileiro
                try:
                    return pd.to_datetime(data_str, format='%d/%m/%Y')
                except (ValueError, TypeError):
                    # Se falhar em todos os formatos, marca como data inválida
                    return pd.NaT

        # PASSO 3: Aplica a correção em todas as colunas de data
        print("Aplicando correção inteligente nas colunas de data...")
        for col in ['DATA_CONTRATO', 'DATA_ADESAO']:
            if col in self.excel_df.columns:
                self.excel_df[col] = self.excel_df[col].apply(corrigir_data_inteligente)
        
        print(f"Tipo final da coluna DATA_CONTRATO: {self.excel_df['DATA_CONTRATO'].dtype}")

        self.preencher_novas_colunas()
        print("Inicialização concluída. Todas as datas foram corrigidas.")

    def preencher_novas_colunas(self):
        self.excel_df['CRM'] = None
        self.excel_df['VENDEDOR_TELE'] = None
        self.excel_df['CATEGORIA'] = None
        self.excel_df['SUBCATEGORIA'] = None

    def salvar_excel_preenchido(self, caminho_saida):
        df_para_salvar = self.excel_df.copy()
        for col in ['DATA_CONTRATO', 'DATA_ADESAO']:
            if col in df_para_salvar.columns and pd.api.types.is_datetime64_any_dtype(df_para_salvar[col]):
                df_para_salvar[col] = df_para_salvar[col].dt.strftime('%d/%m/%Y').replace('NaT', '')
        
        df_para_salvar.to_excel(caminho_saida, index=False, engine='xlsxwriter')
        print(f"Arquivo salvo em: {caminho_saida}")
