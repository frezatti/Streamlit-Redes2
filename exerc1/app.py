import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Dashboard de Análise de Dados com Upload de CSV")

# Upload de arquivo
uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")

if uploaded_file is not None:
    # Carregar dados
    try:
        df = pd.read_csv(uploaded_file)
        
        # Exibir prévia dos dados
        st.subheader("Prévia dos Dados")
        st.dataframe(df.head())
        
        # Selecionar coluna para análise
        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        
        if numeric_columns:
            selected_column = st.selectbox("Selecione uma coluna numérica para análise:", numeric_columns)
            
            # Calcular estatísticas
            st.subheader("Estatísticas")
            media = df[selected_column].mean()
            mediana = df[selected_column].median()
            desvio = df[selected_column].std()
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Média", f"{media:.2f}")
            col2.metric("Mediana", f"{mediana:.2f}")
            col3.metric("Desvio Padrão", f"{desvio:.2f}")
            
            # Gráfico
            st.subheader("Visualização")
            fig = px.histogram(df, x=selected_column, nbins=20, title=f"Histograma de {selected_column}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("O arquivo não contém colunas numéricas para análise.")
    
    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
else:
    st.info("Por favor, faça upload de um arquivo CSV para começar.")
