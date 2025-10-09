PASSO A PASSO PARA INTEGRAR LOGIN OPCIONAL + FAVORITOS

1) Dependências (na venv):
   pip install passlib SQLAlchemy

2) Copie estes arquivos para o projeto:
   - core/validators.py
   - core/auth.py
   - cli/auth_cli.py
   - cli/motors_cli2.py   (CLI com --save)

3) Uso da nova CLI (além da sua atual):
   python -m cli.motors_cli2 calendario --serie f1 --ano 2025 --save
   python -m cli.motors_cli2 resultado --serie f1 --round 1 --ano 2025 --save
   python -m cli.motors_cli2 classificacao --serie f1 --tipo pilotos --ano 2025 --save

   *Se estiver logado, salva um favorito correspondente ao comando executado.

4) Autenticação (opcional; só se quiser salvar informações por usuário):
   python -m cli.auth_cli register --email aluno@exemplo.com --cpf 52998224725
   python -m cli.auth_cli login --email aluno@exemplo.com
   python -m cli.auth_cli whoami
   python -m cli.auth_cli logout

   Favoritos:
   python -m cli.auth_cli fav-add --serie f1 --item-id 2025-round-1 --meta "{\"race\": \"GP Austrália\"}"
   python -m cli.auth_cli fav-list
   python -m cli.auth_cli fav-del --id 1

5) Configuração opcional no .env:
   DATABASE_URL=sqlite:///./data.db
   SESSION_FILE=.session.json

6) Commits sugeridos:
   chore(auth): add validators, user model and session file
   feat(cli): new motors_cli2 with --save and favorites integration
   feat(cli): auth_cli register/login/whoami/logout and favorites commands
