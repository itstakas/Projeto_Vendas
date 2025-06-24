
-----

````markdown
# Sistema de Processamento de Dados de Vendas

Este projeto é uma aplicação web que combina um backend em Python (Flask) e um frontend em Vue.js para processar e analisar dados de vendas a partir de arquivos CSV e Excel.

## 🚀 Como Rodar o Projeto Localmente (Para Desenvolvedores)

Siga estas instruções para configurar e executar o sistema em sua máquina para desenvolvimento.

### Pré-requisitos

Para desenvolvimento, você precisará ter o seguinte software instalado:

* **Python 3.8+**: [Baixar Python](https://www.python.org/downloads/)
* **Node.js (LTS recomendado)** e **NPM** (gerenciador de pacotes que vem com o Node.js): [Baixar Node.js](https://nodejs.org/en/download/)
* **Microsoft Excel**: Essencial para a funcionalidade de automação de macro VBA.
* **Git**: Para clonar o repositório. [Baixar Git](https://git-scm.com/downloads)

### 💾 Instalação e Configuração

Siga os passos abaixo, executando os comandos no seu terminal (Prompt de Comando ou PowerShell no Windows, Terminal no macOS/Linux).

#### 1. Clonar o Repositório

Primeiro, clone o projeto para sua máquina local:

```bash
git clone https://github.com/itstakas/Projeto_Vendas.git
cd PROJETO-VENDAS
````

#### 2\. Configurar o Backend (Python)

Navegue até o diretório do backend:

```bash
cd backend

**a. Instalar Dependências do Python**

Com o ambiente virtual ativado, instale as bibliotecas Python necessárias:

```bash
pip install -r requirements.txt
```

> **Nota:** Se você não tiver o arquivo `requirements.txt` ainda, você precisará criá-lo no seu ambiente de desenvolvimento original usando `pip freeze > requirements.txt` na pasta `backend` **com seu ambiente virtual ativado**.

**b. Preparar Arquivos Essenciais**

  * **Copiar a Macro:** Copie o arquivo da macro `Macro - Troca de Data.xlsm` para a pasta `backend` (junto com `main.py`).

**c. Configurar o Caminho da Macro (Atenção\!)**

Este projeto utiliza uma macro VBA em Excel. Você precisará ajustar o caminho no código do backend:

1.  Abra o arquivo `views.py` (localizado em `backend/routes/views.py`) em um editor de texto.
2.  Encontre a linha que define `application_path` dentro do bloco `else` (aproximadamente na linha 20):
    ```python
    else:
        application_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
    ```
    Garanta que ela esteja configurada para apontar para o diretório `backend` em ambiente de desenvolvimento.

#### 3\. Configurar o Frontend (Vue.js)

Abra um **NOVO terminal** e navegue até o diretório do frontend:

```bash
cd frontend
```

**a. Instalar Dependências do JavaScript**

Instale os pacotes Node.js/JavaScript necessários para o frontend:

```bash
npm install
```

> **Nota:** Certifique-se de que o arquivo `package.json` exista na raiz da pasta `frontend`.

**b. Construir o Frontend para Produção**

Gere os arquivos estáticos otimizados do frontend. Isso é crucial para o empacotamento do executável:

```bash
npm run build
```

### ▶️ Rodar a Aplicação (Modo de Desenvolvimento)

Com ambos os terminais nas respectivas pastas (`backend` e `frontend`), e todas as dependências instaladas, você pode iniciar o servidor e o frontend.

#### 1\. Iniciar o Backend

No terminal da pasta `backend` (com o ambiente virtual Python ativado):

```bash
python main.py
```

Você verá mensagens indicando que o servidor Flask está rodando (geralmente em `http://127.0.0.1:5000/`) e o navegador abrirá automaticamente.

#### 2\. Iniciar o Frontend (Não é necessário executar `npm run dev` separadamente se o Flask estiver servindo)

Após iniciar o backend e o navegador abrir, o frontend será servido pelo Flask.

-----

## 📦 Como Usar o Aplicativo Empacotado (Para Usuários Finais)

Para usuários finais, o projeto pode ser distribuído como um único arquivo executável para Windows.

### Pré-requisitos para o Usuário

  * **Sistema Operacional Windows:** O aplicativo é compatível apenas com Windows.
  * **Microsoft Excel Instalado:** **Essencial** para a funcionalidade de processamento de macro VBA. Sem ele, a parte principal do processamento falhará.
  * **Navegador Web Padrão:** Para acessar a interface do usuário.

### 💾 Instalação e Execução

1.  **Baixar o Executável atraves do link:** https://drive.google.com/file/d/1G_crTpWZwxADoUV-K7pF8yxXHT9Kfa1h/view?usp=sharing
      * **Atenção:** Seu navegador e/ou antivírus podem exibir avisos de segurança ao baixar e executar arquivos `.exe` não assinados. Isso é normal para aplicativos empacotados com PyInstaller. Você pode precisar clicar em "Manter", "Executar mesmo assim" ou "Mais informações" \> "Executar".
2.  **Executar o Aplicativo:** Dê um duplo clique no arquivo `main.exe`.
3.  **Acesso à Interface:**
      * Uma janela de console **aparecerá**
      * Seu navegador web padrão abrirá automaticamente a interface do aplicativo em `http://127.0.0.1:5000/`.
4.  **Local dos Arquivos:** O aplicativo criará uma pasta `uploads_app` no mesmo diretório do executável (`main.exe`) para armazenar os arquivos enviados e o `resultado.xlsx`.

### 🛑 Como Encerrar o Aplicativo

Fecha a janela de console que o aplicativo irá fechar.

-----

## ⚠️ Limitações Importantes

  * **Compatibilidade com Windows:** Devido ao uso de automação de macro VBA do Microsoft Excel (`pywin32`), o backend só pode ser executado em **sistemas operacionais Windows**.
  * **Dependência do Excel:** O Microsoft Excel **precisa estar instalado** na máquina para que a funcionalidade da macro seja executada.

-----

## 🛠️ Contribuição (Opcional)

Se você deseja contribuir para o desenvolvimento deste projeto, sinta-se à vontade para abrir issues, enviar pull requests ou entrar em contato.

```
```