import google.generativeai as genai
import requests
import os

# Configurar a chave da API Gemini
genai.configure(api_key="AIzaSyD8NuvzLTRcmdSSsNsgZ8G7OqDhKtM9POs") 


def search_car_info(query):
    serp_api_key = '2a5d0a505457f4743be1f1e7994b5384ff5def525b5e0191a99bac4e1dd26cd5'
    search_url = f'https://serpapi.com/search?q={query}+car&api_key={serp_api_key}'
    response = requests.get(search_url)

    if response.status_code == 200:
        data = response.json()
        print("Resultados relevantes da API SerpAPI:")
        if 'organic_results' in data:
            for i, result in enumerate(data['organic_results'][:3]):
                print(f"\nResultado {i+1}:")
                print(f"**Título**: {result['title']}")
                print(f"**Descrição**: {result['snippet']}")
                print("-" * 50)
        else:
            print("Nenhum resultado encontrado.")
        return data
    else:
        print(f"Erro ao acessar a API: {response.status_code} - {response.text}")
        return None

def generate_response(query, search_results):
    if 'organic_results' in search_results:
        search_summary = "\n".join([
            f"{result['title']}: {result['snippet']}" 
            for result in search_results['organic_results'][:3]
        ])
    else:
        return "Nenhum resultado encontrado para essa consulta."

    prompt = f"""O usuário perguntou sobre carros: {query}
Aqui estão alguns resultados encontrados:
{search_summary}

Baseado nessas informações, forneça uma resposta clara e concisa para o usuário:"""

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text.strip()

def chatbot(query):
    search_results = search_car_info(query)
    if search_results:
        return generate_response(query, search_results)
    else:
        return "Desculpe, não encontrei informações relevantes na web."

if __name__ == "__main__":
    query = input("Pergunte sobre carros: ")
    answer = chatbot(query)
    print("\nResposta do assistente:")
    print(answer)
