import os
import requests
import google.generativeai as genai
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

# Configuração das APIs usando variáveis de ambiente com fallback
gemini_api_key = os.getenv(
    "GEMINI_API_KEY",
    "AIzaSyD8NuvzLTRcmdSSsNsgZ8G7OqDhKtM9POs"
)
if not gemini_api_key:
    raise RuntimeError("GEMINI_API_KEY não definido e não há chave fallback.")
genai.configure(api_key=gemini_api_key)

SERP_API_KEY = os.getenv(
    "SERP_API_KEY",
    "2a5d0a505457f4743be1f1e7994b5384ff5def525b5e0191a99bac4e1dd26cd5"
)
if not SERP_API_KEY:
    raise RuntimeError("SERP_API_KEY não definido e não há chave fallback.")

# Conexão com PostgreSQL usando variáveis de ambiente
conn = psycopg2.connect(
    host=os.getenv("PGHOST", "localhost"),
    port=os.getenv("PGPORT", "5432"),
    dbname=os.getenv("PGDATABASE", "chatbotdb"),
    user=os.getenv("PGUSER", "postgres"),
    password=os.getenv("PGPASSWORD", "123456"),
    connect_timeout=10
)
cursor = conn.cursor(cursor_factory=RealDictCursor)

# Criação da tabela de logs, se não existir
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

# Pesquisa na SerpAPI com imagens (tbm=isch)
def search_car_info(query: str) -> dict:
    url = f'https://serpapi.com/search.json?q={query}+car&tbm=isch&api_key={SERP_API_KEY}'
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        print(f"Erro ao consultar SerpAPI: {e}")
        return {}

# Geração de resposta com imagem incluída
def generate_response(query: str, search_results: dict) -> str:
    image_url = ""
    images = search_results.get("images_results", [])
    if images:
        image_url = images[0].get("original") or images[0].get("thumbnail")

    prompt = f"""
O usuário perguntou sobre carros: {query}
Gere uma resposta clara e objetiva sobre esse tema, com base no conhecimento atual do modelo.
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

# Função principal do chatbot
def chatbot(query: str) -> str:
    dados = search_car_info(query)
    resposta = generate_response(query, dados) if dados else "Desculpe, não encontrei informações relevantes."

    try:
        cursor.execute(
            "INSERT INTO logs (pergunta, resposta, ts) VALUES (%s, %s, %s)",
            (query, resposta, datetime.utcnow())
        )
        conn.commit()
    except Exception as e:
        print(f"Erro ao gravar log: {e}")

    return resposta

# Execução standalone
if __name__ == "__main__":
    q = input("Pergunte sobre carros: ")
    print("\n" + chatbot(q))
