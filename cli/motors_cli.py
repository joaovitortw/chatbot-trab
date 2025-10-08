import click
from dotenv import load_dotenv
from rich import print
from services.backend import (
    get_calendar,
    get_result_by_round,
    get_standings
)
from core.history import History

@click.group()
def motors():
    """CLI de Automobilismo: calendários, resultados e classificações."""
    load_dotenv()

@motors.command()
@click.option("--serie", type=click.Choice(["f1"], case_sensitive=False), required=True, help="Série esportiva (ex.: f1).")
@click.option("--ano", type=int, required=False, help="Ano do calendário (ex.: 2025).")
def calendario(serie, ano):
    """Exibe o calendário da série e salva a consulta no histórico."""
    data = get_calendar(serie=serie.lower(), year=ano)
    for r in data:
        print(f"{r['round']:>2} | {r['raceName']} | {r['date']} {r.get('time','')} | {r['Circuit']['circuitName']}")
    History().save(event="calendario", serie=serie, payload={"year": ano})

@motors.command()
@click.option("--serie", type=click.Choice(["f1"], case_sensitive=False), required=True)
@click.option("--round", "rnd", type=int, required=True, help="Número da etapa (round).")
@click.option("--ano", type=int, required=False, help="Ano, se quiser fixar.")
def resultado(serie, rnd, ano):
    """Mostra o resultado de uma etapa (round)."""
    res = get_result_by_round(serie=serie.lower(), rnd=rnd, year=ano)
    if not res:
        print("[yellow]Sem resultados encontrados.[/yellow]")
        return
    print(f"[bold]Resultado Round {rnd}[/bold]")
    for pos in res[:10]:
        line = f"{pos['position']:>2} {pos['Driver']['familyName']} ({pos['Constructor']['name']}) - {pos['points']} pts"
        print(line)
    History().save(event="resultado", serie=serie, payload={"round": rnd, "year": ano})

@motors.command()
@click.option("--serie", type=click.Choice(["f1"], case_sensitive=False), required=True)
@click.option("--tipo", type=click.Choice(["pilotos","equipes"], case_sensitive=False), required=True, help="pilotos|equipes")
@click.option("--ano", type=int, required=False)
def classificacao(serie, tipo, ano):
    """Tabela de classificação (pilotos ou equipes)."""
    tbl = get_standings(serie=serie.lower(), tipo=tipo.lower(), year=ano)
    for i, row in enumerate(tbl[:10], start=1):
        if tipo.lower() == "pilotos":
            nm = f"{row['Driver']['familyName']}"
        else:
            nm = row['Constructor']['name']
        print(f"{i:>2} | {nm} | {row['points']} pts")
    History().save(event="classificacao", serie=serie, payload={"tipo": tipo, "year": ano})

if __name__ == "__main__":
    motors()
