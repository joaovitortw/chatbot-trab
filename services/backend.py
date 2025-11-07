import os
import requests
from datetime import datetime, timezone
import psycopg2
from psycopg2.extras import RealDictCursor

# ✅ Corrigido: Função correta da Hyprace
from services.hyprace_client import get_next_race

# ✅ IA + SerpAPI
from services.utils import search_car_info, generate_response

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


def chatbot(query: str) -> str:
    query_lower = query.lower()

    if "próxima corrida" in query_lower and "f1" in query_lower:
        corrida = get_next_race()
        if corrida:
            nome = corrida.get("name", "Nome indisponível")
            circuito = corrida.get("circuit", "Local desconhecido")
            data_str = corrida.get("start", "Data desconhecida")
            dias = corrida.get("countdown", "")

            countdown_info = f"\n\n📅 Faltam **{dias} dias** para o evento!" if dias else ""

            resposta = (
                f"A próxima corrida de Fórmula 1 é o **{nome}**, "
                f"que ocorrerá em **{data_str}**, no circuito de **{circuito}**."
                f"{countdown_info}"
            )
        else:
            resposta = "Desculpe, não há corridas futuras cadastradas na API."
    else:
        try:
            dados = search_car_info(query)
            resposta = generate_response(query, dados) if dados else "Desculpe, não encontrei informações relevantes."
        except Exception as e:
            print(f"Erro ao usar IA/SerpAPI: {e}")
            resposta = "Desculpe, ocorreu um erro ao buscar a resposta com IA."

    try:
        cursor.execute(
            "INSERT INTO logs (pergunta, resposta, ts) VALUES (%s, %s, %s)",
            (query, resposta, datetime.utcnow())
        )
        conn.commit()
    except Exception as e:
        print(f"Erro ao gravar log: {e}")

    return resposta
