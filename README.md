# Projeto de E-commerce da Amazon - Banco de Dados

Este projeto foi desenvolvido para a **Fase 4 (AV2)** da disciplina de **Banco de Dados**.

###  Integrantes
* Raphaella Roma
* Beatriz Marques
* Gabrielle Mascarelo

---

##  Sobre o Projeto

O objetivo foi criar a estrutura de um sistema de e-commerce, implementando as funcionalidades de CRUD (Criar, Ler, Atualizar, Deletar) para gerenciar as principais entidades do negócio, como clientes, produtos e pedidos.

Para o back-end, escolhemos utilizar um banco de dados **PostgreSQL hospedado na Amazon RDS**. A escolha se deu pela alta escalabilidade, confiabilidade e facilidade de gerenciamento que os serviços da AWS oferecem, características essenciais para uma aplicação de e-commerce robusta.

---

## Como Executar

1.  **Configure o Banco de Dados:**
    * Certifique-se de que as credenciais de acesso ao banco de dados estão corretamente configuradas no arquivo `db_config.py`.

2.  **Instale as Dependências:**
    * É recomendado ter as bibliotecas Python necessárias. A principal é a `psycopg2-binary` para a conexão com o PostgreSQL.
    ```bash
    pip install psycopg2-binary
    ```

3.  **Rode a Aplicação:**
    * Execute o arquivo principal para iniciar o programa.
    ```bash
    python main.py
    ```
