import streamlit as st
from services.backend import chatbot  # <--- AGORA CORRETO
from backend import login_execute, criar_usuario, fetch_logs

st.set_page_config(page_title="Chatbot F1", page_icon="🏎️")
st.title("🏁 Chatbot de Automobilismo com IA")

# Sidebar de login
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

# Interface com abas após login
if st.session_state.get("logado"):
    tabs = st.tabs(["🤖 Chatbot", "📜 Histórico", "ℹ️ Sobre"])
    
    with tabs[0]:
        st.subheader("Chat com IA sobre corridas")
        pergunta = st.text_input("Faça sua pergunta:")

        if pergunta:
            with st.spinner("Consultando IA..."):
                resposta = chatbot(pergunta)
                st.write(resposta)

    with tabs[1]:
        st.subheader("📚 Histórico de Perguntas")
        logs = fetch_logs(limit=10)
        for log in logs:
            st.markdown(f"**{log['ts'].strftime('%d/%m/%Y %H:%M')}**")
            st.markdown(f"**Pergunta:** {log['pergunta']}")
            st.markdown(f"**Resposta:** {log['resposta']}")
            st.markdown("---")

    with tabs[2]:
        st.subheader("📦 Sobre o Projeto")
        st.markdown("""
        Este chatbot foi desenvolvido para automatizar consultas sobre automobilismo (F1 e afins) com:
        - **Gemini AI** para respostas inteligentes
        - **OpenF1 API** para dados reais de corridas
        - **PostgreSQL** para histórico e login
        - **SerpAPI** para imagens de carros e pilotos
        """)
