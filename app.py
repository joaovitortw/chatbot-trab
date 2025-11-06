import streamlit as st
from backend import chatbot, login_execute, criar_usuario

st.set_page_config(page_title="Chatbot F1", page_icon="🏎️")
st.title("🏁 Chatbot de Automobilismo com IA")

# Login lateral
with st.sidebar:
    st.subheader("🔐 Acesso")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Entrar"):
            if login_execute(usuario, senha):
                st.session_state["logado"] = True
                st.session_state["usuario"] = usuario
                st.success("Login bem-sucedido!")
            else:
                st.error("Usuário ou senha incorretos")

    with col2:
        if st.button("Criar Conta"):
            criar_usuario(usuario, senha)
            st.success("Usuário criado com sucesso.")

# Verifica login antes de mostrar chatbot
if st.session_state.get("logado"):
    st.subheader(f"Bem-vindo, {st.session_state['usuario']}!")
    pergunta = st.text_input("Faça uma pergunta sobre F1 ou carros:")

    if pergunta:
        with st.spinner("Consultando IA..."):
            resposta = chatbot(pergunta)
            st.write(resposta)
