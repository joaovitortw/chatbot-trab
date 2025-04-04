import streamlit as st
from chatbot import chatbot  # Importa a função principal do chatbot

# Configuração da interface
st.title("🚗 Chatbot de Carros")
st.write("Digite sua pergunta sobre carros e obtenha uma resposta!")

# Campo de entrada para o usuário
query = st.text_input("Faça sua pergunta:")

# Botão para enviar a pergunta
if st.button("Perguntar"):
    if query.strip():
        with st.spinner("Buscando resposta..."):
            resposta = chatbot(query)  # Obtém a resposta do chatbot
        st.write("**Resposta:**")
        st.write(resposta)
    else:
        st.warning("Por favor, digite uma pergunta válida.")
