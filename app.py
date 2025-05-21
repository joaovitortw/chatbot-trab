# app.py (front-end)

import streamlit as st
import pandas as pd
from backend import chatbot, fetch_logs, login_execute

st.set_page_config(page_title="🚗 FUELTECO dos Carros", layout="wide")

# CSS básico
st.markdown("""
<style>
.stApp h1 {
    text-align: center;
    margin-bottom: 0.5rem;
}
div.stButton > button {
    border-radius: 8px;
    padding: 0.5rem 1rem;
}
.stExpander {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# Controle de sessão para login
if "logado" not in st.session_state:
    st.session_state["logado"] = False
if "usuario" not in st.session_state:
    st.session_state["usuario"] = ""

if not st.session_state["logado"]:
    st.title("🔐 Login para acessar o FUELTECO dos Carros")
    usuario_input = st.text_input("Usuário", key="input_usuario")
    senha_input = st.text_input("Senha", type="password", key="input_senha")
    
    if st.button("Entrar"):
        if login_execute(usuario_input, senha_input):
            st.session_state["logado"] = True
            st.session_state["usuario"] = usuario_input
            # API atualizada do Streamlit:
            try:
                st.rerun()
            except AttributeError:
                st.experimental_rerun()
        else:
            st.error("Usuário ou senha incorretos. Tente novamente.")
else:
    st.title("🚗 FUELTECO dos Carros")
    st.write(f"Bem-vindo, **{st.session_state['usuario']}**! Faça sua pergunta sobre carros.")

    example_queries = [
        "Qual é o consumo médio de um Honda Civic?",
        "Qual a velocidade máxima de uma Ferrari 458?",
        "Quais carros usam o motor C20XE?",
        "Qual a autonomia de um Tesla Model 3?",
        "Quais são os melhores SUVs para famílias?"
    ]

    st.markdown("**Clique para usar um exemplo:**")
    cols = st.columns(len(example_queries))
    for i, (col, example) in enumerate(zip(cols, example_queries)):
        if col.button(example, key=f"ex_btn_{i}"):
            st.session_state["query_input"] = example

    with st.form(key="ask_form", clear_on_submit=False):
        query = st.text_input(
            "Faça sua pergunta:",
            value=st.session_state.get('query_input', ''),
            placeholder="Ex: Qual a autonomia de um Tesla Model 3?"
        )
        submitted = st.form_submit_button(label="🔍 Perguntar")
        if submitted:
            if not query:
                st.warning("Digite uma pergunta antes de enviar.")
            else:
                with st.spinner("Buscando resposta..."):
                    resposta = chatbot(query)
                st.success(resposta)

    with st.expander("📜 Histórico de Conversas", expanded=False):
        logs = fetch_logs(limit=50)
        if logs:
            df = pd.DataFrame(logs)
            df['Timestamp'] = pd.to_datetime(df['ts']).dt.strftime('%Y-%m-%d %H:%M:%S')
            df = df[['Timestamp', 'pergunta', 'resposta']]
            df.columns = ['Timestamp', 'Pergunta', 'Resposta']
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Ainda não há registros de conversas.")

    # Botão sair
    if st.button("Sair"):
        st.session_state["logado"] = False
        st.session_state["usuario"] = ""
        try:
            st.rerun()
        except AttributeError:
            st.experimental_rerun()
