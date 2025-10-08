from services.ergast_client import (
    get_f1_calendar,
    get_f1_results_by_round,
    get_f1_standings
)

def get_calendar(serie: str, year: int | None = None):
    if serie != "f1":
        raise ValueError("Série não suportada ainda. Use 'f1'.")
    return get_f1_calendar(year=year)

def get_result_by_round(serie: str, rnd: int, year: int | None = None):
    if serie != "f1":
        raise ValueError("Série não suportada ainda. Use 'f1'.")
    return get_f1_results_by_round(round_num=rnd, year=year)

def get_standings(serie: str, tipo: str, year: int | None = None):
    if serie != "f1":
        raise ValueError("Série não suportada ainda. Use 'f1'.")
    drivers = True if tipo == "pilotos" else False
    return get_f1_standings(drivers=drivers, year=year)

def get_next_event_f1():
    races = get_f1_calendar(year=None)
    # pega a próxima por data (simples; confia no endpoint 'current')
    return races[-1] if races else None
