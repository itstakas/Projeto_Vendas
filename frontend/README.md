# Vue 3 + Vite

This template should help get you started developing with Vue 3 in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

Learn more about IDE Support for Vue in the [Vue Docs Scaling up Guide](https://vuejs.org/guide/scaling-up/tooling.html#ide-support).



# Projeto Upload e Processamento de Arquivos CSV e Excel

## Descrição

Esta aplicação web permite o upload simultâneo de arquivos CSV e Excel, processa os dados no backend com Flask e Python, realiza comparações e filtragens, e gera um arquivo Excel preenchido para download no frontend.

## Tecnologias utilizadas

- Backend: Python 3, Flask, Pandas
- Frontend: Vue.js, Axios
- Outras bibliotecas: Werkzeug, UUID

## Funcionalidades principais

- Upload de arquivos CSV e Excel pelo usuário
- Processamento e filtragem dos dados enviados
- Geração dinâmica de arquivo Excel preenchido
- Download do arquivo processado via frontend

## Como usar

### Backend

1. Defina a pasta de upload configurando a variável `UPLOAD_FOLDER` no Flask.
2. Inicie o servidor Flask:

```bash
export FLASK_APP=main.py
flask run

### Frontend

- Configure a URL do backend no código Vue.js (no Axios)
- Instale as dependências e rode o front

```bash
npm install
npm run dev

- acesse a aplicação no navegador para fazer o upload dos arquivos .CSV e .xlsx
