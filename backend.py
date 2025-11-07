# backend.py (back-end atualizado com OpenF1 API)

import os
import requests
import google.generativeai as genai
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

# Importa a nova API da OpenF1
from services.f1_api_client import (
    get_next_event_f1,
    get_f1_calendar,
    get_f1_results_by_round,
    get_f1_standings
)

# Configuração das APIs usando variáveis de ambiente com fallback
gemini_api_key = os.getenv("GEMINI_API_KEY", "AIzaSyD8NuvzLTRcmdSSsNsgZ8G7OqDhKtM9POs")
if not gemini_api_key:
    raise RuntimeError("GEMINI_API_KEY não definido e não há chave fallback.")
genai.configure(api_key=gemini_api_key)

SERP_API_KEY = os.getenv("SERP_API_KEY", "2a5d0a505457f4743be1f1e7994b5384ff5def525b5e0191a99bac4e1dd26cd5")
if not SERP_API_KEY:
    raise RuntimeError("SERP_API_KEY não definido e não há chave fallback.")

# Conexão com PostgreSQL usando variáveis de ambiente
conn = psycopg2.connect(
    host=os.getenv("PGHOST", "localhost"),
    port=os.getenv("PGPORT", "5432"),
    dbname=os.getenv("PGDATABASE", "chatbotdb"),
    user=os.getenv("PGUSER", "postgres"),
    password=os.getenv("PGPASSWORD", "postgres123"),
    connect_timeout=10
)
cursor = conn.cursor(cursor_factory=RealDictCursor)

# Criação da tabela logs se não existir
cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id SERIAL PRIMARY KEY,
        pergunta TEXT NOT NULL,
        resposta TEXT NOT NULL,
        ts TIMESTAMP NOT NULL
    )
""")
conn.commit()

# Criação da tabela users se não existir
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
""")
conn.commit()

# Função para buscar histórico de conversas
def fetch_logs(limit: int = 20):
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        SELECT pergunta, resposta, ts
        FROM logs
        ORDER BY ts DESC
        LIMIT %s
    """, (limit,))
    return cur.fetchall()


# === 🔎 Pesquisa de imagem com SerpAPI ===
def search_car_info(query: str) -> dict:
    url = f'https://serpapi.com/search.json?q={query}+car&tbm=isch&api_key={SERP_API_KEY}'
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        print(f"Erro ao consultar SerpAPI: {e}")
        return {}


# === 🤖 Geração de resposta com Gemini AI ===
def generate_response(query: str, search_results: dict) -> str:
    image_url = ""
    images = search_results.get("images_results", [])
    if images:
        image_url = images[0].get("original") or images[0].get("thumbnail")

    prompt = f"""
O usuário perguntou sobre: {query}
Responda de forma clara e objetiva, baseada no conhecimento atual do modelo.
"""

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        out = model.generate_content(prompt)
        resposta_texto = out.text.strip()

        if image_url:
            resposta_texto += f"\n\n🔗 Veja uma imagem relacionada: {image_url}"
        return resposta_texto

    except Exception as e:
        print(f"Erro na geração de conteúdo: {e}")
        return "Desculpe, ocorreu um erro ao gerar a resposta."


# === 💬 Função principal do chatbot ===
def chatbot(query: str) -> str:
    """Processa a entrada do usuário e decide se usa a IA ou a API de F1."""
    try:
        # Caso a pergunta seja sobre a próxima corrida da F1
        if "próxima corrida" in query.lower() and "f1" in query.lower():
            corrida = get_next_event_f1()
            if corrida:
                nome = corrida.get("meeting_name", "Nome indisponível")
                data = corrida.get("date_utc", "Data não disponível")[:10]
                circuito = corrida.get("location", "Circuito desconhecido")

                resposta = (
                    f"A próxima corrida de Fórmula 1 é o 🏁 **{nome}**, "
                    f"que ocorrerá em **{data}** no circuito **{circuito}**."
                )
            else:
                resposta = "Desculpe, não consegui obter os dados atualizados da Fórmula 1."
        else:
            # Caso não seja F1 → usa SerpAPI + Gemini
            dados = search_car_info(query)
            resposta = generate_response(query, dados) if dados else "Desculpe, não encontrei informações relevantes."

        # Salva o log no banco de dados
        cursor.execute(
            "INSERT INTO logs (pergunta, resposta, ts) VALUES (%s, %s, %s)",
            (query, resposta, datetime.utcnow())
        )
        conn.commit()
        return resposta

    except Exception as e:
        print(f"Erro no chatbot: {e}")
        return "Desculpe, ocorreu um erro ao processar sua solicitação."


# === 🔐 Login simples ===
def login_execute(username: str, password: str) -> bool:
    try:
        cursor.execute("SELECT password FROM users WHERE username = %s", (username.strip(),))
        row = cursor.fetchone()
        if not row:
            return False
        return row["password"] == password.strip()
    except Exception as e:
        print(f"Erro no login: {e}")
        return False


# === 👤 Criar novo usuário ===
def criar_usuario(username: str, password: str):
    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username.strip(), password.strip())
        )
        conn.commit()
        print("Usuário criado com sucesso.")
    except Exception as e:
        print(f"Erro ao criar usuário: {e}")
