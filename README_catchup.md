# Catch-up Pack (02/10 e 04/10)
Passos rápidos:
1) Crie um venv e instale `requirements.txt`
2) Copie `.env.example` para `.env` e ajuste chaves
3) Rode `python app.py` (demo) e a CLI:
   - `python -m cli.motors_cli calendario --serie f1 --ano 2025`
   - `python -m cli.motors_cli resultado --serie f1 --round 1 --ano 2025`
   - `python -m cli.motors_cli classificacao --serie f1 --tipo pilotos --ano 2025`
4) Verifique `data.db` criado e registros em `core/history`.
5) Commits: `feat(cli): comandos base` / `feat(core): history sqlite` / `chore: .env.example and reqs`.
