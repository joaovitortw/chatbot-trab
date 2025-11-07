# services/f1_api_client.py

import requests
from datetime import datetime

BASE_URL = "https://api.openf1.org/v1"

def get_f1_calendar(year: int = None) -> list:
    """Retorna a lista de corridas de um determinado ano."""
    try:
        year = year or datetime.utcnow().year
        url = f"{BASE_URL}/sessions?year={year}"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        # Remove sessões duplicadas (FP1, FP2, etc), mantendo apenas Race
        races = [d for d in data if d.get("session_name") == "Race"]
        return sorted(races, key=lambda x: x.get("date_utc"))
    except Exception as e:
        print(f"Erro ao buscar calendário da F1: {e}")
        return []

def get_next_event_f1() -> dict:
    """Retorna a próxima corrida futura baseada na data atual."""
    try:
        calendar = get_f1_calendar()
        now = datetime.utcnow().isoformat()
        for race in calendar:
            if race.get("date_utc") and race["date_utc"] > now:
                return race
        return {}
    except Exception as e:
        print(f"Erro ao buscar próxima corrida: {e}")
        return {}

def get_f1_results_by_round(round_num: int, year: int = None) -> dict:
    """Busca resultados da corrida por número da rodada."""
    try:
        races = get_f1_calendar(year)
        if round_num - 1 < len(races):
            return races[round_num - 1]
        else:
            print("Rodada não encontrada.")
            return {}
    except Exception as e:
        print(f"Erro ao buscar resultados: {e}")
        return {}

def get_f1_standings(drivers: bool = True, year: int = None) -> list:
    """OpenF1 não fornece standings diretamente. Retorna corridas como fallback."""
    print("OpenF1 ainda não fornece classificação diretamente.")
    return get_f1_calendar(year)
