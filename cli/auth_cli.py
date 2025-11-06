
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
        
        if not validate_email(email):
            raise click.ClickException("E-mail inválido. Verifique o formato.")
        if cpf and not is_valid_cpf(cpf):
            raise click.ClickException("CPF inválido. Por favor, insira o CPF corretamente.")
        
        uid = register_user(email=email.strip(), password=password, cpf=cpf)
        print(f"[green]Cadastro realizado com sucesso![/green] Usuário logado (id={uid}).")
    except Exception as e:
        raise click.ClickException(f"[red]Erro ao registrar usuário:[/red] {str(e)}")

@auth.command("login")
@click.option("--email", prompt=True)
def login(email: str):
    if not validate_email(email):
        raise click.ClickException("E-mail inválido. Por favor, verifique o formato.")
    password = getpass("Senha: ")
    try:
        uid = login_user(email=email.strip(), password=password)
        print(f"[green]Login realizado com sucesso![/green] (id={uid})")
    except Exception as e:
        raise click.ClickException(f"[red]Erro ao fazer login:[/red] {str(e)}")
