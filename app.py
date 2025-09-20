import streamlit as st
import pandas as pd
import io
from utils import (
    adaptar_csv_biblioteca,
    criar_dj_set,
    plotar_curva_de_vibe
    # exportar_set_para_mixxx_csv # Garanta que esta função está em utils.py
)

# --- CONFIGURAÇÃO DA PÁGINA E ESTADO INICIAL ---
st.set_page_config(
    page_title="DJ Set Creator", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicialização do st.session_state no início do script
if 'biblioteca_limpa' not in st.session_state:
    st.session_state.biblioteca_limpa = None
if 'df_set_gerado' not in st.session_state:
    st.session_state.df_set_gerado = None
if 'csv_para_download' not in st.session_state:
    st.session_state.csv_para_download = ""

# --- CABEÇALHO PRINCIPAL ---
st.title("🎧 DJ Set Creator")
st.markdown("1. ⏪️ Acesse o Painel de Controles na barra lateral")
st.markdown("2. 🆙 Faça upload das suas musicas")
st.markdown("3. Configure e crie um DJ SET, com o poder da `Ciência de dados` 🦾🎲")

# ==============================================================================
# SEÇÃO 1: SIDEBAR - Onde todos os inputs e ações do usuário acontecem
# ==============================================================================
with st.sidebar:
    st.title("⚙️ Painel de Controles do Set")
    st.subheader("1. Use seu software DJ favorito para exportar sua biblioteca ou playlist como .CSV")
    
    uploaded_file = st.file_uploader(
        label="Carregue aqui seu seu arquivo .csv", 
        type=["csv"]
    )

    # Processamento do arquivo de upload
    if uploaded_file is not None:
        try:
            # `st.spinner` mostra uma mensagem de "carregando" enquanto o bloco é executado.
            with st.spinner('Processando e limpando sua biblioteca...'):
                df_real = None
            # Usamos getvalue() para ler em memória e permitir múltiplas leituras
                file_bytes = uploaded_file.getvalue()
            
                try:
                    # Tentativa 1: UTF-8
                    df_real = pd.read_csv(io.BytesIO(file_bytes), encoding='utf-8')
                except (UnicodeDecodeError, KeyError):
                    # Tentativa 2 (Fallback): latin-1
                    df_real = pd.read_csv(io.BytesIO(file_bytes), encoding='latin-1')
                if df_real is None:
                    raise ValueError("Não foi possível ler o arquivo CSV com os encodings suportados.")
                
            # Atualiza o estado da sessão com a biblioteca limpa
            st.session_state.biblioteca_limpa = adaptar_csv_biblioteca(df_real)
            # Reseta qualquer set antigo se uma nova biblioteca for carregada
            st.session_state.df_set_gerado = None
            st.session_state.csv_para_download = ""
        except Exception as e:
            st.error(f"Erro ao processar o arquivo: {e}")
            st.session_state.biblioteca_limpa = None

    # --- Controles de Geração de Set (só aparecem se a biblioteca foi carregada) ---
    if st.session_state.biblioteca_limpa is not None:
        df_limpo = st.session_state.biblioteca_limpa
        st.success(f"Biblioteca carregada! {len(df_limpo)} músicas encontradas.")
        
        st.header("2. Configure o Set")
        lista_musicas = ["Automático"] + df_limpo['title'].tolist()
        musica_inicial = st.selectbox("Música Inicial", options=lista_musicas)
        tamanho_set = st.slider("Tamanho do Set (número de músicas)", min_value=5, max_value=100, value=20, step=1, width=340)
        curva_str = st.text_input("Curva de 'Vibe'", value="up-mid-down-up")
        
        st.header("3. Regras de Seleção")
        bpm_tolerancia = st.slider("Variação de BPM permitida", min_value=1, max_value=60, value=8, step=1, width=340)
        peso_bpm = st.slider("BPM Sync (prioriza BPMs iguais)", min_value=0.0, max_value=1.0, value=0.5, step=0.05, width=340)
        peso_key = 1.0 - peso_bpm
        st.slider("Mixagem Harmônica (prioriza KEYs iguais)", value=peso_key, disabled=True, width=340)

        # Botão de Ação para gerar o set
        if st.button("▶️ Criar DJ Set!", width="stretch"):
            with st.spinner('Criando seu DJ Set personalizado...'):
                musica_inicial_final = None if musica_inicial == "Automático" else musica_inicial
                
                # Executa a lógica principal e atualiza o estado da sessão
                df_set_gerado = criar_dj_set(
                    biblioteca=df_limpo,
                    tamanho_set=int(tamanho_set),
                    curva_energia_str=curva_str,
                    musica_inicial_nome=musica_inicial_final,
                    bpm_tolerancia=int(bpm_tolerancia),
                    pesos={'bpm': peso_bpm, 'key': peso_key}
                )
                st.session_state.df_set_gerado = df_set_gerado
                
                # Prepara os dados para download IMEDIATAMENTE e salva no estado
                if not df_set_gerado.empty:
                    st.session_state.csv_para_download = df_set_gerado.to_csv(index=False)
                else:
                    st.session_state.csv_para_download = ""

        st.header("4. Exportar o Set")
        
        # O botão de download AGORA lê o estado que foi atualizado na mesma execução (se o botão 'Criar' foi clicado)
        st.download_button(
           label="📥 Baixar DJ Set",
           data=st.session_state.csv_para_download,
           file_name="meu_set_inteligente.csv",
           mime="text/csv",
           disabled=(st.session_state.df_set_gerado is None or st.session_state.df_set_gerado.empty),
           width="stretch",
           help="Crie um set para habilitar o download."
        )

# ==============================================================================
# SEÇÃO 3: ÁREA PRINCIPAL - Apenas exibe os resultados com base no estado
# ==============================================================================

# Lógica de Exibição: Mostra o conteúdo apropriado com base no que está no st.session_state
if st.session_state.df_set_gerado is not None and not st.session_state.df_set_gerado.empty:
    st.success("✅ DJ Set criado com sucesso!")
    
    st.subheader("📊 Visualização da Vibe")
    fig = plotar_curva_de_vibe(st.session_state.df_set_gerado)
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("🎶 Seu DJ Set Personalizado")
    st.dataframe(st.session_state.df_set_gerado[['title', 'artist', 'bpm', 'key', 'vibe', 'transition_name', 'transition_effect', 'transition_icon', 'transition_score']])

elif st.session_state.biblioteca_limpa is not None:
    # Este é o estado DEPOIS do upload, mas ANTES de gerar o set
    st.subheader("Sua Biblioteca (Limpa e Formatada)")
    st.dataframe(st.session_state.biblioteca_limpa[['title', 'artist', 'bpm', 'key']])
else:
    # Este é o estado inicial, antes de qualquer upload
    st.info("Aguardando o upload do seu arquivo CSV na barra lateral para começar.")