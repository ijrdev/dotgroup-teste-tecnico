# Dotgroup - Teste técnico

Repositório das questões do desafio técnico para a empresa Dotgroup. Cada questão possui sua própria implementação e documentação, mas todas utilizam o mesmo ambiente Python e o mesmo gerenciador de dependências.

## 🧰 Preparação do ambiente

### Pré-requisitos

- Python `3.14` ou superior;
- [uv](https://docs.astral.sh/uv/) instalado.

Na raiz do repositório, instale as dependências e sincronize o ambiente:

```bash
uv sync
```

**Deve-se prestar atenção para os comandos de executar as aplicações, pois podem ser realizados desde a raíz do projeto quanto isoladamente na pasta das questões.**

---

## Questão 1 - API da Biblioteca Virtual

### 🎯 Objetivo

API para cadastro e consulta de livros, com persistência em SQLite. A implementação atende aos seguintes requisitos:

- Cadastro de livros com título, autor, data de publicação e resumo;
- Consulta por título, autor ou pelos dois filtros combinados;
- Validação dos dados de entrada;
- Testes dos endpoints da API.
- Documentação da API via Swagger;

### 🛠️ Tecnologias e decisões técnicas

- **FastAPI** para construção da API e geração do contrato OpenAPI;
- **Pydantic** para validação e normalização dos dados recebidos;
- **SQLite** para armazenamento local, sem necessidade de serviço externo;
- **Uvicorn** como servidor ASGI;
- **SlowAPI** para colocar limitação de requisições nas rotas;
- **Pytest + HTTPX** para os testes unitários;
- Arquitetura de separação em camadas de apresentação, serviço, repositório e infraestrutura.

O banco SQLite que fica em `questao_1/biblioteca_livros.db` e a tabela `livros` são criados automaticamente na inicialização da aplicação.

### 📁 Estrutura principal

```text
questao_1/
├── app.py                             # Ponto de entrada e configuração da aplicação FastAPI
├── presentation/                      # Camada de apresentação da API
├── services/                          # Regras de negócio e orquestração dos casos de uso
├── infrastructure/                    # Implementações relacionadas à persistência e recursos externos
├── application/                       # Componentes compartilhados da aplicação
└── tests/                             # Testes automatizados
```

### ▶️ Executar a API

Acesse a **raíz da questao_1** e execute:

```bash
uv run app.py
```

A API ficará disponível em `http://localhost:8000`.

Documentação interativa:

- **Swagger UI**: `http://localhost:8000/documentacao`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

### 🧪 Executar os testes

Acesse a **raíz do projeto** e execute:

```bash
uv run pytest questao_1/tests -q
```

Os testes cobrem:

- Cadastro com sucesso;
- Rejeição de payload inválido;
- Consulta filtrada;
- Consulta sem filtro obrigatório.

---

## Questão 2 - Agente Técnico de Python

### 🎯 Objetivo

Agente conversacional especializado em programação Python, com interface de chat para interação e validação manual. A implementação atende aos seguintes requisitos:

- Resolução de dúvidas técnicas com exemplos de código curtos e objetivos;
- Atendimento restrito ao contexto de desenvolvimento Python;
- Consulta a fontes oficiais quando a resposta depender de versões, APIs, compatibilidade ou informações recentes;
- Indicação das fontes consultadas ao utilizar pesquisa na web;
- Interface de chat para interação com o agente;

🛠️ Tecnologias e decisões técnicas

- **LangChain + `create_agent`** para declarar modelo, ferramentas e instruções em uma única abstração. A função retorna um grafo LangGraph compilado, pronto para ser exposto pelo servidor e consumido pelo Agent Chat UI;
- **LangGraph** como runtime do agente, responsável pelo ciclo de uso de ferramentas e pela compatibilidade com o servidor de desenvolvimento e a interface de chat;
- **OpenAI** como provedor do modelo, configurado por variáveis de ambiente para não expor credenciais no código;
- **`web_search`** é a ferramenta que permite ao agente pesquisar na web quando a informação for temporal ou depender de documentação atual;
- **LangSmith** registra rastros das execuções, mensagens, chamadas de ferramenta, latência e erros, para observabilidade e depuração do agente durante o desenvolvimento.

Essa abordagem foi escolhida em vez de montar manualmente uma cadeia com **LCEL**. Embora o LCEL seja adequado para fluxos lineares, ele exigiria orquestrar separadamente prompt, modelo, parser e chamadas de ferramenta. O `create_agent` mantém a implementação enxuta, já utiliza o runtime moderno do LangGraph e permite evoluir o grafo para múltiplos nós, aprovações humanas, persistência ou ramificações sem trocar sua base.

### ⚙️ Configurar as variáveis de ambiente

Crie `questao_2/.env` a partir de `questao_2/.env.example` e preencha:

```env
OPENAI_API_KEY=chave_da_openai
OPENAI_MODEL=nome_do_modelo

LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=chave_do_langsmith
LANGSMITH_PROJECT=nome_do_projeto
```

Para uso do LangSmith, deve-se ter uma conta para criar um projeto e gerar uma api key.

### ▶️ Executar e acessar pelo Agent Chat UI

Na raiz da `questao_2`, inicie o servidor:

```bash
uv run langgraph dev --tunnel
```

O `--tunnel` expõe o servidor local por uma URL HTTPS temporária. Isso permite que uma interface hospedada externamente acesse o grafo local com segurança e evita bloqueios do navegador em conexões entre HTTPS e `localhost`.

Com o servidor em execução:

1. Copie a URL HTTPS do túnel exibida no terminal (fica em API));
2. Abra o [Agent Chat UI](https://agentchat.vercel.app/);
3. Preencha os campos iniciais:
   - **Deployment URL**: cole a URL HTTPS do túnel que foi previamente copiada;
   - **Assistant/Graph ID**: informe `agent`, que é a chave registrada em `questao_2/langgraph.json`;
   - **LangSmith API Key**: preencha com a API KEY criada do Lang Smith;
4. Clique em **Continue** para abrir o chat e iniciar a interação com o agente.

---

## Questão 3 - Busca Semântica com FAISS

### 🎯 Objetivo

Aplicação de linha de comando para recuperar documentos pelo significado da consulta, e não apenas pela correspondência literal de palavras. Ela gera embeddings para os conteúdos, armazena os vetores em um índice FAISS e retorna os documentos semanticamente mais próximos.

A implementação atende aos seguintes requisitos:

- Leitura de um conjunto local de documentos de texto em JSON;
- Geração de embeddings por um modelo baseado em Transformers;
- Armazenamento dos vetores em uma vector store FAISS;
- Busca semântica por consulta textual, ordenada por similaridade;
- Demonstração no terminal dos documentos mais relevantes;
- Persistência local do índice para reutilização entre execuções.

### 🛠️ Tecnologias e decisões técnicas

- **Sentence Transformers** para carregar o modelo `sentence-transformers/all-MiniLM-L6-v2` e gerar os embeddings. A biblioteca utiliza Transformers internamente;
- **FAISS CPU** para criar e consultar o índice vetorial;
- **NumPy**, utilizado pelos embeddings retornados pelo modelo e pelo FAISS;
- **JSON** para manter o conjunto de textos-fonte em `questao_3/contents.json`;

Os embeddings são normalizados antes de serem inseridos no índice. Por isso, o produto interno usado pelo `IndexFlatIP` representa a similaridade de cosseno entre consulta e documentos.

Na primeira execução, os embeddings de todos os conteúdos são gerados e o índice é persistido em `questao_3/documents.faiss`. Nas execuções seguintes, o índice existente é carregado diretamente, sem gerar novamente os embeddings dos documentos.

### ▶️ Executar a aplicação

Acesse a **raíz da questao_3** e execute:

```bash
uv run questao_3/app.py
```

A aplicação executa a consulta definida no arquivo e exibe no terminal os documentos mais relevantes, com o score de similaridade e o texto correspondente.

### ✏️ Alterar a consulta e a quantidade de resultados

Em `questao_3/app.py`, ajuste as variáveis dentro do bloco `if __name__ == "__main__"`:

```python
query: str = "Quais ferramentas podem ser usadas para busca vetorial?"
top_k: int = 3
```

- `query`: texto que será pesquisado semanticamente;
- `top_k`: número máximo de documentos relevantes retornados.

### 📚 Alterar os conteúdos pesquisáveis

Os textos estão em `questao_3/contents.json`, em uma lista JSON de strings. Inclua, edite ou remova textos nesse arquivo para mudar a base de busca.

Após qualquer alteração em `contents.json`, exclua `questao_3/documents.faiss` e execute a aplicação novamente. Isso força a geração de embeddings para a nova coleção; caso contrário, a aplicação reutilizará o índice anterior. Esse arquivo é ignorado pelo Git por ser um artefato local gerado automaticamente.

### 🧩 Por que não foi utilizado chunking ou documentos complexos?

O conjunto desta demonstração é formado por textos curtos e autocontidos, nos quais cada item de `contents.json` já representa uma unidade semântica completa. Dividi-los em chunks adicionaria complexidade sem melhorar a recuperação e poderia separar contexto importante do mesmo assunto.

Chunking passa a ser necessário para fontes extensas ou estruturadas, como PDFs, páginas HTML longas, contratos e documentos com múltiplas seções, porque esses conteúdos podem ultrapassar o limite útil do modelo de embeddings e abordar vários temas no mesmo arquivo. Nesse cenário, seria necessário definir tamanho e sobreposição dos trechos, preservar metadados de origem e retornar o trecho relevante junto da referência ao documento original. Para o escopo atual, uma lista simples de textos torna o fluxo de geração, persistência e busca vetorial mais direto de demonstrar.
