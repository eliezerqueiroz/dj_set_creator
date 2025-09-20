import streamlit as st
import pandas as pd
import io
from utils import (
    adaptar_csv_biblioteca,
    criar_dj_set,
    plotar_curva_de_vibe
    # exportar_set_csv
)

# --- CONFIGURAÇÃO DA PÁGINA ---
# st.set_page_config() é a primeira coisa que você deve rodar.
# Ela define configurações globais da página, como o título na aba do navegador e o layout.
st.set_page_config(
    page_title="DJ Set Creator", 
    layout="wide", # Usa a largura total da tela, ótimo para tabelas e gráficos
    initial_sidebar_state="expanded" # Deixa a barra lateral aberta por padrão
)
# --- GERENCIAMENTO DE ESTADO ---
# Inicializamos uma "gaveta" no st.session_state para guardar nossa biblioteca limpa.
if 'biblioteca_limpa' not in st.session_state:
    st.session_state.biblioteca_limpa = None
if 'df_set_gerado' not in st.session_state: # <-- Inicializa o estado do set gerado
    st.session_state.df_set_gerado = None

# --- CABEÇALHO PRINCIPAL ---
# st.title() cria um texto grande, como um <h1> em HTML.
st.title("🎧 DJ Set Creator")
# st.markdown() permite escrever em formato Markdown, ótimo para textos com formatação.
st.markdown("1. ⏪️ Acesse o Painel de Controles na barra lateral")
st.markdown("2. 🆙 Faça upload das suas musicas")
st.markdown("3. Configure e crie um DJ SET, com o poder da `Ciência de dados` 🦾🎲")

# --- BARRA LATERAL (FORMULÁRIO DE CONTROLES) ---
st.sidebar.title("⚙️ Painel de Controles do Set")
st.sidebar.subheader("1. Use seu software DJ favorito para exportar sua biblioteca ou playlist como .CSV")

# SEÇÃO 1: PROCESSAMENTO DO UPLOAD (MODIFICA O ESTADO)
uploaded_file = st.sidebar.file_uploader(
    label="Carregue aqui seu seu arquivo .csv", 
    type=["csv"]
)
# --- LÓGICA DE PROCESSAMENTO COM ESTADO ---
# Se um novo arquivo foi enviado, nós o processamos e guardamos na "st.session_state".
if uploaded_file is not None:
    try:
        # `st.spinner` mostra uma mensagem de "carregando" enquanto o bloco é executado.
        with st.spinner('Processando e limpando sua biblioteca...'):
            df_real = None
            # Precisamos ler os bytes para poder "rebobinar" o arquivo
            file_bytes = uploaded_file.getvalue()
            
            try:
                # Tentativa 1: Tenta ler com UTF-8, o padrão mais moderno
                df_real = pd.read_csv(io.BytesIO(file_bytes), encoding='utf-8')
            except (UnicodeDecodeError, KeyError):
                # Tentativa 2 (FALLBACK): Se UTF-8 falhar, tenta com latin-1
                df_real = pd.read_csv(io.BytesIO(file_bytes), encoding='latin-1')

            if df_real is None:
                raise ValueError("Não foi possível ler o arquivo CSV com os encodings suportados.")
            
            # Processa e limpa a biblioteca usando a função do utils.py
            st.session_state.biblioteca_limpa = adaptar_csv_biblioteca(df_real)
        
        st.sidebar.success(f"Biblioteca carregada! {len(st.session_state.biblioteca_limpa)} músicas encontradas.")
        st.session_state.df_set_gerado = None # Reseta o set gerado ao carregar uma nova biblioteca

    except Exception as e:
        st.sidebar.error(f"Erro ao processar o arquivo: {e}")
        st.session_state.biblioteca_limpa = None # Reseta em caso de erro

#  SEÇÃO 2: --- LÓGICA DE EXIBIÇÃO DOS CONTROLES NA SIDEBAR E CAPTURA DE PARÂMETROS---
# Esta seção só aparece se o csv estiver carregado.
if st.session_state.biblioteca_limpa is not None:
    df_limpo = st.session_state.biblioteca_limpa

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

    criar_set_btn = st.sidebar.button("▶️ Criar DJ Set!", width="stretch")
 # --- FIM DOS CONTROLES NA SIDEBAR ---

# SEÇÃO 3: LÓGICA DE AÇÃO (MODIFICA O ESTADO)
 # Se o botão "Criar Set!" for pressionado
    if criar_set_btn:
        with st.spinner('Criando seu DJ Set personalizado...'):
            musica_inicial_final = None if musica_inicial == "Automático" else musica_inicial
            df_set_gerado = criar_dj_set(
                biblioteca=df_limpo,
                tamanho_set=int(tamanho_set),
                curva_energia_str=curva_str,
                musica_inicial_nome=musica_inicial_final,
                bpm_tolerancia=int(bpm_tolerancia),
                pesos={'bpm': peso_bpm, 'key': peso_key}
            )
            st.session_state.df_set_gerado = df_set_gerado

# SEÇÃO 4: DESENHO DOS WIDGETS QUE DEPENDEM DO ESTADO ATUALIZADO            
# --- INÍCIO DA FEATURE DE DOWNLOAD NA SIDEBAR ---
    st.sidebar.subheader("4. Exportar Set(.CSV compatível com Mixxx)")
    # A lógica para habilitar/desabilitar o botão
    set_foi_gerado = st.session_state.df_set_gerado is not None and not st.session_state.df_set_gerado.empty
    if set_foi_gerado:
        # Prepara os dados para o download APENAS se um set já foi gerado
        df_para_download = st.session_state.df_set_gerado
        csv_string = df_para_download.to_csv(index=False).encode('utf-8')
    else:
        csv_string = "" # Botão desabilitado não precisa de dados

    st.sidebar.download_button(
       label="📥 Baixar DJ Set",
       data=csv_string,
       width="stretch",
       file_name="meu_set_inteligente.csv",
       mime="text/csv",
       disabled=not set_foi_gerado, # O botão fica desabilitado se `set_foi_gerado` for False
       help="Crie um set para habilitar o download." # Dica que aparece ao passar o mouse
    )
# --- FIM DA FEATURE DE DOWNLOAD NA SIDEBAR ---
# SEÇÃO 5: EXIBIÇÃO NA ÁREA PRINCIPAL
    if st.session_state.df_set_gerado is not None:
        df_set = st.session_state.df_set_gerado

        if not df_set.empty:
            st.success("✅ DJ Set criado com sucesso!")
            st.subheader("📊 Visualização da Vibe")
            fig = plotar_curva_de_vibe(df_set)
            st.plotly_chart(fig, use_container_width=True)
            st.subheader("🎶 Seu DJ Set Personalizado")
            st.dataframe(df_set[['title', 'artist', 'bpm', 'key', 'vibe', 'transition_name', 'transition_effect', 'transition_icon', 'transition_score'] ])
        else:
            st.error("❌ Não foi possível criar um set com os parâmetros fornecidos. Tente ajuste as configurações.")
    else:
        st.subheader("Sua Biblioteca (Limpa e Formatada)")
        st.dataframe(df_limpo[['title', 'artist', 'bpm', 'key']])
else:
    st.info("Aguardando o upload do seu arquivo CSV na barra lateral para começar.")


    

