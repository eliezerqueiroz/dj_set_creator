

# 🎧 DJ Set Creator Inteligente

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://djsetcreator.streamlit.app)

Como Engenheiro de Dados e DJ, sempre me deparei com um desafio: o processo de descobrir e testar combinações de músicas para um novo set era demorado e manual. Eu queria uma forma mais eficiente de explorar minha biblioteca, unindo a precisão da ciência de dados com a arte da mixagem. Foi assim que nasceu o **DJ Set Creator**.

Esta aplicação é a minha solução: uma ferramenta que analisa uma biblioteca musical a partir de um arquivo CSV e utiliza um algoritmo inteligente para sugerir sets coesos, com transições harmônicas perfeitas e uma jornada de energia planejada.

### ✨ **[Teste a Aplicação Ao Vivo!](https://djsetcreator.streamlit.app)** ✨

![GIF de Demonstração do DJ Set Creator](https://github.com/eliezerqueiroz/dj_set_creator/blob/main/demo.gif?raw=true)
*(Instrução para você: Grave um GIF curto da aplicação, adicione-o à raiz do seu repositório com o nome `demo.gif` e esta linha irá exibi-lo.)*

---

## 🎯 A Visão de um Profissional de Dados

Este projeto foi construído para demonstrar um ciclo completo de desenvolvimento de um produto de dados, da concepção à entrega. Ele evidencia competências essenciais na área de dados:

*   **Engenharia de Dados (ETL):** Construção de um pipeline robusto em Python que ingere dados brutos (CSV), os transforma (limpando nomes de colunas, extraindo chaves Camelot, normalizando BPMs) e os estrutura para análise.
*   **Engenharia de Features:** A criação da métrica de **"Vibe"**, uma abstração que traduz conceitos musicais (ritmo e harmonia) em um score numérico (0.0 a 1.0), servindo como a fundação para o algoritmo.
*   **Design de Algoritmos:** Desenvolvimento de um algoritmo de recomendação que não apenas busca compatibilidade local, mas segue uma estratégia global (a "Curva de Vibe") para construir uma jornada musical coesa.
*   **Visualização de Dados Interativa:** Uso de Plotly para transformar a saída do algoritmo em insights visuais e acionáveis, permitindo que o usuário "veja" a energia do seu set.
*   **Desenvolvimento de Aplicação Web:** Empacotamento de toda a lógica de dados em uma aplicação interativa e amigável, utilizando Streamlit para uma prototipagem e entrega ágil.

---

## 🚀 Como Criar seu Set com o DJ Set Creator

### 1. 🆙 Faça o Upload da sua Biblioteca
Na barra lateral, carregue sua biblioteca de músicas em formato `.csv`. O sistema é compatível com exportações de softwares de DJ populares como o **Mixxx**.

### 2. ⚙️ Configure sua Jornada Musical
No "Painel de Controles", você define a "alma" do seu set:

*   #### **A Curva de 'Vibe'**
    A "Vibe" é uma métrica que criei para quantificar a energia de uma música, combinando seu ritmo (BPM) e seu humor harmônico (tonalidade Maior/Menor). No campo **Curva de 'Vibe'**, você pode desenhar a jornada de energia do seu set. Por exemplo:
    *   `mid-up-up`: Começa com energia média e constrói para um pico longo.
    *   `up-down-up`: Um set com um momento de respiro no meio.

### 3. 🎛️ Ajuste as Regras de Seleção
Tenha controle fino sobre como o algoritmo pensa:

*   **Ajuste de Pesos (BPM vs. Chave):** O coração do algoritmo! Use o slider para dizer ao sistema o que é mais importante para você:
    *   **Foco em Ritmo (BPM Sync):** Prioriza transições com BPMs quase idênticos, ideal para mixagens suaves e longas.
    *   **Foco em Harmonia (Mixagem Harmônica):** Prioriza a compatibilidade de chave (Camelot Wheel), criando transições musicalmente perfeitas.

### 4. ▶️ Gere, Analise e Exporte!
Clique em **"▶️ Criar DJ Set!"**. A aplicação irá exibir:

*   #### **Análise Visual e Exportação**
    *   **Gráfico da Curva de Vibe:** Visualize a jornada de energia do set. **Você pode baixar uma imagem PNG do gráfico** usando o ícone de câmera na barra de ferramentas do gráfico.
    *   **Download do Set (CSV):** Na barra lateral, o botão de download estará habilitado. Ele gera um `.csv` formatado para ser **importado diretamente no Mixxx**. A coluna **"Comentário"** no Mixxx virá preenchida com o efeito de transição que o algoritmo planejou para cada música!

**Importante:** Lembre-se, o DJ Set Creator é uma **ferramenta de sugestão para potencializar sua criatividade**. O resultado final sempre dependerá das suas decisões como artista. Use as sugestões como um ponto de partida para explorar novas combinações e aperfeiçoar sua arte.

---

## 🛠️ Tecnologias Utilizadas

*   **Backend & Análise de Dados:** Python, Pandas, NumPy
*   **Interface Web:** Streamlit
*   **Visualização de Dados:** Plotly
*   **Versionamento:** Git & GitHub

---

## 🛣️ Roadmap: O Futuro do Projeto

Este projeto é uma plataforma para inovação contínua. As próximas metas estão focadas em dar ainda mais controle criativo ao DJ e em usar IA para ir além da seleção de músicas, sugerindo técnicas de mixagem.

*   **Meta 1: O "Solucionador de Transições" Interativo**
    *   **Feature:** Uma nova interface de "construção manual", onde o DJ seleciona a primeira música e, a cada passo, o sistema apresenta um ranking das melhores próximas faixas. O DJ pode então escolher a próxima música, ver o impacto na curva de vibe em tempo real, e continuar construindo o set, música por música.
    *   **Valor para o DJ:** Combina a inteligência do algoritmo com o controle total do artista. Permite a criação de sets mais personalizados e a exploração de diferentes caminhos de energia de forma interativa.

*   **Meta 2: Exportação Multi-Plataforma**
    *   **Feature:** Expandir a funcionalidade de exportação para garantir compatibilidade total com os principais softwares de DJ do mercado.
    *   **Implementação:** Adicionar suporte para os formatos de playlist `.xml` (usado pelo **Rekordbox** e **Traktor**) e `.m3u8` (um padrão universal compatível com o **Serato** e outros).
    *   **Valor para o DJ:** Torna a ferramenta universalmente útil, independentemente do equipamento ou software que o DJ utiliza.

## 👨‍💻 Sobre o Autor

Olá! Sou **Eliezer Queiroz**, um Engenheiro de Dados com uma profunda paixão por música e discotecagem. Este projeto é a intersecção dos meus dois mundos, criado para resolver um desafio que eu mesmo enfrentava.

Estou sempre aberto a novas conexões, feedback e oportunidades.

*   **[LinkedIn](https://www.linkedin.com/in/eliezerqueiroz/)**
*   **[GitHub](https://github.com/eliezerqueiroz)**
