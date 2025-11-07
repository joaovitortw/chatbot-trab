# backend.py (raiz) — Gerenciador central do backend do projeto

import os
import requests
import google.generativeai as genai
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

# Configuração das APIs com variáveis de ambiente
gemini_api_key = os.getenv("GEMINI_API_KEY", "AIzaSyD8NuvzLTRcmdSSsNsgZ8G7OqDhKtM9POs")
SERP_API_KEY = os.getenv("SERP_API_KEY", "2a5d0a505457f4743be1f1e7994b5384ff5def525b5e0191a99bac4e1dd26cd5")

# Inicializa Gemini
genai.configure(api_key=gemini_api_key)

# 🔌 Conexão com o banco PostgreSQL
conn = psycopg2.connect(
    host=os.getenv("PGHOST", "localhost"),
    port=os.getenv("PGPORT", "5432"),
    dbname=os.getenv("PGDATABASE", "chatbotdb"),
    user=os.getenv("PGUSER", "postgres"),
    password=os.getenv("PGPASSWORD", "postgres123"),
    connect_timeout=10
)
cursor = conn.cursor(cursor_factory=RealDictCursor)

# Tabelas (se não existirem)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id SERIAL PRIMARY KEY,
        pergunta TEXT NOT NULL,
        resposta TEXT NOT NULL,
        ts TIMESTAMP NOT NULL
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
""")
conn.commit()

# === Funções utilitárias ===

def fetch_logs(limit: int = 20):
    """Retorna as últimas conversas salvas."""
    cursor.execute("""
        SELECT pergunta, resposta, ts
        FROM logs
        ORDER BY ts DESC
        LIMIT %s
    """, (limit,))
    return cursor.fetchall()

def search_car_info(query: str) -> dict:
    """Busca imagens e informações de carros via SerpAPI."""
    url = f"https://serpapi.com/search.json?q={query}+car&tbm=isch&api_key={SERP_API_KEY}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"Erro ao consultar SerpAPI: {e}")
        return {}

def generate_response(query: str, search_results: dict) -> str:
    """Gera resposta com Gemini e adiciona imagem se disponível."""
    image_url = ""
    images = search_results.get("images_results", [])
    if images:
        image_url = images[0].get("original") or images[0].get("thumbnail")

    prompt = f"O usuário perguntou: {query}\nResponda de forma clara e objetiva."

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        out = model.generate_content(prompt)
        resposta = out.text.strip()

        if image_url:
            resposta += f"\n\n🔗 Veja uma imagem relacionada: {image_url}"
        return resposta
    except Exception as e:
        print(f"Erro ao gerar resposta com Gemini: {e}")
        return "Desculpe, ocorreu um erro ao gerar a resposta."

# === Autenticação ===

def login_execute(username: str, password: str) -> bool:
    """Valida credenciais simples (sem hash)."""
    try:
        cursor.execute("SELECT password FROM users WHERE username = %s", (username.strip(),))
        row = cursor.fetchone()
        return row and row["password"] == password.strip()
    except Exception as e:
        print(f"Erro no login: {e}")
        return False

def criar_usuario(username: str, password: str):
    """Cria novo usuário com nome e senha simples (sem hash)."""
    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username.strip(), password.strip())
        )
        conn.commit()
        print("Usuário criado com sucesso.")
    except Exception as e:
        print(f"Erro ao criar usuário: {e}")
