import streamlit as st
import pandas as pd
import numpy as np

st.title("Mapa Interativo com Dados Geográficos")

# Criar dados de exemplo para o mapa
@st.cache_data
def gerar_dados_geo():
    # Coordenadas aproximadas de algumas cidades brasileiras
    
    
    for cidade, coords in cidades.items():
        # Adicionar entre 3 e 8 pontos para cada cidade
        for _ in range(np.random.randint(3, 9)):
            # Adicionar uma pequena variação às coordenadas
            lat_var = coords[0] + np.random.uniform(-0.05, 0.05)
            lon_var = coords[1] + np.random.uniform(-0.05, 0.05)
            
            # Categorias de eventos aleatórios
            categoria = np.random.choice(['Turismo', 'Negócios', 'Educação', 'Cultura'])
            
            dados.append({
                'cidade': cidade,
                'latitude': lat_var,
                'longitude': lon_var,
                'categoria': categoria,
                'valor': np.random.randint(10, 100)
            })
    
    return pd.DataFrame(dados)

# Carregar dados
dados_geo = gerar_dados_geo()

# Filtros
st.sidebar.header("Filtros")

# Filtro por cidade
cidades_disponiveis = ['Todas'] + sorted(dados_geo['cidade'].unique().tolist())
cidade_selecionada = st.sidebar.selectbox('Filtrar por Cidade:', cidades_disponiveis)

# Filtro por categoria
categorias_disponiveis = ['Todas'] + sorted(dados_geo['categoria'].unique().tolist())
categoria_selecionada = st.sidebar.selectbox('Filtrar por Categoria:', categorias_disponiveis)

# Aplicar filtros
dados_filtrados = dados_geo.copy()

if cidade_selecionada != 'Todas':
    dados_filtrados = dados_filtrados[dados_filtrados['cidade'] == cidade_selecionada]

if categoria_selecionada != 'Todas':
    dados_filtrados = dados_filtrados[dados_filtrados['categoria'] == categoria_selecionada]

# Exibir informações
st.write(f"Exibindo {len(dados_filtrados)} pontos no mapa")

# Exibir mapa
st.map(dados_filtrados)

# Tabela de dados
with st.expander("Ver detalhes dos pontos"):
    st.dataframe(
        dados_filtrados[['cidade', 'categoria', 'valor', 'latitude', 'longitude']], 
        hide_index=True
    )

# Estatísticas
col1, col2 = st.columns(2)
with col1:
    st.metric("Total de pontos", len(dados_filtrados))
with col2:
    st.metric("Valor médio", f"{dados_filtrados['valor'].mean():.2f}")
