# populate_f1_races.py

import os
import requests
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

# Configurações da API
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "d4972bd191msh23ae861b3f27a66p12270ajsnbb12b59402af")

headers = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": "hyprace-api.p.rapidapi.com"
}

# Conexão com o PostgreSQL
conn = psycopg2.connect(
    host=os.getenv("PGHOST", "localhost"),
    port=os.getenv("PGPORT", "5432"),
    dbname=os.getenv("PGDATABASE", "chatbotdb"),
    user=os.getenv("PGUSER", "postgres"),
    password=os.getenv("PGPASSWORD", "postgres123"),
    connect_timeout=10
)
cursor = conn.cursor(cursor_factory=RealDictCursor)

# Criação da tabela, se não existir
cursor.execute("""
    CREATE TABLE IF NOT EXISTS f1_races (
        id SERIAL PRIMARY KEY,
        gp_id UUID UNIQUE NOT NULL,
        name TEXT NOT NULL,
        location TEXT,
        country TEXT,
        date_start DATE,
        date_end DATE
    )
""")
conn.commit()

# Função para popular corridas
def populate_races():
    current_year = datetime.now().year
    years_to_try = [current_year, current_year - 1, 2024]  # fallback: tenta anos anteriores

    for year in years_to_try:
        print(f"🔎 Tentando buscar dados para o ano {year}...")
        url = f"https://hyprace-api.p.rapidapi.com/v2/seasons/{year}/grands-prix"
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            data = response.json()
            if not data:
                raise ValueError("Resposta vazia da API.")

            for gp in data:
                gp_id = gp.get("id")
                name = gp.get("name", "Nome desconhecido")
                location = gp.get("location", {}).get("circuit", {}).get("name", "")
                country = gp.get("location", {}).get("country", "")
                start = gp.get("start_date", None)
                end = gp.get("end_date", None)

                # Conversão de datas
                date_start = datetime.fromisoformat(start).date() if start else None
                date_end = datetime.fromisoformat(end).date() if end else None

                cursor.execute("""
                    INSERT INTO f1_races (gp_id, name, location, country, date_start, date_end)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (gp_id) DO NOTHING
                """, (gp_id, name, location, country, date_start, date_end))

            conn.commit()
            print(f"✅ {len(data)} GPs de {year} inseridos com sucesso.")
            return  # Sucesso, sai da função
        except Exception as e:
            print(f"⚠️ Erro ao buscar dados para {year}: {e}")

    print("❌ Não foi possível popular os dados de nenhuma temporada.")

# Execução direta
if __name__ == "__main__":
    populate_races()
