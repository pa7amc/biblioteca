# Projeto de gestão de biblioteca

## Ideia do nome da biblioteca
**"AlphaBeta"** devido a ser uma biblioteca temática especialmente dedicada a livros científicos e tecnológicos. 
O nome tem, pelo menos, duplo sentido: uma mistura da palavra alfabética + o algoritmo Alpha-beta, muito utilizado em contexto de jogos (de 2 jogadores).
    
## Funcionalidades
- **Livros:** Registar, Ver e Remover
- **Sócios:** Registar, Ver e Remover
- **Requisitos de livros:** Registar, Ver e Completar
- **Campanhas:** Registar, Ver e Remover
- **Adesões:** Registar, Ver e Remover

## Correr com docker
`make docker`

Este comando vai fazer launch da aplicação já com alguns dados previamente inseridos. A aplicação estará disponível em http://127.0.0.1:5000.

**Resolução de evental erro 'Warning: The lock file is not up to date with the latest changes in pyproject.toml'**

https://stackoverflow.com/questions/62040724/warning-the-lock-file-is-not-up-to-date-with-the-latest-changes-in-pyproject-to

## Correr localmente

Instalar **poetry**: https://python-poetry.org/docs/#installation

Instalar **dependências** do projeto: `poetry install`

Entrar no ambiente virtual: `poetry shell`

Executar a aplicação: `make run`

Este comando vai fazer launch da aplicação já com alguns dados previamente inseridos. A aplicação estará disponível em http://127.0.0.1:5000.

## Gerar uma nova BD (com valores previamente inseridos)
` make init ` 

## Gerar uma BD vazia
` make empty ` 
