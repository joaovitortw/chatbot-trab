import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

URL = "https://www.formula1.com/en/racing/2025.html"

def get_next_race():
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Procura todas as divs que contêm os eventos
        event_cards = soup.select(".event-card")

        if not event_cards:
            return {"erro": "Nenhuma corrida encontrada no HTML."}

        now = datetime.now()

        for card in event_cards:
            round_info = card.select_one(".card-title")
            date_info = card.select_one(".date")
            location_info = card.select_one(".event-title")

            if not round_info or not date_info or not location_info:
                continue

            # Extrair texto
            round_name = round_info.text.strip()
            location = location_info.text.strip()
            date_range = date_info.text.strip()  # Ex: "28 – 30 NOV"

            # Extrair última data (dia final da corrida)
            match = re.search(r"(\d{1,2})\s*–\s*(\d{1,2})\s+([A-Z]+)", date_range)
            if not match:
                continue

            end_day = match.group(2)
            month_abbr = match.group(3)
            year = now.year

            # Monta a data completa
            full_date_str = f"{end_day} {month_abbr} {year}"
            try:
                race_date = datetime.strptime(full_date_str, "%d %b %Y")
            except ValueError:
                continue

            # Verifica se a corrida ainda está por vir
            if race_date > now:
                return {
                    "proxima_corrida": round_name,
                    "local": location,
                    "data": race_date.strftime("%d/%m/%Y")
                }

        return {"erro": "Nenhuma corrida futura encontrada."}

    except Exception as e:
        return {"erro": str(e)}

if __name__ == "__main__":
    resultado = get_next_race()
    print(resultado)
