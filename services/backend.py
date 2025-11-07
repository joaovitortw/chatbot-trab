import os
import requests
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor

from services.ergast_client import (
    get_f1_calendar,
    get_f1_results_by_round,
    get_f1_standings,
    get_next_event_f1  # <- agora importado de forma unificada
)

from services.backend import (
    search_car_info,
    generate_response
)

# 🔌 Conexão com PostgreSQL
conn = psycopg2.connect(
    host=os.getenv("PGHOST", "localhost"),
    port=os.getenv("PGPORT", "5432"),
    dbname=os.getenv("PGDATABASE", "chatbotdb"),
    user=os.getenv("PGUSER", "postgres"),
    password=os.getenv("PGPASSWORD", "postgres123"),
    connect_timeout=10
)
cursor = conn.cursor(cursor_factory=RealDictCursor)

# 🤖 Função principal do chatbot
def chatbot(query: str) -> str:
    if "próxima corrida" in query.lower() and "f1" in query.lower():
        corrida = get_next_event_f1()
        if corrida:
            nome = corrida.get("raceName", "Nome indisponível")
            data = corrida.get("date", "Data não disponível")
            circuito = corrida.get("Circuit", {}).get("circuitName", "Circuito desconhecido")
            pais = corrida.get("Circuit", {}).get("Location", {}).get("country", "País desconhecido")
            resposta = (
                f"A próxima corrida de Fórmula 1 é o 🏁 **{nome}**, "
                f"que ocorrerá em **{data}** no circuito **{circuito} ({pais})**."
            )
        else:
            resposta = "Desculpe, não consegui obter os dados atualizados da Fórmula 1."
    else:
        # Caso não seja F1, usa IA + SerpAPI
        dados = search_car_info(query)
        resposta = generate_response(query, dados) if dados else "Desculpe, não encontrei informações relevantes."

    # 📝 Registra no banco de dados
    try:
        cursor.execute(
            "INSERT INTO logs (pergunta, resposta, ts) VALUES (%s, %s, %s)",
            (query, resposta, datetime.utcnow())
        )
        conn.commit()
    except Exception as e:
        print(f"Erro ao gravar log: {e}")

    return resposta
