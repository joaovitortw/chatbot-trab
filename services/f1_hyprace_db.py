# services/f1_hyprace_db.py

import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timezone
import os

# Conexão com PostgreSQL
conn = psycopg2.connect(
    host=os.getenv("PGHOST", "localhost"),
    port=os.getenv("PGPORT", "5432"),
    dbname=os.getenv("PGDATABASE", "chatbotdb"),
    user=os.getenv("PGUSER", "postgres"),
    password=os.getenv("PGPASSWORD", "postgres123"),
    connect_timeout=10
)
cursor = conn.cursor(cursor_factory=RealDictCursor)

def get_proxima_corrida():
    try:
        now = datetime.now(timezone.utc)
        cursor.execute("""
            SELECT *
            FROM corridas
            WHERE date > %s
            ORDER BY date ASC
            LIMIT 1
        """, (now,))
        corrida = cursor.fetchone()
        return corrida
    except Exception as e:
        print(f"Erro ao buscar próxima corrida: {e}")
        return None
