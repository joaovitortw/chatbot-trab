import streamlit as st
import pandas as pd
from chatbot import chatbot, fetch_logs

# Configuração da página
st.set_page_config(
    page_title="🚗 FUELTECO dos Carros",
    layout="wide"
)

st.title("🚗 FUELTECO dos Carros")
st.write("Digite sua pergunta sobre carros e obtenha uma resposta!")

# Entrada de pergunta e exibição de resposta
query = st.text_input("Faça sua pergunta:", key="query_input")
if st.button("Perguntar", key="ask_button"):
    if query.strip():
        with st.spinner("Buscando resposta..."):
            resposta = chatbot(query)
        st.markdown("### Resposta")
        st.write(resposta)
    else:
        st.warning("Por favor, digite uma pergunta válida.")

# Separador visual
st.markdown("---")

# Histórico de conversas em tabela
st.markdown("### Histórico de Conversas (últimas 20)")
logs = fetch_logs(limit=20)
if logs:
    # Converte em DataFrame
    df = pd.DataFrame(logs)
    df['Timestamp'] = pd.to_datetime(df['ts']).dt.strftime("%Y-%m-%d %H:%M:%S")
    df = df[['Timestamp', 'pergunta', 'resposta']]
    df.columns = ['Timestamp', 'Pergunta', 'Resposta']

    # Exibe sem índice e com largura total
    st.dataframe(df, use_container_width=True)
else:
    st.info("Ainda não há registros de conversas.")