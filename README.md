
# 📊 Sistema de Processamento de Dados de Vendas

Aplicação web com **Python (Flask)** no backend e **Vue.js** no frontend, que processa arquivos **CSV** e **Excel** para análise de vendas, incluindo automação com **macro VBA** no Microsoft Excel.

---

## 🚀 Como Rodar o Projeto Localmente

### ✅ Pré-requisitos

Antes de começar, instale:

- 🐍 [Python 3.8+](https://www.python.org/downloads/)
- 🟢 [Node.js (LTS)](https://nodejs.org/en/download/)
- 📊 [Microsoft Excel](https://www.microsoft.com/pt-br/microsoft-365/excel) (para macro VBA)
- 🧰 [Git](https://git-scm.com/downloads)

---

## 💾 Instalação

### 1️⃣ Clonar o Repositório

```bash
git clone https://github.com/itstakas/Projeto_Vendas.git
cd PROJETO-VENDAS
```

---

### 2️⃣ Configurar o Backend (Python + Flask)

```bash
cd backend
```

#### a. Criar e ativar ambiente virtual

```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
```

#### b. Instalar dependências

```bash
pip install -r requirements.txt
```

> ⚠️ Se `requirements.txt` não existir, gere com:
> ```bash
> pip freeze > requirements.txt
> ```

#### c. Configurar caminho da macro VBA

Edite o caminho da macro no arquivo `routes/views.py`:

```python
caminho_macro = r'C:\SeuUsuario\Caminho\Macro - Troca de Data.xlsm'
```

📌 Dica: Use `r'caminho'` ou `\\` para evitar erros com barras invertidas.

---

### 3️⃣ Configurar o Frontend (Vue.js)

Abra outro terminal e vá até:

```bash
cd ../frontend
```

#### a. Instalar dependências

```bash
npm install
```

---

## ▶️ Executar o Sistema

### 🖥️ Backend

No terminal do `backend`:

```bash
python main.py
```

- Servidor Flask rodando em: [http://127.0.0.1:5000](http://127.0.0.1:5000)

### 🌐 Frontend

No terminal do `frontend`:

```bash
npm run dev
```

- Frontend acessível em: [http://localhost:5173](http://localhost:5173)

---

## 🔎 Como Usar

1. Acesse o frontend no navegador.
2. Envie os arquivos CSV e Excel pelos botões da interface.
3. O sistema processa os dados e exibe os resultados por vendedor.
4. Você pode baixar o relatório final em Excel.

---

## ⚠️ Limitações

- ❌ **Somente Windows:** O uso do `pywin32` exige Windows com Excel instalado.
- 🔧 **Caminho da macro deve ser configurado manualmente** por máquina.


## 🤝 Contribuindo

Contribuições são bem-vindas!

- 📌 Sugira melhorias via [Issues](https://github.com/itstakas/Projeto_Vendas/issues)
- 🔧 Envie um Pull Request
- ⭐ Dê uma estrela no projeto!

---

## 👤 Autor

Feito com ❤️ por **Leonardo Takeshi Rodrigues Maeda**

- 📫 Email: takeshileonardo.1@gmail.com
- 🔗 LinkedIn: https://www.linkedin.com/in/itstakas/
- 💻 GitHub: https://github.com/itstakas
---

> Este projeto é ideal para equipes comerciais que desejam automatizar relatórios de vendas com praticidade e organização.
