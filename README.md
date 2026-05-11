# Order Management System API

Uma API robusta e escalável para gerenciamento de pedidos e autenticação, desenvolvida com **FastAPI** e **SQLAlchemy**. O projeto demonstra competências avançadas em desenvolvimento backend, incluindo segurança com JWT, modelagem relacional de dados e versionamento de banco de dados com Alembic.

##  Tecnologias Utilizadas

*   **Framework:** [FastAPI](https://fastapi.tiangolo.com/) - Alta performance e documentação automática.
*   **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/) - Mapeamento objeto-relacional para manipulação de dados.
*   **Banco de Dados:** SQLite (pode ser facilmente migrado para PostgreSQL/MySQL).
*   **Migrações:** [Alembic](https://alembic.sqlalchemy.org/) - Controle de versão e evolução do esquema do banco.
*   **Segurança:** 
    *   **JWT (JSON Web Tokens):** Para autenticação assíncrona e segura.
    *   **Bcrypt:** Criptografia de senhas (hashing).
*   **Validação:** Pydantic Schemas para tipagem e validação de entrada/saída.

## Diferenciais Técnicos

Este projeto foi construído seguindo boas práticas de arquitetura de software:

-   **Injeção de Dependências:** Sistema de sessões de banco de dados (`get_db`) e verificação de tokens implementados como dependências nativas do FastAPI.
-   **Segurança com Refresh Tokens:** Implementação de lógica para renovação de acesso, garantindo melhor experiência de usuário e segurança.
-   **Lógica no Modelo (Domain Logic):** O modelo `Pedido` possui métodos internos (como `calcular_preco`) para garantir que as regras de negócio sejam consistentes na persistência.
-   **Controle de Acesso (RBAC):** Diferenciação entre usuários comuns e administradores para ações críticas como listar todos os pedidos ou cancelar registros.
-   **Clean Code:** Separação clara entre rotas, modelos, dependências e esquemas.

## Principais Funcionalidades

### Autenticação
- Cadastro de usuários com senhas protegidas por hash.
- Login via JSON ou formulário padrão OAuth2.
- Proteção de rotas através de verificação de expiração e assinatura do token.

### Gestão de Pedidos
- Fluxo completo de pedidos: criar, adicionar itens, remover itens, finalizar e cancelar.
- Cálculo automático do valor total do pedido baseado no preço unitário e quantidade dos itens.
- Consulta de histórico de pedidos vinculada ao perfil do usuário autenticado.

## Como Executar o Projeto

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/miguelnsimoes/FastAPI-pizzaria.git
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    # No Windows:
    venv\Scripts\activate
    # No Linux/Mac:
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as variáveis de ambiente (.env):**
    Crie um arquivo `.env` na raiz do projeto:
    ```env
    SECRET_KEY="sua_chave_secreta_aqui"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

5.  **Rode as migrações do banco de dados:**
    ```bash
    alembic upgrade head
    ```

6.  **Inicie a aplicação:**
    ```bash
    uvicorn main:app --reload
    ```

7.  **Acesse a documentação:**
    Explore e teste os endpoints em `http://127.0.0.1:8000/docs`.

---
Desenvolvido por [Miguel] - [www.linkedin.com/in/miguel-nazario-simoes]
