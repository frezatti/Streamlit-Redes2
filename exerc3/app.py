import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title("Simulador de Investimento")

# Parâmetros do investimento
st.subheader("Parâmetros do Investimento")

col1, col2, col3 = st.columns(3)

with col1:
    valor_inicial = st.number_input(
        "Valor inicial (R$):",
        min_value=100.0,
        max_value=1000000.0,
        value=10000.0,
        step=100.0
    )

with col2:
    taxa_juros = st.slider(
        "Taxa de juros anual (%):",
        min_value=0.1,
        max_value=20.0,
        value=5.0,
        step=0.1
    )

with col3:
    periodos = st.selectbox(
        "Período (anos):",
        options=[1, 2, 3, 5, 10, 15, 20, 25, 30],
        index=4
    )

# Cálculo do investimento com juros compostos
@st.cache_data
def calcular_investimento(principal, taxa, anos):
    taxa_decimal = taxa / 100
    timeline = np.arange(0, anos + 1)
    valores = [principal * (1 + taxa_decimal) ** ano for ano in timeline]
    return pd.DataFrame({
        'Ano': timeline,
        'Valor (R$)': valores
    })

# Calcular crescimento do investimento
df_investimento = calcular_investimento(valor_inicial, taxa_juros, periodos)

# Resultados
st.subheader("Resultados")

col1, col2 = st.columns(2)

with col1:
    montante_final = df_investimento['Valor (R$)'].iloc[-1]
    st.metric(
        "Montante Final",
        f"R$ {montante_final:.2f}",
        f"{((montante_final / valor_inicial) - 1) * 100:.2f}%"
    )

with col2:
    juros_total = montante_final - valor_inicial
    st.metric(
        "Juros Totais",
        f"R$ {juros_total:.2f}"
    )

# Gráfico do crescimento
st.subheader("Crescimento ao Longo do Tempo")
fig = px.line(
    df_investimento,
    x='Ano',
    y='Valor (R$)',
    title='Crescimento do Investimento',
    markers=True
)
fig.update_layout(
    xaxis_title='Ano',
    yaxis_title='Valor (R$)',
    xaxis={'tickmode': 'linear', 'tick0': 0, 'dtick': max(1, periodos // 10)}
)
st.plotly_chart(fig, use_container_width=True)

# Tabela de valores
with st.expander("Detalhes por Ano"):
    df_investimento['Valor (R$)'] = df_investimento['Valor (R$)'].round(2)
    st.dataframe(df_investimento, hide_index=True)
