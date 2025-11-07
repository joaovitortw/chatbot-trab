# services/hyprace_client.py

import os
import requests
from datetime import datetime, timezone

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "d4972bd191msh23ae861b3f27a66p12270ajsnbb12b59402af")
headers = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": "hyprace-api.p.rapidapi.com"
}

def get_next_race():
    try:
        url = "https://hyprace-api.p.rapidapi.com/v2/grands-prix"
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        gps = response.json()

        now = datetime.now(timezone.utc)
        future_races = []

        for gp in gps:
            start_str = gp.get("start_date")
            if not start_str:
                continue

            start_dt = datetime.fromisoformat(start_str.replace("Z", "+00:00"))
            if start_dt > now:
                future_races.append((start_dt, gp))

        future_races.sort(key=lambda x: x[0])

        if future_races:
            race = future_races[0][1]
            name = race.get("name", "Nome desconhecido")
            country = race.get("location", {}).get("country", "País desconhecido")
            circuit = race.get("location", {}).get("circuit", {}).get("name", "Circuito desconhecido")
            start_dt = future_races[0][0]
            dias = (start_dt - now).days

            return {
                "name": name,
                "circuit": circuit,
                "country": country,
                "start": start_dt.strftime("%d/%m/%Y"),
                "countdown": dias
            }

    except Exception as e:
        print(f"Erro ao buscar próxima corrida: {e}")
        return None
