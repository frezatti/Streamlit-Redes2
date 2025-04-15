import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import re

st.title("Análise de Texto com Processamento em Tempo Real")

# Função para processar o texto
def processar_texto(texto):
    if not texto.strip():
        return None, None, None, None
    
    # Contar caracteres
    num_caracteres = len(texto)
    
    # Contar palavras
    palavras = re.findall(r'\b\w+\b', texto.lower())
    num_palavras = len(palavras)
    
    # Encontrar palavras mais frequentes
    contador = Counter(palavras)
    palavras_frequentes = contador.most_common(10)
    
    # Remover stopwords em português para melhorar a nuvem de palavras
    stopwords = set(['de', 'a', 'o', 'que', 'e', 'do', 'da', 'em', 'um', 'para', 'é', 'com',
                    'não', 'uma', 'os', 'no', 'se', 'na', 'por', 'mais', 'as', 'dos', 'como',
                    'mas', 'foi', 'ao', 'ele', 'das', 'tem', 'à', 'seu', 'sua', 'ou', 'ser',
                    'quando', 'muito', 'há', 'nos', 'já', 'está', 'eu', 'também', 'só', 'pelo',
                    'pela', 'até', 'isso', 'ela', 'entre', 'era', 'depois', 'sem', 'mesmo',
                    'aos', 'ter', 'seus', 'quem', 'nas', 'me', 'esse', 'eles', 'estão', 'você',
                    'essa', 'num', 'nem', 'suas', 'meu', 'às', 'minha', 'têm', 'numa', 'pelos',
                    'elas', 'havia', 'seja', 'qual', 'será', 'nós', 'tenho', 'lhe', 'deles',
                    'essas', 'esses', 'pelas', 'este', 'fosse', 'dele', 'tu', 'te', 'vocês',
                    'vos', 'lhes', 'meus', 'minhas', 'teu', 'tua', 'teus', 'tuas', 'nosso',
                    'nossa', 'nossos', 'nossas', 'dela', 'delas', 'esta', 'estes', 'estas',
                    'aquele', 'aquela', 'aqueles', 'aquelas', 'isto', 'aquilo', 'estou',
                    'está', 'estamos', 'estão', 'estive', 'esteve', 'estivemos', 'estiveram'])
    
    palavras_filtradas = [p for p in palavras if p not in stopwords and len(p) > 2]
    contador_filtrado = Counter(palavras_filtradas)
    
    # Gerar nuvem de palavras
    if palavras_filtradas:
        wordcloud = WordCloud(
            width=800, 
            height=400, 
            background_color='white',
            colormap='viridis',
            max_words=100
        ).generate(' '.join(palavras_filtradas))
    else:
        wordcloud = None
    
    return num_caracteres, num_palavras, palavras_frequentes, wordcloud

# Interface do usuário
texto = st.text_area(
    "Digite ou cole seu texto aqui:",
    height=200,
    placeholder="Digite ou cole seu texto para análise..."
)

# Processar o texto em tempo real
caracteres, palavras, palavras_freq, nuvem = processar_texto(texto)

if caracteres is not None:
    # Exibir estatísticas básicas
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total de Caracteres", caracteres)
    with col2:
        st.metric("Total de Palavras", palavras)
    
    # Exibir palavras mais frequentes
    st.subheader("Palavras mais frequentes")
    if palavras_freq:
        # Criar dataframe para exibição
        df_palavras = pd.DataFrame(palavras_freq, columns=['Palavra', 'Frequência'])
        
        # Exibir gráfico e tabela
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Criar gráfico de barras
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.barh(
                [p[0] for p in palavras_freq[:5]], 
                [p[1] for p in palavras_freq[:5]],
                color='skyblue'
            )
            ax.set_xlabel('Frequência')
            ax.set_title('5 Palavras Mais Frequentes')
            plt.tight_layout()
            st.pyplot(fig)
            
        with col2:
            st.dataframe(df_palavras, hide_index=True)
    else:
        st.info("Nenhuma palavra encontrada para análise.")
    
    # Exibir nuvem de palavras
    st.subheader("Nuvem de Palavras")
    if nuvem is not None:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(nuvem, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)
    else:
        st.info("Texto insuficiente para gerar uma nuvem de palavras.")
else:
    st.info("Digite algum texto para iniciar a análise.")
