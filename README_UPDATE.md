# Pacote de Atualização — Login Opcional + Favoritos + Postgres-ready

Este pacote deixa seu projeto pronto para:
- **Registro/Login opcional** (usuário entra só se quiser)
- **Salvar informações** por usuário (favoritos)
- **Banco de dados configurável por .env** (SQLite por padrão; Postgres quando quiser)
- **CLI com `--save`** para guardar favoritos automaticamente

## 1) Instale as dependências (na sua venv)
```bash
pip install -r requirements-additions.txt
# ou:
pip install "psycopg[binary]==3.2.1" "SQLAlchemy==2.0.35" "passlib==1.7.4"
```

## 2) Copie os arquivos para o seu projeto (preservando pastas)
- `core/validators.py`
- `core/auth.py`
- `core/history.py`   (usa DATABASE_URL do .env; substitui o seu se preferir)
- `cli/auth_cli.py`
- `cli/motors_cli2.py`
- `requirements-additions.txt` (apenas referência)
- `.env.example` (faça uma cópia como `.env`)

> **Não apague sua CLI atual**. A nova `motors_cli2.py` é complementar e oferece `--save`.

## 3) Configure o `.env`
### Começar rápido (SQLite local)
```
DATABASE_URL=sqlite:///./data.db
SESSION_FILE=.session.json
LOG_LEVEL=INFO
```

### Quando for conectar ao **Postgres** (pgAdmin)
```
DATABASE_URL=postgresql+psycopg://usuario:senha@localhost:5432/seu_banco
SESSION_FILE=.session.json
LOG_LEVEL=INFO
```
Criação rápida via psql:
```sql
CREATE DATABASE chatbot_trab;
CREATE USER app_user WITH PASSWORD 'senha_forte';
GRANT ALL PRIVILEGES ON DATABASE chatbot_trab TO app_user;
-- (opcional) schema dedicado:
-- \c chatbot_trab
-- CREATE SCHEMA app AUTHORIZATION app_user;
-- ALTER ROLE app_user IN DATABASE chatbot_trab SET search_path TO app, public;
```

## 4) Teste do banco
```bash
# qualquer comando que importe auth/history já cria tabelas
python -m cli.auth_cli whoami
```

## 5) Como usar (login **opcional**)
### Autenticação
```bash
python -m cli.auth_cli register --email aluno@exemplo.com --cpf 52998224725
python -m cli.auth_cli login --email aluno@exemplo.com
python -m cli.auth_cli whoami
python -m cli.auth_cli logout
```

### Favoritos por usuário
```bash
python -m cli.auth_cli fav-add --serie f1 --item-id 2025-round-1 --meta "{"race":"GP Austrália"}"
python -m cli.auth_cli fav-list
python -m cli.auth_cli fav-del --id 1
```

### CLI com `--save` (salva favorito se houver login)
```bash
python -m cli.motors_cli2 calendario --serie f1 --ano 2025 --save
python -m cli.motors_cli2 resultado --serie f1 --round 1 --ano 2025 --save
python -m cli.motors_cli2 classificacao --serie f1 --tipo pilotos --ano 2025 --save
```

## 6) Commits sugeridos
```bash
git add core/validators.py core/auth.py core/history.py cli/auth_cli.py cli/motors_cli2.py .env.example requirements-additions.txt
git commit -m "feat: auth opcional + favoritos; DB via .env (SQLite/Postgres); CLI com --save"
```

## 7) Notas
- **Senha** com PBKDF2 via `passlib`.
- `DATABASE_URL` aceita tanto SQLite quanto Postgres sem mudar o código.
- `pool_pre_ping=True` evita erros de conexão após inatividade.
