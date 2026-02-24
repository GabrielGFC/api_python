# API de Usuários com Perfil (FastAPI + SQLAlchemy + MySQL)

API REST para gerenciamento de **Usuários** e seus **Perfis** com relacionamento 1:1, utilizando **FastAPI**, **SQLAlchemy (ORM)**, **MySQL** e **Alembic** para migrations.

## Tecnologias

- Python
- FastAPI
- SQLAlchemy (ORM)
- MySQL (padrão) / SQLite (opcional para dev)
- Alembic (migrations)
- Passlib (hash de senha com bcrypt)
- Pydantic v2

## Estrutura de Pastas

```bash
app/
├── database.py          # conexão e sessão do banco
├── models.py            # models SQLAlchemy (User e Profile)
├── schemas.py           # schemas Pydantic
├── crud.py              # funções de acesso ao banco
├── routers/
│   └── usuarios.py      # rotas do CRUD de usuários
└── main.py              # instância do FastAPI e registro das rotas
.env
.env.example
requirements.txt
README.md
postman_collection.json
```

## Entidades

- **User**
  - `id`
  - `nome`
  - `email` (único)
  - `senha` (armazenada hasheada com bcrypt)
  - `profile_id`
  - `created_at`
- **Profile**
  - `id`
  - `perfil_nome`

Relacionamento **1:1** entre `User` e `Profile`:

- `User.profile` ↔ `Profile.user` via `relationship` com `back_populates` e `uselist=False`.

## Requisitos

- Python instalado (3.10+ recomendado).
- Servidor MySQL acessível.

## Instalação

Dentro da pasta do projeto (`api_python`):

```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows PowerShell
# ou
source .venv/bin/activate      # Linux/Mac

pip install -r requirements.txt
```

## Configuração de Ambiente

1. Copie o arquivo de exemplo:

```bash
cp .env.example .env
```

2. Edite o arquivo `.env` com suas credenciais:

```env
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/nome_do_banco
CORS_ORIGINS=*
```

Alternativa para desenvolvimento com SQLite (opcional):

```env
DATABASE_URL=sqlite:///./dev.db
```

> Lembre de manter o `.env` fora do controle de versão.

## Migrations com Alembic

### 1. Inicializar Alembic

No diretório raiz do projeto:

```bash
alembic init migrations
```

### 2. Configurar `alembic.ini`

No arquivo `alembic.ini`, ajuste a URL do banco (ou deixe vazia e use o `.env` no `env.py`):

```ini
sqlalchemy.url = mysql+pymysql://user:password@localhost:3306/nome_do_banco
```

### 3. Configurar `migrations/env.py`

Garanta que o Alembic use os models da aplicação:

```python
from app.database import Base

target_metadata = Base.metadata
```

### 4. Gerar migration inicial

```bash
alembic revision -m "create users and profiles tables" --autogenerate
```

### 5. Aplicar migrations

```bash
alembic upgrade head
```

## Executando a API

Após instalar as dependências, configurar o `.env` e aplicar as migrations:

```bash
uvicorn app.main:app --reload
```

API disponível por padrão em:

```bash
http://localhost:8000
```

Documentação automática:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints Principais

### Health check

- **GET** `/health`  
  Verifica se a API está respondendo.

### Usuários

- **POST** `/usuarios/`  
  Cria um novo usuário com perfil associado.  
  Corpo (JSON):

```json
{
  "nome": "João da Silva",
  "email": "joao@example.com",
  "senha": "SenhaSegura123",
  "profile": {
    "perfil_nome": "ADMIN"
  }
}
```

- **GET** `/usuarios/`  
  Lista usuários com seus perfis.

- **GET** `/usuarios/{id}`  
  Obtém um usuário específico pelo `id`.

- **PUT** `/usuarios/{id}`  
  Atualiza dados de um usuário (somente `nome` e `email`):

```json
{
  "nome": "João Atualizado",
  "email": "joao.novo@example.com"
}
```

- **DELETE** `/usuarios/{id}`  
  Remove um usuário e o perfil associado.

## Regras de Negócio Implementadas

- Relacionamento **1:1** entre Usuário e Perfil.
- Criação de usuário permite criar o perfil junto.
- Validação de e-mail único com tratamento de erro adequado.
- CRUD completo de Usuário.
- Listagem de usuários retornando dados do perfil via relacionamento.
- Senha armazenada **sempre hasheada** com `passlib[bcrypt]`.
- Campo `senha` **nunca é retornado** nas respostas.

## Coleção do Postman

O arquivo `postman_collection.json` na raiz do projeto contém uma coleção pronta para importação no Postman, com:

- Health check
- Criar usuário
- Listar usuários
- Detalhar usuário
- Atualizar usuário
- Remover usuário

Use a variável `{{base_url}}` definida na própria coleção (por padrão `http://localhost:8000`).

