import streamlit as st
import pandas as pd
import io
import os
from utils import (
    adaptar_csv_biblioteca,
    criar_dj_set,
    plotar_curva_de_vibe,
    exportar_set_csv
)

# --- CONFIGURAÇÃO DA PÁGINA E ESTADO INICIAL ---
st.set_page_config(
    page_title="DJ Set Creator", 
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/eliezerqueiroz/dj_set_creator',
        'About': "![Eliezer Queiroz](https://avatars.githubusercontent.com/u/60445437?v=4)\n\n Desenvolvido por Eliezer Queiroz: [GitHub]('https://github.com/eliezerqueiroz') | [LinkedIn](https://www.linkedin.com/in/eliezerqueiroz/)"
    }
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
# st.markdown("1. ⏪️ Acesse o Painel de Controles na barra lateral")
# st.markdown("2. 🆙 Faça upload das suas musicas")
# st.markdown("3. Configure e crie um DJ SET, com o poder da `Ciência de dados` 🦾🎲")

# ==============================================================================
# SEÇÃO 1: SIDEBAR - Onde todos os inputs e ações do usuário acontecem
# ==============================================================================
with st.sidebar:
    # Callback para carregar os dados de exemplo
    def carregar_dados_exemplo():
        try:
            with st.spinner('Carregando músicas de exemplo...'):
                # Lê o CSV local
                # 2. Constrói o caminho para o arquivo de forma robusta
                # __file__ é uma variável especial que contém o caminho do script atual (app.py)
                caminho_script = os.path.dirname(__file__)
                # os.path.join junta os pedaços do caminho com a barra correta para o sistema
                caminho_csv_exemplo = os.path.join(caminho_script, "assets", "sample_library.csv")
                df_exemplo = pd.read_csv(caminho_csv_exemplo) 
                # Processa com a mesma função de limpeza
                st.session_state.biblioteca_limpa = adaptar_csv_biblioteca(df_exemplo)
                # Reseta qualquer estado antigo
                st.session_state.df_set_gerado = None
                st.session_state.csv_para_download = ""
        except Exception as e:
            st.error(f"Erro ao carregar arquivo de exemplo: {e}")
            st.session_state.biblioteca_limpa = None

    st.sidebar.button(
        "🧪 Carregar músicas de Exemplo", 
        on_click=carregar_dados_exemplo, # Usa a abordagem de callback
        use_container_width=True,
        help="Teste o DJ Set Creator"
    )
    uploaded_file = st.file_uploader(
        label="Carregue aqui sua playlist em formato .csv", 
        type=["csv"]
    )    

    st.title("⚙️ Painel de Controles do Set")
    st.subheader("1. Use seu software DJ favorito para exportar suas músicas como .CSV")


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
        set_name = st.text_input("Nome do Set (opcional)", value="Meu Set Inteligente", max_chars=50, help="Este nome será usado no arquivo exportado.")
        lista_musicas = ["Automático"] + df_limpo['title'].tolist()
        musica_inicial = st.selectbox("Música de abertura", options=lista_musicas, placeholder="Escolha a música de abertura", help="Use a biblioteca para copiar a música desejada ou deixe em 'Automático'")
        tamanho_set = st.slider("Tamanho do Set (número de músicas)", min_value=5, max_value=100, value=20, step=1, width=340)
        curva_str = st.text_input("Curva de 'Vibe'", value="up-mid-down-up")
        
        st.header("3. Regras de Seleção")
        bpm_tolerancia = st.slider("Variação de BPM permitida", min_value=1, max_value=60, value=8, step=1, width=340)
        peso_bpm = st.slider("BPM Sync (prioriza BPMs iguais)", min_value=0.0, max_value=1.0, value=0.5, step=0.05, width=340)
        peso_key = 1.0 - peso_bpm
        st.slider("Mixagem Harmônica (prioriza KEYs iguais)", value=peso_key, disabled=True, width=340)

        # Botão de Ação para gerar o set
        if st.button("▶️ Criar DJ Set!", width="stretch"):
            with st.spinner(f'Criando DJ Set {set_name}'):
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
                    st.session_state.csv_para_download = exportar_set_csv(df_set_gerado)
                else:
                    st.session_state.csv_para_download = ""

        st.header("4. Exportar o Set")
        
        # O botão de download AGORA lê o estado que foi atualizado na mesma execução (se o botão 'Criar' foi clicado)
        st.download_button(
           label= f"📥 Baixar {set_name}",
           data=st.session_state.csv_para_download,
           file_name=f"{set_name}.csv",
           mime="text/csv",
           disabled=(st.session_state.df_set_gerado is None or st.session_state.df_set_gerado.empty),
           width="stretch",
           help="Crie um set para habilitar o download."
        )

    st.markdown("---")
    st.markdown("Desenvolvido com :brain: por :rainbow[Eliezer Queiroz]")
    footer_html = """
        <div>
            <p style="color: #888; font-size: 0.9em;">
                <a href="https://github.com/eliezerqueiroz/dj_set_creator" target="_blank">GitHub</a> | 
                <a href="https://www.linkedin.com/in/eliezerqueiroz/" target="_blank">LinkedIn</a>
            </p>
        </div>
        """
    st.markdown(footer_html, unsafe_allow_html=True)
# ==============================================================================
# SEÇÃO 3: ÁREA PRINCIPAL - Apenas exibe os resultados com base no estado
# ==============================================================================

# Lógica de Exibição: Mostra o conteúdo apropriado com base no que está no st.session_state
if st.session_state.df_set_gerado is not None and not st.session_state.df_set_gerado.empty:
    st.success(f"✅ DJ Set:  **{set_name}**  foi criado com sucesso!")
    
    st.subheader("📊 Visualização da Vibe")
    fig = plotar_curva_de_vibe(st.session_state.df_set_gerado)
    config = {
        'toImageButtonOptions': {
        'format': 'png', # one of png, svg, jpeg, webp
        'filename': set_name,
        }
    }
    fig.update_layout(title={'text': f'<b>Curva de Vibe: {set_name}</b>'})
    st.plotly_chart(fig, use_container_width=True, config=config)
    
    st.subheader(f"🎶 Set List: {set_name}")
    st.dataframe(st.session_state.df_set_gerado[['title', 'artist', 'bpm', 'key', 'vibe', 'transition_name', 'transition_effect', 'transition_icon', 'transition_score']])

elif st.session_state.biblioteca_limpa is not None:
    # Este é o estado DEPOIS do upload, mas ANTES de gerar o set
    st.subheader("Biblioteca carregada")
    st.dataframe(st.session_state.biblioteca_limpa[['title', 'artist', 'bpm', 'key']])
else:
# --- TELA 1: TELA DE APRESENTAÇÃO E TUTORIAL ---
    st.subheader("Bem-vindo ao DJ Set Creator!")
    st.write("Use a Ciência de dados para montar sets 100% harmonicos:")

    col1, col2= st.columns(2, border=True)

    with col1:
        st.markdown("<h4 style='text-align: center;'>1. Carregue suas músicas</h4>", unsafe_allow_html=True)
        st.image("assets/step1.gif", caption="1. Carregue suas músicas ou use os dados de exemplo")
        st.warning("Use seu software DJ favorito para exportar uma playlist como **.CSV**"
        "\n\nOu use o botão no topo da barra lateral para carregar os dados de exemplo.") 
        
    with col2:
        st.markdown("<h4 style='text-align: center;'>2. Configure e crie seu Set</h4>", unsafe_allow_html=True)
        st.image("assets/step2.gif", caption="2. use o painel lateral para configurar o set")
        st.info("Após configurar os parâmetros, clique em **'Criar DJ Set!'**. O algoritmo analisará milhares de combinações para encontrar uma sequência 100% harmônica que segue a sua curva de vibe.")
        st.success("Você verá um gráfico interativo da jornada de energia e a playlist detalhada.")
    col3, col4, col5 = st.columns([1,2,1])
    # col4_container = st.container( border=True, horizontal=True, horizontal_alignment="center")

    col4_container = col4.container(border=True)


    with col4_container:
        st.markdown("<h4 style='text-align: center;'>3. Analise a curva de <em>Vibe,</em> baixe e toque um set 100% harmônico</h4>", unsafe_allow_html=True)
        st.image("assets/step3.gif" , caption="3. A Vibe se baseia em BPM e Key e o peso dessas variáveis são ajustáveis no painel de controle")
        st.info("A 'Vibe' é uma métrica de 0 a 1 que calcula a energia de uma música combinando seu ritmo (BPM) e seu humor (Nota ou Key).")
        st.code("Exemplo: 'mid-up-up-down'", language="text")
        st.success("Isso cria um set que começa com energia média, sobe para um pico longo e depois relaxa no final.")
