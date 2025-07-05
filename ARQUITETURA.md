Arquitetura e Fluxo de Dados do Sistema
Este documento descreve a arquitetura interna do backend do projeto, explicando a responsabilidade de cada componente e como os dados fluem através do sistema.

Visão Geral da Arquitetura
O backend foi projetado usando uma arquitetura em camadas, uma abordagem profissional que separa as diferentes responsabilidades da aplicação. Isso torna o código mais organizado, mais fácil de manter e de testar.

A lógica flui da seguinte forma:

Requisição do Usuário ➡️ Routes (API) ➡️ Services (Lógica de Negócio) ➡️ Data Processing (Preparação) ➡️ Resposta

Pense nisso como um restaurante:

Routes (views.py): É o Garçom. Ele anota o pedido do cliente.

Services (pipeline_service.py, etc.): É a Cozinha. Onde o prato é de fato preparado.

Data Processing (processador_vendas.py): É a Área de Preparação. Onde os ingredientes são lavados e cortados antes de irem para a cozinha.

Componentes Principais do Backend
Cada pasta e arquivo tem um propósito claro:

main.py: O "Interruptor Geral". Sua única função é ligar e configurar o servidor Flask.

config.py: O "Painel de Controle". Todas as configurações que podem mudar com o tempo (nomes de colunas, listas de exclusão, etc.) vivem aqui. Se precisar ajustar uma regra, você mexe aqui, sem tocar no resto do código.

routes/views.py: A camada da API (o Garçom). Define todas as URLs (ex: /upload, /vendedores_tele). A responsabilidade deste arquivo é apenas receber o pedido e chamar o serviço correto na "cozinha". Ele não faz lógica de negócio.

services/pipeline_service.py: O "Gerente da Fábrica". Ele orquestra o fluxo de trabalho principal quando os arquivos são enviados, chamando o "Chef Preparador" e o "Detetive" na ordem correta.

data_processing/processador_vendas.py: O "Chef Preparador" (ProcessadorVendas). Sua missão é pegar os dados brutos e fazer toda a limpeza inicial: padronizar nomes de colunas, corrigir datas, remover linhas e colunas indesejadas. Ele entrega os "ingredientes" limpos para a próxima etapa.

services/conciliador.py: O "Detetive de Dados" (ConciliadorVendas). Este é o cérebro da lógica de negócio. Ele recebe os dados já limpos e faz o trabalho de cruzar informações, encontrar clientes parecidos (fuzzy matching), preencher colunas vazias e adicionar novos clientes.

services/relatorio_service.py: O "Assistente com Memória Fotográfica" (RelatorioService). Para otimizar a performance, ele lê o arquivo de resultado final uma única vez e o guarda na memória. Todas as rotas de consulta (para os gráficos do frontend) pedem a informação para ele, que responde instantaneamente sem precisar ler o arquivo do disco toda vez.

utils/formatadores.py: A "Caixa de Ferramentas". Contém funções pequenas e especialistas, como a nossa corrigir_data_inteligentemente.

tests/: O "Controle de Qualidade". Contém testes automáticos que garantem que as partes mais críticas e complexas do sistema (como a correção de datas e a conciliação) estão funcionando como esperado.

Fluxo de Dados Detalhado
1. Processo de Upload (/upload)
Garçom (views.py): A rota /upload recebe os arquivos CSV e Excel.

Gerente (pipeline_service): O garçom chama a função executar_pipeline_completo.

Chef Preparador (ProcessadorVendas): O gerente manda o Chef limpar e preparar os dados.

Detetive (ConciliadorVendas): Com os dados limpos, o gerente manda o Detetive fazer a conciliação.

Salvamento: O gerente pega o relatório final do Detetive e o salva como resultado.xlsx.

Memorização (RelatorioService): Por fim, o gerente entrega uma cópia do relatório para o "Assistente de Pesquisa", que o memoriza para futuras consultas.

2. Processo de Consulta (/vendedores_tele)
Garçom (views.py): A rota /vendedores_tele recebe o pedido.

Assistente (RelatorioService): O garçom simplesmente pergunta ao "Assistente de Pesquisa" pelos dados.

Resposta Instantânea: O assistente consulta sua memória (o DataFrame que ele já tem) e devolve a resposta imediatamente. O garçom a entrega ao cliente.

Esta arquitetura garante um sistema organizado, eficiente e fácil de dar manutenção.