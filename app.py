import os
from dotenv import load_dotenv
from services.backend import get_next_event_f1
from rich import print

def main():
    load_dotenv()
    print("[bold cyan]Demo:[/bold cyan] Próxima corrida da F1")
    try:
        nxt = get_next_event_f1()
        if nxt:
            print(f"[green]Próxima:[/green] {nxt['raceName']} - {nxt['date']} {nxt.get('time','')} ({nxt['Circuit']['circuitName']})")
        else:
            print("[yellow]Não foi possível obter a próxima corrida.[/yellow]")
    except Exception as e:
        print(f"[red]Erro:[/red] {e}")

if __name__ == "__main__":
    main()
