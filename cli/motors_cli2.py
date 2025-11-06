import click
from dotenv import load_dotenv
from rich import print
from services.backend import get_calendar, get_result_by_round, get_standings
from core.history import History

def try_save_fav(enabled: bool, serie: str, item_id: str, meta: dict):
    if not enabled:
        return
    try:
        from core.auth import current_user, add_favorite
        if current_user():
            add_favorite(serie, item_id, meta=meta)
            print("[green]✓ salvo nos favoritos[/green]")
        else:
            print("[yellow]Dica:[/yellow] faça login para salvar nos favoritos.")
    except Exception as e:
        print(f"[yellow]Não foi possível salvar favorito:[/yellow] {e}")

@click.group(context_settings=dict(help_option_names=["-h", "--help"])) 
@click.option("--debug", is_flag=True, help="Mostra trace completo de erros.")
@click.pass_context
def motors2(ctx, debug):
    """CLI de Automobilismo (com --save opcional)."""
    load_dotenv()
    ctx.ensure_object(dict)
    ctx.obj["DEBUG"] = bool(debug)

def handle_errors(f):
    import functools, click as _click, traceback
    @functools.wraps(f)
    @click.pass_context
    def wrapper(ctx, *args, **kwargs):
        try:
            return f(*args, **kwargs)
        except _click.ClickException:
            raise
        except Exception as e:
            if ctx.obj.get("DEBUG"):
                traceback.print_exc()
                raise
            print(f"[red]Erro:[/red] {e}")
            print("[yellow]Use --debug para detalhes.[/yellow]")
            raise _click.ClickException("Falha ao executar o comando.")
    return wrapper

@motors2.command()
@click.option("--serie", type=click.Choice(["f1"], case_sensitive=False), required=True, help="Série esportiva (ex.: f1)." )
@click.option("--ano", type=int, required=False, help="Ano do calendário (ex.: 2025)." )
@click.option("--save", is_flag=True, help="Tenta salvar como favorito (se logado)." )
@handle_errors
def calendario(serie, ano, save):
    data = get_calendar(serie=serie.lower(), year=ano)
    for r in data:
        print(f"{r['round']:>2} | {r['raceName']} | {r['date']} {r.get('time','')} | {r['Circuit']['circuitName']}")
    History().save(event="calendario", serie=serie, payload={"year": ano})
    try_save_fav(save, serie.lower(), f"{ano or 'current'}-calendar", {"count": len(data)} )

@motors2.command()
@click.option("--serie", type=click.Choice(["f1"], case_sensitive=False), required=True)
@click.option("--round", "rnd", type=int, required=True, help="Número da etapa (round)." )
@click.option("--ano", type=int, required=False, help="Ano, se quiser fixar." )
@click.option("--save", is_flag=True, help="Tenta salvar como favorito (se logado)." )
@handle_errors
def resultado(serie, rnd, ano, save):
    res = get_result_by_round(serie=serie.lower(), rnd=rnd, year=ano)
    if not res:
        print("[yellow]Sem resultados encontrados.[/yellow]")
        return
    print(f"[bold]Resultado Round {rnd}[/bold]")
    for pos in res[:10]:
        line = f"{pos['position']:>2} {pos['Driver']['familyName']} ({pos['Constructor']['name']}) - {pos['points']} pts"
        print(line)
    History().save(event="resultado", serie=serie, payload={"round": rnd, "year": ano})
    try_save_fav(save, serie.lower(), f"{ano or 'current'}-round-{rnd}", {"top": 10})

@motors2.command()
@click.option("--serie", type=click.Choice(["f1"], case_sensitive=False), required=True)
@click.option("--tipo", type=click.Choice(["pilotos","equipes"], case_sensitive=False), required=True, help="pilotos|equipes" )
@click.option("--ano", type=int, required=False)
@click.option("--save", is_flag=True, help="Tenta salvar como favorito (se logado)." )
@handle_errors
def classificacao(serie, tipo, ano, save):
    tbl = get_standings(serie=serie.lower(), tipo=tipo.lower(), year=ano)
    for i, row in enumerate(tbl[:10], start=1):
        if tipo.lower() == "pilotos":
            nm = f"{row['Driver']['familyName']}"
        else:
            nm = row['Constructor']['name']
        print(f"{i:>2} | {nm} | {row['points']} pts")
    History().save(event="classificacao", serie=serie, payload={"tipo": tipo, "year": ano})
    try_save_fav(save, serie.lower(), f"{ano or 'current'}-standings-{tipo.lower()}", {"top": 10})

if __name__ == "__main__":
    motors2()
