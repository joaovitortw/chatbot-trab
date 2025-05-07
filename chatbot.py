import os
import requests
import google.generativeai as genai
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

# Configurações das APIs
genai.configure(api_key=os.getenv("GEMINI_API_KEY", "SEU_API_KEY_GEMINI"))
SERP_API_KEY = os.getenv(
    "SERP_API_KEY",
    "SEU_API_KEY_SERPAPI"
)

# Conexão com PostgreSQL
conn = psycopg2.connect(
    host     = os.getenv("PGHOST", "localhost"),
    port     = os.getenv("PGPORT", "5432"),
    dbname   = os.getenv("PGDATABASE", "chatbotdb"),
    user     = os.getenv("PGUSER", "postgres"),
    password = os.getenv("PGPASSWORD", "!!!!!SUASENHAAQUI!!!!!")
)
cursor = conn.cursor(cursor_factory=RealDictCursor)

# Cria tabela de logs se não existir
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS logs (
      id SERIAL PRIMARY KEY,
      pergunta TEXT NOT NULL,
      resposta TEXT NOT NULL,
      ts TIMESTAMP NOT NULL
    )
    """
)
conn.commit()

# Função para buscar histórico de conversas
def fetch_logs(limit: int = 20):
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        """
        SELECT pergunta, resposta, ts
          FROM logs
      ORDER BY ts DESC
         LIMIT %s
        """,
        (limit,)
    )
    return cur.fetchall()

# Função para buscar informações sobre carros via SerpAPI
def search_car_info(query: str) -> dict:
    url = f'https://serpapi.com/search?q={query}+car&api_key={SERP_API_KEY}'
    resp = requests.get(url)
    if resp.status_code != 200:
        print("Erro SerpAPI:", resp.status_code, resp.text)
        return {}
    return resp.json()

# Função para gerar resposta com Gemini
def generate_response(query: str, search_results: dict) -> str:
    results = search_results.get('organic_results', [])[:7]
    if not results:
        return "Nenhum resultado encontrado para essa consulta."
    summary = "\n".join(f"• {r['title']}: {r['snippet']}" for r in results)
    prompt = f"""
O usuário perguntou sobre carros: {query}
Aqui estão alguns resultados encontrados:
{summary}

Baseado nessas informações, forneça uma resposta clara e concisa para o usuário:
"""
    model = genai.GenerativeModel("gemini-2.0-flash")
    out = model.generate_content(prompt)
    return out.text.strip()

# Função principal do chatbot que grava no banco
def chatbot(query: str) -> str:
    dados = search_car_info(query)
    resposta = generate_response(query, dados) if dados else "Desculpe, não encontrei informações relevantes."

    # Grava log da conversa
    cursor.execute(
        "INSERT INTO logs (pergunta, resposta, ts) VALUES (%s, %s, %s)",
        (query, resposta, datetime.utcnow())
    )
    conn.commit()

    return resposta

# Execução standalone para testes
if __name__ == "__main__":
    q = input("Pergunte sobre carros: ")
    print(chatbot(q))