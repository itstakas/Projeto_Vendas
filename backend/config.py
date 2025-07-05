# ==============================================================================
# ARQUIVO CENTRAL DE CONFIGURAÇÕES DO PROJETO
# ==============================================================================


# Este é o "painel de controle" da aplicação. Se qualquer nome de coluna, lista de exclusão ou valor fixo precisar mudar, altere APENAS AQUI, sem precisar mexer no resto do código.

# --- MAPEAMENTO DE COLUNAS CRÍTICAS ---
# Aqui, "traduzimos" os nomes exatos das colunas dos seus arquivos originais para variáveis que o nosso programa entende. Se um dia o nome de uma coluna no seu Excel ou CSV mudar, você só precisa corrigir o texto aqui.

# Colunas do arquivo Excel de entrada
COLUNA_NOME_EXCEL = 'NOME'
COLUNA_DATA_CONTRATO_EXCEL = 'DATA_CONTRATO'
COLUNA_DATA_ADESAO_EXCEL = 'DATA ADESAO'
COLUNA_VENDEDOR_EXCEL = 'VENDEDOR'

# Colunas do arquivo CSV de entrada
COLUNA_ID_CLIENTE_CSV = 'Id Cliente'
COLUNA_UNIDADE_CSV = 'Unidade'
COLUNA_DATA_CRIACAO_CSV = 'Data de criação'
COLUNA_ORIGEM_CSV = 'Origem (categoria)'
COLUNA_RESPONSAVEL_CSV = 'Responsável por indicar'


# --- LISTAS PARA PROCESSAMENTO E LIMPEZA --- FAZER DE FORMA DINAMICA DEPOIS
# Estas listas controlam o que será removido durante a "faxina" dos dados.

# Lista de colunas que serão completamente apagadas do relatório final.
COLUNAS_PARA_REMOVER = [
    'DATA_CADASTRO',
    'ULTIMO_PAGAMENTO',
    'ULT_MES_REF_PAGO',
    'PAGOU',
    'EM_ATRASO',
    'DATA_CONFIRMACAO',
    'VALOR_CONFIRM',
    'ENDERECO_COB'
]

# "Lista Negra": qualquer cliente cujo nome esteja aqui será removido do relatório.
NOMES_EXCLUIR = {
    'DORALINA', 'MARINALVA DE OLIVEIRA SOBRINHO', 'JENIFER GABRIELLY DE ARAUJO REQUENA',
    'LUCIANA BRITES DO NASCIMENTO', 'VILMA DE ARAUJOEPHANIE LOREN PUERTA COSME', 'FELIPE TOMPOROSKI PEREZ',
    'JULIANA PIMENTEL MOLINA FIEL', 'FABIANA DIAS BARROSO', 'SILVIO ALEXANDRE LOPES FORTALEZA',
    'ROSENI MARTINS DOS SANTOS', 'VILMAR PEREIRA DE JESUS', 'KHISLEY MARESSA SILVA DIAS',
    'MARIA DE FÁTIMA RAMOS DA SILVA OLIVEIRA', 'GEANNE DA SILVA BORGES', 'SANDRA MARIA DA SILVA SANTOS',
    'MILCE FERREIRA DA COSTA', 'THAÍS FONTANA DA CUNHA', 'GISLAINE LOPES DA SILVA',
    'LUCAS HENRIQUE', 'SÔNIA GREFFE CHAVES'
}


# --- LISTAS PARA ADIÇÃO MANUAL E CLASSIFICAÇÃO ---  FAZER DE FORMA DINAMICA DEPOIS
# Estas listas adicionam informações novas ou categorizam as existentes.

# Lista de clientes que serão adicionados ao final do relatório, "na mão".
NOVOS_CLIENTES_MANUAIS = [
    {"NOME": "NAIANNNY GUERRIERI", "VENDEDOR_TELE": "Lucas Dos Santos Delgado", "DATA_CONTRATO": "06/06/2025"},
    {"NOME": "LUIZ HENRIQUE AGUIAR", "VENDEDOR_TELE": "Sheila Licia Nascimento Silva", "DATA_CONTRATO": "06/06/2025"}
]

# Lista usada para classificar os vendedores do tipo "Porta a Porta".
NOMES_PORTA_A_PORTA = [
    "GLEICI IDALINA PEREIRA RUIZ", "VEND.SILAS DE OLIVEIRA", "MARIA ROSELI",
    "ANA BEATRIZ DO PRADO SCAVONE", "ELIZABETE ALVES", "TALITA JUNIA DA CONCEICAO SILVA"
]

# Lista usada para classificar os vendedores do tipo "Externa".
NOMES_EXTERNA = [
    "ANDRE MENOSSI", "MARIO ANTONIO DELGADO MOREL", "NATANAEL DE SOUZA BRASIL",
    "ANA GRACIELA BENITEZ", "DIANA ELIZABETH FERREIRA PALACIOS", "DEMETRIO FIDEL INSFRAN BALBUENA"
]
