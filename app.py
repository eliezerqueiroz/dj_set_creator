import streamlit as st
import pandas as pd
from utils import (
    adaptar_csv_biblioteca,
    criar_dj_set_v4,
    plotar_curva_de_vibe
)

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
st.markdown("1. Acesso o Painel de Controles na barra lateral")
st.markdown("2. Faça upload das suas musicas")
st.markdown("3. E veja o poder da `Ciência de dados` criar um set 100% harmônico!")

# --- BARRA LATERAL (FORMULÁRIO DE CONTROLES) ---
st.sidebar.title("⚙️ Painel de Controles do Set")
st.sidebar.subheader("1. Use seu software DJ favorito para exportar sua biblioteca ou playlist como .CSV")
uploaded_file = st.sidebar.file_uploader(
    label="Carregue aqui seu seu arquivo .csv", 
    type=["csv"]
)

# --- GERENCIAMENTO DE ESTADO ---
# Inicializamos uma "gaveta" no st.session_state para guardar nossa biblioteca limpa.
if 'biblioteca_limpa' not in st.session_state:
    st.session_state.biblioteca_limpa = None
if 'df_set_gerado' not in st.session_state: # <-- Inicializa o estado do set gerado
    st.session_state.df_set_gerado = None

# --- LÓGICA DE PROCESSAMENTO COM ESTADO ---
# Se um novo arquivo foi enviado, nós o processamos e guardamos na "st.session_state".
if uploaded_file is not None:
    try:
        # `st.spinner` mostra uma mensagem de "carregando" enquanto o bloco é executado.
        with st.spinner('Processando e limpando sua biblioteca...'):
            # Para ler o arquivo de forma flexível, precisamos "rebobinar" o cursor do arquivo
            # se a primeira tentativa de leitura falhar.
            uploaded_file.seek(0)
            try:
                # TENTATIVA 1: Tenta ler com UTF-8, o padrão mais moderno.
                st.write("Tentando ler o arquivo com encoding UTF-8...")
                df_real = pd.read_csv(uploaded_file, encoding='utf-8')
            except UnicodeDecodeError:
                # TENTATIVA 2 (FALLBACK): Se o UTF-8 falhar, rebobina o arquivo e tenta com latin-1.
                st.write("UTF-8 falhou. Tentando com encoding latin-1...")
                uploaded_file.seek(0)
                df_real = pd.read_csv(uploaded_file, encoding='latin-1')
            
            # Processa e limpa a biblioteca usando a função do utils.py
            st.session_state.biblioteca_limpa = adaptar_csv_biblioteca(df_real)
        
        st.sidebar.success(f"Biblioteca carregada! {len(st.session_state.biblioteca_limpa)} músicas encontradas.")
        st.session_state.df_set_gerado = None # Reseta o set gerado ao carregar uma nova biblioteca
        
    except Exception as e:
        st.sidebar.error(f"Erro ao processar o arquivo: {e}")
        st.session_state.biblioteca_limpa = None # Reseta em caso de erro

# --- LÓGICA DE EXIBIÇÃO DOS CONTROLES---
# Agora, em vez de checar o `uploaded_file`, checamos `st.session_state`
if st.session_state.biblioteca_limpa is not None:
    df_limpo = st.session_state.biblioteca_limpa
    # --- INÍCIO DOS CONTROLES DE AJUSTE ---
    st.sidebar.subheader("2. Configuração do Set")
    # Selectbox para a música inicial. As opções são preenchidas dinamicamente!
    lista_musicas = ["Automático"] + df_limpo['title'].tolist()
    musica_inicial = st.sidebar.selectbox("Música Inicial", options=lista_musicas)
    # Slider para o tamanho do set. Retorna um número inteiro.
    tamanho_set = st.sidebar.slider("Tamanho do Set (número de músicas)", min_value=5, max_value=100, value=20, step=1, width=340)
    # Input de texto para a curva de energia
    curva_str = st.sidebar.text_input("Curva de 'Vibe' do set (ex: up-down-mid-up)", value="up-down-mid-up")
    
    st.sidebar.subheader("3. Regras de seleção de músicas")
    # Slider para a tolerância de BPM
    bpm_tolerancia = st.sidebar.slider("Variação de BPM permitida", min_value=1, max_value=60, value=8, step=1, width=340)

    # Sliders para os pesos de BPM vs. Chave
    peso_bpm = st.sidebar.slider("BPM Sync (prioriza BPMs iguais)", min_value=0.0, max_value=1.0, value=0.5, step=0.05, width=340)
    peso_key = 1.0 - peso_bpm
    st.sidebar.slider("Mixagem Harmônica (prioriza KEYs iguais)", value=peso_key, disabled=True, width=340)
    # st.sidebar.markdown(f"**Foco em Mixagem Harmônica:** `{peso_key:.2f}`")

    criar_set_btn = st.sidebar.button("▶️ Criar meu Set Inteligente!")

    # --- FIM DOS CONTROLES DE AJUSTE ---
    st.subheader("Sua Biblioteca (Limpa e Formatada)")
    st.dataframe(df_limpo)
else:
    st.info("Aguardando o upload do seu arquivo CSV na barra lateral para começar.")


    

