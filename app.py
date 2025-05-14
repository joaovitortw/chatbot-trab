import streamlit as st
import pandas as pd
from chatbot import chatbot, fetch_logs

# ─── Configuração da página e CSS ───────────────────────────────────────────────
st.set_page_config(page_title="🚗 FUELTECO dos Carros", layout="wide")
st.markdown("""
<style>
/* Centraliza o título */
.stApp h1 {
    text-align: center;
    margin-bottom: 0.5rem;
}
/* Estiliza formulários e botões */
div.stButton > button {
    border-radius: 8px;
    padding: 0.5rem 1rem;
}
/* Estilo dos expanders */
.stExpander {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# ─── Exemplos de perguntas ──────────────────────────────────────────────────────
example_queries = [
    "Qual é o consumo médio de um Honda Civic?",
    "Qual a velocidade máxima de uma Ferrari 458?",
    "Quais carros usam o motor C20XE?",
    "Qual a autonomia de um Tesla Model 3?",
    "Quais são os melhores SUVs para famílias?"
]

# ─── Sidebar com instruções e exemplos ──────────────────────────────────────────
with st.sidebar:
    st.header("📝 Exemplos de Perguntas")
    for i, ex in enumerate(example_queries):
        if st.button(f"💡 {ex}", key=f"sidebar_ex_{i}"):
            st.session_state['query_input'] = ex
    st.markdown("---")
    st.write(
        "🤖 **Como usar:**\n"
        "- Escolha um exemplo clicando no botão acima, ou\n"
        "- Digite sua própria pergunta no formulário.\n"
        "- Clique em **🔍 Perguntar** e aguarde a resposta."
    )

# ─── Cabeçalho ──────────────────────────────────────────────────────────────────
st.title("🚗 FUELTECO dos Carros")
st.write("Uma forma fácil e rápida de obter informações sobre carros.")

# ─── Formulário de entrada ──────────────────────────────────────────────────────
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

# ─── Histórico de conversas ──────────────────────────────────────────────────────
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
