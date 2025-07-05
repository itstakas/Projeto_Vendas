Sistema de Processamento e Análise de Vendas
Este projeto é uma aplicação web full-stack que combina um backend em Python (Flask) e um frontend em Vue.js para processar, corrigir e analisar dados de vendas a partir de arquivos CSV e Excel. A aplicação está hospedada na web e pode ser acessada publicamente.

➡️ Acessar a Aplicação Web

✨ Principais Funcionalidades
Upload de Arquivos: Interface amigável para o upload de arquivos de vendas (CSV) e de base de clientes (Excel).

Processamento de Dados: Lógica de backend robusta que limpa, compara e enriquece os dados, utilizando a biblioteca Pandas.

Correção Inteligente de Datas: Implementa uma rotina de parsing customizada para corrigir e padronizar datas com formatos inconsistentes (DD/MM/AAAA vs. MM/DD/AAAA) diretamente na fonte.

Visualização Interativa: O frontend em Vue.js exibe os dados processados em tempo real, permitindo a filtragem e a visualização de detalhes de vendedores.

Deploy Contínuo: A aplicação é automaticamente atualizada na web a cada novo push para a branch main no GitHub, utilizando um pipeline de CI/CD configurado no Render.

🛠️ Tecnologias Utilizadas
Categoria

Tecnologias

Backend

Python, Flask, Pandas, Openpyxl, Gunicorn, RapidFuzz, Pytest

Frontend

JavaScript, Vue.js, Axios, Tailwind CSS

Deploy

Render, Git, GitHub

🚀 Como Rodar o Projeto Localmente (Para Desenvolvedores)
Siga estas instruções para configurar e executar o sistema em sua máquina para desenvolvimento.

Pré-requisitos
Python 3.8+ e pip.

Node.js (LTS) e npm.

Git para clonar o repositório.

💾 Instalação e Configuração
Execute os comandos no seu terminal (PowerShell, CMD, Git Bash, etc.).

1. Clonar o Repositório
git clone https://github.com/itstakas/Projeto_Vendas.git
cd Projeto_Vendas

2. Configurar o Backend (Python)
Abra um terminal na pasta raiz do projeto (Projeto_Vendas).

a. Criar e Ativar o Ambiente Virtual
É uma boa prática isolar as dependências do projeto.

# Criar o ambiente virtual (só precisa fazer isso uma vez)
python -m venv venv

# Ativar o ambiente virtual (precisa fazer toda vez que for trabalhar no projeto)
# No Windows (PowerShell):
.\venv\Scripts\activate

Nota: Se o comando de ativação der erro no PowerShell, execute Set-ExecutionPolicy RemoteSigned -Scope Process primeiro e tente novamente.

b. Instalar Dependências do Python
Com o ambiente (venv) ativo, instale as bibliotecas necessárias.

pip install -r backend/requirements.txt

3. Configurar o Frontend (Vue.js)
Abra um novo terminal, separado do terminal do backend.

a. Navegar até a Pasta do Frontend

cd frontend

b. Instalar Dependências do JavaScript

npm install

▶️ Rodar a Aplicação (Modo de Desenvolvimento)
Agora você precisa de dois terminais abertos para rodar a aplicação completa.

1. Iniciar o Backend (Terminal 1)

Verifique se você está na pasta raiz (Projeto_Vendas) e se o ambiente (venv) está ativo.

Execute o comando:

# Usamos -m para rodar o backend como um pacote, o que resolve os imports.
python -m backend.main

O servidor Flask iniciará em http://127.0.0.1:5000.

2. Iniciar o Frontend (Terminal 2)

Verifique se você está na pasta frontend.

Execute o comando:

npm run dev

O servidor de desenvolvimento do Vue (Vite) iniciará, geralmente em http://localhost:5173, e abrirá o site no seu navegador automaticamente.

Agora você pode fazer alterações no código e ver as atualizações na tela em tempo real.

☁️ Sobre o Deploy
Este projeto é configurado para deploy contínuo na plataforma Render. O arquivo render.yaml na raiz do projeto contém todas as instruções de build e start. Qualquer push para a branch main no GitHub irá disparar um novo deploy automaticamente.

📁 Estrutura do Projeto (Refatorada)
/Projeto_Vendas
├── backend/                        # Contém toda a lógica Python (Flask)
│   ├── processamento_de_dados/     # Classes para limpeza e preparação inicial dos dados
│   ├── routes/                     # Definição das rotas da API (o "garçom")
│   ├── services/                   # O "cérebro": lógica de negócio e orquestração
│   ├── tests/                      # Testes automatizados para garantir a qualidade
│   ├── utils/                      # Ferramentas pequenas e reutilizáveis
│   ├── config.py                   # Painel de controle: todas as configurações
│   └── main.py                     # Ponto de entrada que inicia o servidor
├── frontend/                       # Contém toda a interface (Vue.js)
│   └── ...
├── .gitignore                      # Arquivo que diz ao Git o que ignorar
├── render.yaml                     # Manual de instruções para o deploy no Render
└── ...
