import click
from rich import print
from getpass import getpass
from core.auth import (
    register_user, login_user, logout_user, current_user,
    add_favorite, list_favorites, remove_favorite,
)
from core.validators import validate_email

@click.group(help="Autenticação e preferências do usuário.")
def auth():
    pass

@auth.command("register")
@click.option("--email", prompt=True, help="Seu e-mail (será seu login).")
@click.option("--cpf", prompt=False, help="Opcional: CPF (apenas números).")
def register(email: str, cpf: str | None):
    password = getpass("Senha (min 6 caracteres): ")
    try:
        uid = register_user(email=email.strip(), password=password, cpf=cpf)
        print(f"[green]Cadastro ok![/green] Usuário logado (id={uid}).")
    except Exception as e:
        raise click.ClickException(str(e))

@auth.command("login")
@click.option("--email", prompt=True)
def login(email: str):
    if not validate_email(email):
        raise click.ClickException("E-mail inválido.")
    password = getpass("Senha: ")
    try:
        uid = login_user(email=email.strip(), password=password)
        print(f"[green]Login ok![/green] (id={uid})")
    except Exception as e:
        raise click.ClickException(str(e))

@auth.command("logout")
def logout():
    logout_user()
    print("[yellow]Sessão finalizada.[/yellow]")

@auth.command("whoami")
def whoami():
    me = current_user()
    if not me:
        print("[red]Ninguém logado.[/red]")
    else:
        print(f"[cyan]Usuário atual:[/cyan] {me['email']} (id={me['user_id']})")

@auth.command("fav-add")
@click.option("--serie", required=True, type=click.Choice(["f1"], case_sensitive=False))
@click.option("--item-id", required=True, help="Identificador (ex: 2025-round-1)")
@click.option("--meta", required=False, help="JSON opcional com detalhes")
def fav_add(serie: str, item_id: str, meta: str | None):
    import json
    meta_dict = {}
    if meta:
        try:
            meta_dict = json.loads(meta)
        except Exception:
            raise click.ClickException("Meta deve ser um JSON válido.")
    try:
        fid = add_favorite(serie.lower(), item_id, meta=meta_dict)
        print(f"[green]Favorito salvo![/green] id={fid}")
    except Exception as e:
        raise click.ClickException(str(e))

@auth.command("fav-list")
@click.option("--serie", required=False)
def fav_list(serie: str | None):
    try:
        rows = list_favorites(serie.lower() if serie else None)
        if not rows:
            print("[yellow]Sem favoritos.[/yellow]")
            return
        for r in rows:
            print(f"{r['id']:>3} | {r['serie']} | {r['item_id']} | {r['meta']} | {r['created_at']}")
    except Exception as e:
        raise click.ClickException(str(e))

@auth.command("fav-del")
@click.option("--id", "fav_id", required=True, type=int)
def fav_del(fav_id: int):
    try:
        remove_favorite(fav_id)
        print("[green]Favorito removido.[/green]")
    except Exception as e:
        raise click.ClickException(str(e))

if __name__ == "__main__":
    auth()
