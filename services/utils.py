# services/utils.py

import os
import requests
import google.generativeai as genai

# === Configuração das APIs ===
gemini_api_key = os.getenv("GEMINI_API_KEY", "AIzaSyD8NuvzLTRcmdSSsNsgZ8G7OqDhKtM9POs")
SERP_API_KEY = os.getenv("SERP_API_KEY", "2a5d0a505457f4743be1f1e7994b5384ff5def525b5e0191a99bac4e1dd26cd5")
genai.configure(api_key=gemini_api_key)


# === Pesquisa na SerpAPI ===
def search_car_info(query: str) -> dict:
    url = f"https://serpapi.com/search.json?q={query}+car&tbm=isch&api_key={SERP_API_KEY}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        print(f"Erro ao consultar SerpAPI: {e}")
        return {}


# === Geração de resposta com Gemini AI ===
def generate_response(query: str, search_results: dict) -> str:
    image_url = ""
    images = search_results.get("images_results", [])
    if images:
        image_url = images[0].get("original") or images[0].get("thumbnail")

    prompt = f"O usuário perguntou: {query}\nResponda de forma clara e objetiva."

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
