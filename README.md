# API de Controle de Investimentos

## Descrição do Projeto

Este projeto é uma API RESTful desenvolvida como o MVP (Minimum Viable Product) para a disciplina de Desenvolvimento Full Stack Básico da Pós-Graduação em Engenharia de Software da PUC-Rio. O objetivo da API é fornecer um serviço de back-end para gerenciar uma carteira de investimentos, permitindo o registo, visualização e remoção de ativos e suas categorias.

---

## Tecnologias Utilizadas

* **Linguagem:** Python 3.12
* **Framework:** Flask
* **Banco de Dados:** SQLAlchemy com SQLite
* **Validação de Dados:** Pydantic
* **Documentação da API:** Flask-OpenAPI3 (Swagger UI)
* **Segurança:** Flask-CORS

---

## Como Executar o Projeto

Siga os passos abaixo para executar a API localmente.

### Pré-requisitos

* Python 3.12 ou superior instalado.
* Git instalado.

### Passos para Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/LayonFornaciari/mvp-invest-api.git](https://github.com/LayonFornaciari/mvp-invest-api.git)
    ```

2.  **Navegue até a pasta do projeto:**
    ```bash
    cd mvp-invest-api
    ```

3.  **Crie e ative um ambiente virtual:**
    ```bash
    # Criar o ambiente
    python -m venv .venv

    # Ativar no Windows
    .\.venv\Scripts\activate
    ```

4.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Execute a API:**
    ```bash
    flask run
    ```

A API estará a correr em `http://127.0.0.1:5000/`.