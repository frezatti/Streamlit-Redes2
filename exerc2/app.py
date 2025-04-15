import streamlit as st
import pandas as pd
import numpy as np

st.title("Filtro Dinâmico em Tabela")

# Criar dados de exemplo
@st.cache_data
def load_data():
 try:
        df = pd.read_csv('products_data.csv')
        return df
 except FileNotFoundError:
        st.error("Arquivo 'products_data.csv' não encontrado. Verifique se o arquivo está no diretório correto.")
        # Return an empty DataFrame or fallback to sample data
        return pd.DataFrame()

df = load_data()

# Exibir todos os dados
st.subheader("Dados Completos")
st.dataframe(df)

# Filtros
st.subheader("Filtros")

# Filtros para colunas categóricas
col1, col2 = st.columns(2)

with col1:
    # Multiselect para cidades
    cidades = df['Cidade'].unique().tolist()
    cidades_selecionadas = st.multiselect('Filtrar por Cidade:', cidades, default=cidades)

with col2:
    # Multiselect para categorias
    categorias = df['Categoria'].unique().tolist()
    categorias_selecionadas = st.multiselect('Filtrar por Categoria:', categorias, default=categorias)

# Filtros para colunas numéricas
col3, col4 = st.columns(2)

with col3:
    # Slider para vendas
    vendas_min, vendas_max = int(df['Vendas'].min()), int(df['Vendas'].max())
    vendas_range = st.slider('Faixa de Vendas:', vendas_min, vendas_max, (vendas_min, vendas_max))

with col4:
    # Slider para avaliação
    aval_min, aval_max = float(df['Avaliação'].min()), float(df['Avaliação'].max())
    aval_range = st.slider('Faixa de Avaliação:', aval_min, aval_max, (aval_min, aval_max))

# Aplicar filtros
filtered_df = df[
    (df['Cidade'].isin(cidades_selecionadas)) &
    (df['Categoria'].isin(categorias_selecionadas)) &
    (df['Vendas'] >= vendas_range[0]) & (df['Vendas'] <= vendas_range[1]) &
    (df['Avaliação'] >= aval_range[0]) & (df['Avaliação'] <= aval_range[1])
]

# Exibir resultados filtrados
st.subheader("Resultados Filtrados")
st.dataframe(filtered_df)

# Estatísticas
st.subheader("Estatísticas")
st.metric("Total de Registros", filtered_df.shape[0])
st.metric("Média de Vendas", f"R$ {filtered_df['Vendas'].mean():.2f}")
