import streamlit as st
import pandas as pd
from utils import adaptar_csv_biblioteca

# --- CONFIGURAÇÃO DA PÁGINA ---
# st.set_page_config() é a primeira coisa que você deve rodar.
# Ela define configurações globais da página, como o título na aba do navegador e o layout.
st.set_page_config(
    page_title="DJ Set Creator", 
    layout="wide", # Usa a largura total da tela, ótimo para tabelas e gráficos
    initial_sidebar_state="expanded" # Deixa a barra lateral aberta por padrão
)

# --- CABEÇALHO PRINCIPAL ---
# st.title() cria um texto grande, como um <h1> em HTML.
st.title("🎧 DJ Set Creator Inteligente")
# st.markdown() permite escrever em formato Markdown, ótimo para textos com formatação.
st.markdown("1. Exporte Sua Biblioteca Musical como .CSV usando seu software DJ favorito")
st.markdown("2. Faça upload do arquivo CSV gerado")
st.markdown("3. Use o poder da Ciência de dados para criar um set harmônico!")

# --- BARRA LATERAL (FORMULÁRIO DE CONTROLES) ---
st.sidebar.title("⚙️ Controles do Set")
uploaded_file = st.sidebar.file_uploader(
    label="1. Sua Biblioteca Musical (.csv)", 
    type=["csv"]
)

# --- GERENCIAMENTO DE ESTADO ---
# Inicializamos uma "gaveta" no st.session_state para guardar nossa biblioteca limpa.
if 'biblioteca_limpa' not in st.session_state:
    st.session_state.biblioteca_limpa = None

# --- LÓGICA DE PROCESSAMENTO COM ESTADO ---
# Se um novo arquivo foi enviado, nós o processamos e guardamos na "gaveta".
if uploaded_file is not None:
    # `st.spinner` mostra uma mensagem de "carregando" enquanto o bloco é executado.
    with st.spinner('Processando e limpando sua biblioteca...'):
        try:
            # Usamos latin-1 como fallback, que é comum em CSVs do Windows.
            df_real = pd.read_csv(uploaded_file, encoding='utf-8')
            # CHAMANDO SUA FUNÇÃO DO utils.py!
            st.session_state.biblioteca_limpa = adaptar_csv_biblioteca(df_real)
            st.sidebar.success(f"{len(st.session_state.biblioteca_limpa)} músicas carregadas com sucesso!")
        except Exception as e:
            st.sidebar.error(f"Erro ao processar o arquivo: {e}")
            st.session_state.biblioteca_limpa = None # Reseta em caso de erro

# --- LÓGICA DE EXIBIÇÃO ---
# Agora, em vez de checar o `uploaded_file`, checamos nossa "gaveta".
if st.session_state.biblioteca_limpa is not None:
    st.header("Sua Biblioteca (Limpa e Formatada)")
    st.dataframe(st.session_state.biblioteca_limpa)
else:
    st.info("Aguardando o upload do seu arquivo CSV na barra lateral para começar.")