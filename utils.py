import pandas as pd
import re
import plotly.graph_objects as go
from config import CONFIG_SALTOS


def adaptar_csv_biblioteca(df_original):
    """Adapta um DataFrame de biblioteca musical para o formato padrão do sistema.

    Esta função realiza as seguintes operações:
    1. Renomeia as colunas essenciais ('título', 'artista', 'bpm', 'nota').
    2. Seleciona apenas as colunas necessárias para o algoritmo.
    3. Extrai a notação Camelot da coluna de chave.
    4. Converte a coluna BPM para um tipo numérico inteiro.
    5. Remove linhas que contenham valores nulos nas colunas essenciais.

    Args:
        df_original (pd.DataFrame): O DataFrame bruto carregado do CSV.

    Returns:
        pd.DataFrame: O DataFrame limpo e formatado, pronto para ser usado.
    """
    # 1. LIMPEZA DOS NOMES DAS COLUNAS
    # Remove caracteres invisíveis (como o BOM), espaços em branco
    # e converte para minúsculas para uma correspondência mais flexível.
    df = df_original.copy()
    df.columns = df.columns.str.lower().str.strip().str.replace('\ufeff', '', regex=False)

    # 2. MAPEAMENTO FLEXÍVEL
    # Agora o mapeamento usa nomes em minúsculas
    mapeamento_colunas = {
        'título': 'title', # "Título" se torna "título"
        'artista': 'artist',
        'bpm': 'bpm',
        'nota': 'key'
    }
    df.rename(columns=mapeamento_colunas, inplace=True)
    # --- FIM DA CORREÇÃO ---

    # 3. Seleção de colunas (lógica inalterada, mas agora funciona)
    colunas_desejadas = ['title', 'artist', 'bpm', 'key']
    colunas_para_manter = [col for col in colunas_desejadas if col in df.columns]
    
    # Validação importante: Se colunas essenciais não foram encontradas APÓS a limpeza.
    if 'title' not in colunas_para_manter or 'artist' not in colunas_para_manter:
        raise KeyError("Não foi possível encontrar as colunas 'Título' ou 'Artista' no seu CSV. Por favor, verifique o arquivo.")
        
    df = df[colunas_para_manter]
    print(f"Colunas selecionadas: {colunas_para_manter}")
    # 3. Limpeza e Formatação de Dados
    # Usamos a função `extrair_chave_camelot` para transformar a coluna 'key'.
    if 'key' in df.columns:
        print("Formatando a coluna 'key' usando a função 'extrair_chave_camelot'...")
        df['key'] = df['key'].str.upper().str.extract(r'(\d{1,2}[AB])')
    # Converter BPM para numérico
    if 'bpm' in df.columns:
        print("Convertendo a coluna 'bpm' para tipo numérico e formatando...")
        df['bpm'] = pd.to_numeric(df['bpm'], errors='coerce')
        # Formatar a coluna 'bpm' com duas casas decimais
        df['bpm'] = df['bpm'].round(0)
    # 4. Validação Final: Remover linhas com dados essenciais faltando
    colunas_obrigatorias = ['title', 'artist', 'bpm', 'key']
    linhas_antes = len(df)
    df.dropna(subset=colunas_obrigatorias, inplace=True)
    linhas_depois = len(df)
    print(f"Validação final: Removidas {linhas_antes - linhas_depois} linhas com dados essenciais inválidos.")
    print("--- ADAPTAÇÃO CONCLUÍDA ---")
    return df

def calculate_bpm_score(bpm1, bpm2, bpm_tolerancia=5):
    """Calcula um score de compatibilidade de BPM de 0.0 a 1.0.

    O score é 1.0 para BPMs idênticos e decai linearmente até 0.0 no limite
    da tolerância.

    Args:
        bpm1 (float): O BPM da primeira música.
        bpm2 (float): O BPM da segunda música.
        bpm_tolerancia (int): A diferença máxima de BPM permitida.

    Returns:
        float: O score de compatibilidade de BPM entre 0.0 e 1.0.
    """
    # Se algum dos BPMs for inválido, a compatibilidade é zero.
    if pd.isna(bpm1) or pd.isna(bpm2):
      return 0.0
    # Se algum dos BPMs for inválido, a compatibilidade é zero.
    diff = abs(bpm1 - bpm2)
    # Se a diferença for maior que a tolerância, a transição é considerada impossível. Score zero.
    if diff > bpm_tolerancia:
        return 0.0
    # A fórmula de decaimento linear:
    # Se a diferença (diff) é 0, o score é 1.0 (perfeito).
    # Se a diferença é igual à tolerância, o score é 0.0.
    score = 1.0 - (diff / bpm_tolerancia)
    return score

def parse_key(key_str):
    """Analisa uma string de chave Camelot e a decompõe em número e letra.

    Args:
        key_str (str): A string da chave a ser analisada (ex: "8A", "12B").

    Returns:
        tuple[int, str] or tuple[None, None]: Uma tupla contendo o número e a letra,
                                              ou (None, None) se a chave for inválida.
    """
    if not isinstance(key_str, str) or len(key_str) < 2: return None, None
    try:
      numero = int(key_str[:-1])
      letra = key_str[-1].upper()
      if not (1 <= numero <= 12 and letra in ['A', 'B']): return None, None
      return numero, letra
    except (ValueError, TypeError):
      return None, None

def calculate_key_score_programmatic(jump, flip):
  """Calcula o score de uma transição de chave (0.0 a 1.0) baseado em regras.

    Args:
        jump (int): O salto numérico (0 a 11) na Roda de Camelot.
        flip (bool): True se houve mudança de modo (Maior <-> Menor).

    Returns:
        float: O score de compatibilidade harmônica.
    """
  distancia_salto = min(jump, 12-jump)
  penalidade_salto = (distancia_salto ** 1.5) * 0.05

  if flip:
    penalidade_flip = 0.05 if jump != 0 else 0.02
  else:
    penalidade_flip = 0.0

  score_final = 1.0 - (penalidade_salto + penalidade_flip)
  return max(0, score_final)

def analisar_transicao_com_vibe(key1, key2):
    """Analisa a transição entre duas chaves, gera um nome e calcula o score.

    Args:
        key1 (str): A chave da música de origem.
        key2 (str): A chave da música de destino.

    Returns:
        dict: Um dicionário contendo a análise completa da transição, incluindo
              'nome_funcao', 'score_key', 'icon', e 'efeito_base'.
    """
    num1, letra1 = parse_key(key1)
    num2, letra2 = parse_key(key2)

    # Tratamento de erro inicial
    if num1 is None or num2 is None:
        return {'compativel': False, 'nome_funcao': 'Chave Inválida', 'score_key': 0.0, 'icon': '⚠️'}

    jump = (num2 - num1 + 12) % 12
    flip = (letra1 != letra2)
    base_info = CONFIG_SALTOS.get(jump, {"icon": "?", "efeito": "Desconhecido"})
    # Lógica de nomenclatura "Vibe"
    prefixo = "Creative " if flip and jump != 0 else ""
    icone = base_info['icon'] # Começa com o ícone padrão do salto
    # Se houve flip, a transição é "criativa" e o ícone deve refletir isso.
    if flip:
        icone = '🎨' # Novo ícone para qualquer transição com flip
    # Lógica de nomenclatura (agora mais simples)
    nome_funcao = ""
    if jump == 0:
        nome_funcao = "Perfect Vibe" if not flip else "Vibe Change"
        if flip:
             icone = '🎭' # Ícone especial para Vibe Change, que é uma troca de humor
    elif jump <= 6:
        nome_funcao = f"{prefixo}Vibe+{jump}"
    else:
        salto_negativo = jump - 12
        nome_funcao = f"{prefixo}Vibe{salto_negativo}"
    score_da_chave = calculate_key_score_programmatic(jump, flip)
    return {
        'compativel': True,
        'nome_funcao': nome_funcao,
        'score_key': score_da_chave,
        'icon': icone, # Usa a variável 'icone' que foi condicionalmente atualizada
        'efeito_base': base_info['efeito']
    }

def calcular_vibe(df, pesos={'bpm': 0.7, 'key': 0.3}): 
  """Calcula uma métrica de 'vibe' (energia) para cada música no DataFrame.

    A vibe é uma média ponderada da energia rítmica (BPM normalizado) e da
    energia harmônica (fator da chave Maior/Menor).

    Args:
        df (pd.DataFrame): O DataFrame de músicas limpo.
        pesos (dict): Um dicionário com os pesos para 'bpm' and 'key'.
                      A soma dos pesos deve ser 1.0.

    Returns:
        pd.DataFrame: O DataFrame original com uma nova coluna 'vibe'.
    """
  print(f"Calculando 'vibe' com os pesos: {pesos}")
  df_temp = df.copy()
  # Etapa 1: Normalizar BPM
  min_bpm = df_temp['bpm'].min()
  max_bpm = df_temp['bpm'].max()
  df_temp['bpm_norm'] = (df_temp['bpm'] - min_bpm) / (max_bpm - min_bpm)
  # Etapa 2: Fator de Chave
  df_temp['key_factor'] = df_temp['key'].apply(lambda k: 1.0 if 'B' in k else 0.85)
  # Etapa 3: Cálculo Ponderado da Vibe (agora usa os pesos recebidos)
  df_temp['vibe'] = (pesos['bpm'] * df_temp['bpm_norm']) + (pesos['key'] * df_temp['key_factor'])
  # Etapa 4: Limpeza
  df_final = df_temp.drop(columns=['bpm_norm', 'key_factor'])
  return df_final


def get_target_vibe_range(segment_name):
    """Retorna a tupla (min_vibe, max_vibe) para um segmento."""
    return VIBE_SEGMENTS.get(segment_name, (0.0, 1.0)) # Retorna tudo se o nome for inválido

def calculate_energy_curve_bonus(vibe_candidata, segmento_alvo):
    """
    Calcula um bônus (ou penalidade) para uma música candidata com base em
    quão bem sua 'vibe' se encaixa no segmento alvo do set.
    """
    min_vibe, max_vibe = get_target_vibe_range(segmento_alvo)
    # Regra de Negócio:
    # - Se a música está DENTRO da faixa alvo, ela recebe um bônus significativo.
    # - Se está um pouco fora, recebe um bônus menor (ou penalidade pequena).
    # - Se está muito fora, recebe uma penalidade grande para ser evitada.
    if min_vibe <= vibe_candidata <= max_vibe:
        return 0.20  # Bônus máximo por estar na faixa perfeita!
    # Lógica de "proximidade": quão longe está da faixa?
    distancia_do_alvo = 0
    if vibe_candidata < min_vibe:
        distancia_do_alvo = min_vibe - vibe_candidata
    elif vibe_candidata > max_vibe:
        distancia_do_alvo = vibe_candidata - max_vibe
    # A penalidade aumenta com a distância.
    # Uma música a 0.1 de distância é penalizada em -0.1. A 0.3 de distância, em -0.3.
    penalidade = distancia_do_alvo * -1.0
    # Retorna o bônus (que pode ser negativo, ou seja, uma penalidade)
    # Limitamos para que a penalidade máxima não seja tão destrutiva.
    return max(-0.5, penalidade)

def calculate_final_score(musica_anterior, candidata, pesos={'bpm': 0.7, 'key': 0.3}, bpm_tolerancia=5):
  """Calcula o score final ponderado de uma transição combinando BPM e Chave.

    Args:
        musica_anterior (dict): Dicionário da música de origem.
        candidata (dict): Dicionário da música de destino.
        pesos (dict): Dicionário com pesos para 'bpm' e 'key'.
        bpm_tolerancia (int): Tolerância de BPM a ser usada no cálculo.

    Returns:
        dict: Dicionário contendo a música candidata, seu 'score_final' e
              a análise completa da transição.
    """
  score_bpm = calculate_bpm_score(musica_anterior['bpm'], candidata['bpm'], bpm_tolerancia)
  analise_key = analisar_transicao_com_vibe(musica_anterior['key'], candidata['key'])
  score_key = analise_key['score_key']
  # Calcula a média ponderada para obter o score final
  score_final = (pesos['bpm'] * score_bpm) + (pesos['key'] * score_key)
  #Retorna um objeto completo com a música, seu score e a análise da transição
  return {
      'musica': candidata,
      'score_final': score_final,
      'analise_transicao': analise_key
  }

def criar_dj_set(biblioteca, tamanho_set, curva_energia_str, musica_inicial_nome=None, bpm_tolerancia=8, pesos={'bpm': 0.6, 'key': 0.4}):
  """Gera um DJ set estratégico que tenta seguir uma curva de energia (vibe).

    Esta versão do algoritmo funciona como um "diretor de cena". Ela divide o set
    em segmentos baseados na `curva_energia_str` e, para cada música a ser escolhida,
    aplica um bônus ou penalidade às candidatas com base em quão bem a 'vibe' delas
    se alinha com a 'vibe' alvo do segmento atual. A seleção final ainda é
    baseada no maior score combinado (BPM, Chave e Bônus de Curva).

    Args:
        biblioteca (pd.DataFrame): O DataFrame completo e limpo de músicas.
        tamanho_set (int): O número de músicas desejado no set final.
        curva_energia_str (str): A string que define a jornada de vibe, separada
                                 por hífens (ex: "mid-up-up-down").
        musica_inicial_nome (str, optional): Título da música para forçar o início
                                             do set. Se None, o algoritmo escolhe
                                             a melhor para o primeiro segmento.
                                             Defaults to None.
        bpm_tolerancia (int, optional): A tolerância máxima de BPM para uma transição
                                        ser considerada. Defaults to 8.
        pesos (dict, optional): Dicionário com os pesos para 'bpm' e 'key' no
                                cálculo do score. Defaults to {'bpm': 0.6, 'key': 0.4}.

    Returns:
        pd.DataFrame: Um DataFrame contendo o set gerado, com colunas detalhadas
                      de análise para cada transição. Retorna um DataFrame vazio
                      se a geração falhar.
    """
  print("="*50)
  print(f"INICIANDO GERAÇÃO DE SET V4 - CURVA: {curva_energia_str}")
  print("="*50)

  # 1. PREPARAÇÃO
  biblioteca_com_vibe = calcular_vibe_v2(biblioteca, pesos=pesos)
  setlist = []
  musicas_disponiveis = biblioteca_com_vibe.copy().set_index('title', drop=False)
  curva_energia_lista = curva_energia_str.split('-')
  # Previne divisão por zero se a curva for vazia
  if not curva_energia_lista or not curva_energia_lista[0]:
      print("Erro: String de curva de energia inválida.")
      return pd.DataFrame()
  tamanho_segmento = tamanho_set // len(curva_energia_lista)
  # 2. SELEÇÃO DA PRIMEIRA MÚSICA
  if musica_inicial_nome and musica_inicial_nome in musicas_disponiveis.index:
      musica_atual_row = musicas_disponiveis.loc[musica_inicial_nome]
  else:
      primeiro_segmento = curva_energia_lista[0]
      min_vibe, max_vibe = get_target_vibe_range(primeiro_segmento)
      candidatas_iniciais = musicas_disponiveis[musicas_disponiveis['vibe'].between(min_vibe, max_vibe)]
      if candidatas_iniciais.empty:
          print(f"Aviso: Nenhuma música encontrada na faixa de vibe inicial '{primeiro_segmento}'. Iniciando com a de menor vibe geral.")
          musica_atual_row = musicas_disponiveis.sort_values(by='vibe').iloc[0]
      else:
          musica_atual_row = candidatas_iniciais.sort_values(by='vibe').iloc[0]
  musica_atual_dict = musica_atual_row.to_dict()
  # Adicionando todas as colunas de transição para a primeira música
  musica_atual_dict['transition_name'] = 'Abertura'
  musica_atual_dict['transition_effect'] = 'Início do Set'
  musica_atual_dict['transition_icon'] = '🎉'
  musica_atual_dict['transition_score'] = 1.0
  setlist.append(musica_atual_dict)
  musicas_disponiveis = musicas_disponiveis.drop(musica_atual_row.name)
  # 3. LOOP PRINCIPAL DE GERAÇÃO
  while len(setlist) < tamanho_set and not musicas_disponiveis.empty:
      musica_anterior = setlist[-1]
      posicao_atual = len(setlist)
      indice_segmento = min(posicao_atual // tamanho_segmento, len(curva_energia_lista) - 1)
      segmento_alvo = curva_energia_lista[indice_segmento]
      candidatas_avaliadas = []
      for _, candidata_row in musicas_disponiveis.iterrows():
          if abs(musica_anterior['bpm'] - candidata_row['bpm']) <= bpm_tolerancia:
              info_candidata = calculate_final_score(musica_anterior, candidata_row.to_dict(), pesos, bpm_tolerancia)
              bonus = calculate_energy_curve_bonus(info_candidata['musica']['vibe'], segmento_alvo)
              info_candidata['score_final'] += bonus
              candidatas_avaliadas.append(info_candidata)

      if not candidatas_avaliadas:
          print(f"Não encontrei nenhuma música compatível para continuar o set após '{musica_anterior['title']}'. Parando.")
          break

      melhor_candidata_info = max(candidatas_avaliadas, key=lambda x: x['score_final'])
      proxima_musica_dict = melhor_candidata_info['musica']
      analise = melhor_candidata_info['analise_transicao']
      proxima_musica_dict['transition_name'] = analise['nome_funcao']
      proxima_musica_dict['transition_effect'] = analise['efeito_base']
      proxima_musica_dict['transition_icon'] = analise['icon']  
      proxima_musica_dict['transition_score'] = melhor_candidata_info['score_final'] 
      setlist.append(proxima_musica_dict)
      musicas_disponiveis = musicas_disponiveis.drop(proxima_musica_dict['title'])
  # Colunas finais do DataFrame do set
  colunas_finais = ['title', 'artist', 'bpm', 'key', 'vibe', 'transition_name', 'transition_effect', 'transition_icon', 'transition_score']
  df_set = pd.DataFrame(setlist)
  # Garantir que as colunas existam para evitar erros
  for col in colunas_finais:
      if col not in df_set.columns:
          df_set[col] = None

  return df_set[colunas_finais]


def plotar_curva_de_vibe(df_set):
    """Gera um gráfico interativo da curva de vibe de um set.

    Args:
        df_set (pd.DataFrame): O DataFrame do set gerado.

    Returns:
        plotly.graph_objects.Figure: O objeto da figura do Plotly, pronto para ser renderizado.
    """
    # Validação: Garante que o DataFrame não está vazio e tem a coluna 'vibe'
    if df_set.empty or 'vibe' not in df_set.columns:
        print("DataFrame do set está vazio ou não contém a coluna 'vibe'. Gráfico não pode ser gerado.")
        return
    # 1. Prepara os dados para o gráfico
    # O eixo X será a posição da música (1, 2, 3...)
    posicao_no_set = list(range(1, len(df_set) + 1))
    # O eixo Y será a nossa métrica de 'vibe'
    vibe_scores = df_set['vibe']
    # Criamos um texto customizado para o 'hover' (quando o usuário passa o mouse)
    # Isso enriquece muito a visualização!
    hover_text = [
        f"<b>{row['title']}</b><br>" +
        f"Artista: {row['artist']}<br>" +
        f"BPM: {row['bpm']:.0f} | Chave: {row['key']}<br>" +
        f"Vibe: {row['vibe']:.2f}<br>" +
        f"Transição: {row['transition_name']} ({row['transition_icon']})"
        for index, row in df_set.iterrows()
    ]
    # 2. Cria o objeto do gráfico
    fig = go.Figure()
    # 3. Adiciona a linha (o "traço") da curva de vibe
    fig.add_trace(go.Scatter(
        x=posicao_no_set,
        y=vibe_scores,
        mode='lines+markers',  # Linhas conectando os pontos (marcadores)
        name='Vibe do Set',
        text=hover_text,       # Associa nosso texto customizado
        hoverinfo='text',      # Diz ao Plotly para mostrar APENAS nosso texto
        line=dict(color='royalblue', width=3, shape='spline'), # Linha suave e azul
        marker=dict(size=10, color='mediumslateblue')
    ))
    # 4. Configura o layout (títulos, eixos, etc.)
    fig.update_layout(
        title={
            'text': '<b>Curva de Vibe do Set Gerado</b>',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20}
        },
        xaxis_title='Posição da Música no Set',
        yaxis_title='Nível de Vibe (0.0 a 1.0)',
        xaxis=dict(tickmode='linear', dtick=1), # Força o eixo X a mostrar todos os números (1, 2, 3...)
        yaxis=dict(range=[0, 1]), # Fixa o eixo Y entre 0 e 1 para consistência
        template='plotly_white', # Fundo branco e limpo
        height=500
    )
    # 5. Mostra o gráfico!
    return fig

