# 🎧 DJ Set Creator: Ciência de Dados na Pista de Dança

[![Python Version](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://djsetcreator.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Esta aplicação transforma a arte da mixagem em uma ciência precisa, sem perder a alma. O **DJ Set Creator** é uma ferramenta de curadoria musical inteligente que eu construí para resolver um desafio que todo DJ conhece: o bloqueio criativo e as horas gastas para encontrar a sequência perfeita de músicas.

Este não é apenas um script; é um produto de dados interativo. **[✨ Experimente a aplicação ao vivo! ✨](https://djsetcreator.streamlit.app/)**

> Como Engenheiro de Dados e DJ, eu vivia entre dois mundos: a lógica dos algoritmos e a energia da música. Decidi uni-los para transformar um processo manual e demorado em um parceiro criativo inteligente. O resultado é esta ferramenta, que usa dados para sugerir jornadas musicais coesas, permitindo que o artista foque no que realmente importa: a performance.

![Demonstração do DJ Set Creator](https://github.com/eliezerqueiroz/dj_set_creator/blob/main/assets/step2.gif?raw=true)

---

## ✨ Core Features

*   **🎼 Análise Inteligente de Biblioteca:** Faça o upload de um `.csv` da sua biblioteca musical (compatível com Mixxx, Rekordbox, etc.) e a aplicação extrai e limpa automaticamente os metadados essenciais: BPM, tonalidade (chave Camelot), artista e título.

*   **📈 Design de Jornada com a "Vibe Curve":** O coração da ferramenta. A métrica de "Vibe" (0.0 a 1.0) que desenvolvi traduz ritmo e harmonia em um score de energia. Você pode ditar a narrativa do seu set com comandos simples como `down-up-up` (aquecimento, pico, pico) ou `up-down-mid` (abertura forte, um respiro, e finalização controlada).

*   **🎛️ Você no Controle do Algoritmo:** Ajuste os pesos do sistema de recomendação para priorizar o que é mais importante para o seu estilo de mixagem:
    *   **BPM Sync:** Foco em transições rítmicas perfeitas.
    *   **Mixagem Harmônica:** Foco em transições musicalmente impecáveis.

*   **🚀 Visualização e Exportação Prontas para o Palco:** Gere seu set e obtenha insights imediatos com um gráfico interativo da Curva de Vibe. Com um clique, baixe um `.csv` pronto para ser importado de volta no seu software de DJ, com a coluna de comentários já preenchida com as sugestões de transição!

![Demonstração do DJ Set Creator](https://github.com/eliezerqueiroz/dj_set_creator/blob/main/assets/step3.gif)

---

## 🎯 Por que Este Projeto Importa (Para Líderes Técnicos e Recrutadores)

Este projeto foi desenhado para ser um case completo, demonstrando competência em todo o ciclo de vida de um produto de dados:

*   **Pensamento de Produto (End-to-End):** Fui da identificação de uma dor de usuário real à entrega de uma solução web funcional e com valor tangível.
*   **Engenharia de Dados (ETL):** Implementei um pipeline em Python/Pandas para ingestão, limpeza, transformação e estruturação de dados brutos.
*   **Ciência de Dados Aplicada:** Criei features (`Vibe score`), desenvolvi um algoritmo de recomendação ponderado e modelei um sistema que traduz um objetivo estratégico (`Curva de Vibe`) em resultados táticos (a playlist final).
*   **BI & Visualização de Dados:** Utilizei Plotly para criar uma visualização de dados interativa que não apenas mostra dados, mas gera insights acionáveis para o usuário.
*   **Desenvolvimento e Deploy:** Empacotei a lógica complexa em uma aplicação user-friendly com Streamlit e realizei o deploy na nuvem, tornando-a acessível a todos.

---

## 🛠️ Tech Stack

| Área                  | Tecnologias                                    |
| --------------------- | ---------------------------------------------- |
| **Backend & Análise** | `Python`, `Pandas`, `NumPy`                    |
| **Interface Web**     | `Streamlit`                                    |
| **Visualização**      | `Plotly`                                       |
| **Versionamento & CI/CD** | `Git`, `GitHub` |

---

## 🛣️ Roadmap: O Futuro é Colaborativo e Inteligente

Este projeto é uma fundação. A visão é expandi-lo para se tornar um verdadeiro "copiloto" para DJs.

-   **[  ] Modo "Copiloto" Interativo:** Uma interface onde o DJ constrói o set música por música, recebendo um ranking das melhores próximas faixas em tempo real e visualizando o impacto de cada escolha na Curva de Vibe.
-   **[  ] Exportação Multi-Plataforma:** Adicionar suporte nativo para formatos de playlist do **Rekordbox**, **Traktor** e **Serato** (`.xml`, `.m3u8`).

---

## 👨‍💻 Vamos nos Conectar!

Olá, sou **Eliezer Queiroz**, um Engenheiro de Dados apaixonado por construir soluções que vivem na intersecção entre a tecnologia e a criatividade.

Se você se interessou por este projeto, tem feedback, ou quer discutir oportunidades, adoraria conversar.

*   🔗 **Encontre-me no [LinkedIn](https://www.linkedin.com/in/eliezerqueiroz/)**
*   ⭐ **Explore meus outros projetos no [GitHub](https://github.com/eliezerqueiroz)**
