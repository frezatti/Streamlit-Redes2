import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title("Sistema de Recomendação de Filmes")

# Base de dados de filmes
@st.cache_data
def carregar_filmes():
    filmes = {
        "Ação": [
            {"titulo": "Vingadores: Ultimato", "pontuacao_base": 92, "ano": 2019},
            {"titulo": "Duro de Matar", "pontuacao_base": 88, "ano": 1988},
            {"titulo": "Mad Max: Estrada da Fúria", "pontuacao_base": 91, "ano": 2015},
            {"titulo": "John Wick", "pontuacao_base": 86, "ano": 2014},
            {"titulo": "Velozes e Furiosos 7", "pontuacao_base": 82, "ano": 2015}
        ],
        "Comédia": [
            {"titulo": "Superbad", "pontuacao_base": 85, "ano": 2007},
            {"titulo": "O Grande Lebowski", "pontuacao_base": 90, "ano": 1998},
            {"titulo": "Debi & Lóide", "pontuacao_base": 86, "ano": 1994},
            {"titulo": "Borat", "pontuacao_base": 84, "ano": 2006},
            {"titulo": "Deadpool", "pontuacao_base": 87, "ano": 2016}
        ],
        "Drama": [
            {"titulo": "O Poderoso Chefão", "pontuacao_base": 95, "ano": 1972},
            {"titulo": "Um Sonho de Liberdade", "pontuacao_base": 94, "ano": 1994},
            {"titulo": "Cidade de Deus", "pontuacao_base": 91, "ano": 2002},
            {"titulo": "Interestelar", "pontuacao_base": 89, "ano": 2014},
            {"titulo": "Clube da Luta", "pontuacao_base": 92, "ano": 1999}
        ],
        "Ficção Científica": [
            {"titulo": "Blade Runner 2049", "pontuacao_base": 90, "ano": 2017},
            {"titulo": "Matriz", "pontuacao_base": 93, "ano": 1999},
            {"titulo": "Duna", "pontuacao_base": 88, "ano": 2021},
            {"titulo": "Star Wars: O Império Contra-Ataca", "pontuacao_base": 94, "ano": 1980},
            {"titulo": "Chegada", "pontuacao_base": 89, "ano": 2016}
        ],
        "Terror": [
            {"titulo": "O Iluminado", "pontuacao_base": 88, "ano": 1980},
            {"titulo": "Hereditário", "pontuacao_base": 87, "ano": 2018},
            {"titulo": "Um Lugar Silencioso", "pontuacao_base": 86, "ano": 2018},
            {"titulo": "Invocação do Mal", "pontuacao_base": 85, "ano": 2013},
            {"titulo": "Corra!", "pontuacao_base": 90, "ano": 2017}
        ]
    }
    return filmes

filmes = carregar_filmes()

# Configurações de preferência
st.sidebar.header("Suas Preferências")

# Preferências de gênero
st.sidebar.subheader("Gêneros de Filmes")
generos_preferidos = {}
for genero in filmes.keys():
    generos_preferidos[genero] = st.sidebar.checkbox(f"{genero}", key=f"genero_{genero}")

# Preferências de época
st.sidebar.subheader("Época")
epocas = {
    "Clássicos (Antes de 1990)": st.sidebar.checkbox("Clássicos (Antes de 1990)", value=True),
    "Modernos (1990-2010)": st.sidebar.checkbox("Modernos (1990-2010)", value=True),
    "Recentes (Após 2010)": st.sidebar.checkbox("Recentes (Após 2010)", value=True)
}

# Gerar recomendações
def gerar_recomendacoes():
    # Verificar se pelo menos um gênero foi selecionado
    if not any(generos_preferidos.values()):
        st.warning("Selecione pelo menos um gênero para obter recomendações.")
        return []
    
    recomendacoes = []
    
    # Processar cada gênero selecionado
    for genero, selecionado in generos_preferidos.items():
        if selecionado:
            for filme in filmes[genero]:
                # Verificar se o filme se encaixa nas preferências de época
                if (filme["ano"] < 1990 and epocas["Clássicos (Antes de 1990)"]) or \
                   (1990 <= filme["ano"] <= 2010 and epocas["Modernos (1990-2010)"]) or \
                   (filme["ano"] > 2010 and epocas["Recentes (Após 2010)"]):
                    
                    # Calcular pontuação ajustada com base nas preferências
                    pontuacao_ajustada = filme["pontuacao_base"]
                    
                    # Adicionar dados do filme e pontuação às recomendações
                    recomendacoes.append({
                        "Título": filme["titulo"],
                        "Gênero": genero,
                        "Ano": filme["ano"],
                        "Pontuação": pontuacao_ajustada
                    })
    
    # Ordenar por pontuação
    recomendacoes_df = pd.DataFrame(recomendacoes)
    if not recomendacoes_df.empty:
        recomendacoes_df = recomendacoes_df.sort_values("Pontuação", ascending=False)
    
    return recomendacoes_df

# Botão para gerar recomendações
if st.sidebar.button("Gerar Recomendações"):
    with st.spinner("Gerando recomendações personalizadas..."):
        recomendacoes_df = gerar_recomendacoes()
        
        if not recomendacoes_df.empty:
            st.success(f"Encontramos {len(recomendacoes_df)} filmes que correspondem às suas preferências!")
            
            # Exibir top recomendações
            st.subheader("Melhores Recomendações para Você")
            
            # Mostrar os 10 melhores filmes ou todos se forem menos de 10
            top_n = min(10, len(recomendacoes_df))
            top_recomendacoes = recomendacoes_df.head(top_n)
            
            # Exibir cada recomendação em um cartão
            for i, (_, filme) in enumerate(top_recomendacoes.iterrows()):
                with st.container():
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.subheader(f"#{i+1}")
                        st.metric("Pontuação", f"{filme['Pontuação']:.1f}/100")
                    with col2:
                        st.subheader(filme['Título'])
                        st.write(f"**Gênero:** {filme['Gênero']} | **Ano:** {filme['Ano']}")
                    st.divider()
            
            # Gráfico de barras para as pontuações
            st.subheader("Pontuações dos Filmes Recomendados")
            fig = px.bar(
                top_recomendacoes,
                x='Título',
                y='Pontuação',
                color='Gênero',
                title='Pontuação dos Filmes Recomendados',
                hover_data=['Ano']
            )
            fig.update_layout(xaxis_title='Filme', yaxis_title='Pontuação')
            st.plotly_chart(fig, use_container_width=True)
            
            # Análise de gêneros
            st.subheader("Distribuição por Gênero")
            genero_counts = recomendacoes_df['Gênero'].value_counts().reset_index()
            genero_counts.columns = ['Gênero', 'Quantidade']
            
            fig_pie = px.pie(
                genero_counts, 
                values='Quantidade', 
                names='Gênero',
                title='Distribuição de Gêneros nas Recomendações'
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        else:
            st.warning("Nenhum filme encontrado com as preferências selecionadas. Tente selecionar mais gêneros ou épocas.")
else:
    st.info("Selecione suas preferências de filmes no menu lateral e clique em 'Gerar Recomendações'.")
