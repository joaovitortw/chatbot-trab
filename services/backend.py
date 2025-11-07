import os
import requests
from datetime import datetime, timezone
import psycopg2
from psycopg2.extras import RealDictCursor

# API OpenF1 para eventos futuros
from services.f1_api_client import get_next_event_f1

# IA + SerpAPI
from services.utils import (
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
    query_lower = query.lower()

    if "próxima corrida" in query_lower and "f1" in query_lower:
        corrida = get_next_event_f1()
        if corrida:
            nome = corrida.get("meeting_name", "Nome indisponível")
            data_str = corrida.get("date_utc", "Data não disponível")[:10]
            circuito = corrida.get("location", "Local desconhecido")

            # 🕒 Contagem regressiva (dias)
            try:
                corrida_dt = datetime.fromisoformat(
                    corrida.get("date_utc", "").replace("Z", "+00:00")
                )
                dias_restantes = (corrida_dt - datetime.now(timezone.utc)).days
                countdown_info = f"\n\n📅 Faltam **{dias_restantes} dias** para o evento!"
            except Exception as e:
                print(f"Erro ao calcular contagem regressiva: {e}")
                countdown_info = ""

            resposta = (
                f"A próxima corrida de Fórmula 1 é o **{nome}**, "
                f"que ocorrerá em **{data_str}**, no circuito de **{circuito}**."
                f"{countdown_info}"
            )
        else:
            resposta = "Desculpe, não consegui obter dados atualizados da próxima corrida de F1."

    else:
        # IA + imagens (sem dados da OpenF1)
        try:
            dados = search_car_info(query)
            resposta = generate_response(query, dados) if dados else "Desculpe, não encontrei informações relevantes."
        except Exception as e:
            print(f"Erro ao usar IA/SerpAPI: {e}")
            resposta = "Desculpe, ocorreu um erro ao buscar a resposta com IA."

    # 🗃️ Log no banco de dados
    try:
        cursor.execute(
            "INSERT INTO logs (pergunta, resposta, ts) VALUES (%s, %s, %s)",
            (query, resposta, datetime.utcnow())
        )
        conn.commit()
    except Exception as e:
        print(f"Erro ao gravar log: {e}")

    return resposta
