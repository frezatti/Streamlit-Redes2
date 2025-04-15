import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

st.title("Aplicativo de Previsão de Notas")
st.write("Este aplicativo prevê a nota final com base nas horas de estudo e notas anteriores.")

# Criar dados de exemplo para o modelo
@st.cache_data
def gerar_dados_exemplo():
    np.random.seed(42)
    horas_estudo = np.random.uniform(1, 10, 100)
    nota_anterior = np.random.uniform(3, 10, 100)
    
    # Simular uma relação: nota_final = 2 + 0.5*horas_estudo + 0.3*nota_anterior + ruído
    nota_final = 2 + 0.5 * horas_estudo + 0.3 * nota_anterior + np.random.normal(0, 1, 100)
    
    # Garantir que as notas estejam no intervalo 0-10
    nota_final = np.clip(nota_final, 0, 10)
    
    df = pd.DataFrame({
        'horas_estudo': horas_estudo,
        'nota_anterior': nota_anterior,
        'nota_final': nota_final
    })
    
    return df

dados = gerar_dados_exemplo()

# Treinar modelo de regressão linear
X = dados[['horas_estudo', 'nota_anterior']]
y = dados['nota_final']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

modelo = LinearRegression()
modelo.fit(X_train, y_train)

# Interface para inserção de dados
st.sidebar.header("Parâmetros de Entrada")

horas_estudo = st.sidebar.slider(
    "Horas de estudo por semana",
    min_value=1.0,
    max_value=10.0,
    value=5.0,
    step=0.5
)

nota_anterior = st.sidebar.number_input(
    "Nota anterior (0-10)",
    min_value=0.0,
    max_value=10.0,
    value=7.0,
    step=0.5
)

# Fazer previsão
entrada = np.array([[horas_estudo, nota_anterior]])
previsao = modelo.predict(entrada)[0]

# Exibir resultados
st.header("Resultados da Previsão")
col1, col2 = st.columns(2)

with col1:
    st.metric("Horas de Estudo", f"{horas_estudo} horas")
    st.metric("Nota Anterior", f"{nota_anterior}")

with col2:
    st.metric("Previsão de Nota Final", f"{previsao:.2f}")

# Avaliação do modelo
y_pred_test = modelo.predict(X_test)
r2 = r2_score(y_test, y_pred_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))

st.write(f"Coeficiente de determinação (R²): {r2:.2f}")
st.write(f"Erro médio quadrático (RMSE): {rmse:.2f}")

# Gráfico comparativo
st.header("Visualização dos Dados")

# Adicionar o ponto da previsão aos dados
novo_ponto = pd.DataFrame({
    'horas_estudo': [horas_estudo],
    'nota_anterior': [nota_anterior],
    'nota_final': [previsao],
    'tipo': ['Previsão']
})

dados_viz = dados.copy()
dados_viz['tipo'] = 'Dados Originais'
dados_viz_completo = pd.concat([dados_viz, novo_ponto])

# Gráfico 3D com Plotly
fig = px.scatter_3d(dados_viz_completo, x='horas_estudo', y='nota_anterior', z='nota_final',
                   color='tipo', color_discrete_map={'Dados Originais': 'blue', 'Previsão': 'red'},
                   opacity=0.7, title="Relação entre Horas de Estudo, Nota Anterior e Nota Final")

fig.update_layout(scene=dict(xaxis_title='Horas de Estudo',
                            yaxis_title='Nota Anterior',
                            zaxis_title='Nota Final'),
                 width=800, height=600)

st.plotly_chart(fig)

# Gráfico de dispersão 2D com a linha de regressão
fig2 = px.scatter(dados, x='horas_estudo', y='nota_final', 
                 title="Relação entre Horas de Estudo e Nota Final",
                 labels={'horas_estudo': 'Horas de Estudo', 'nota_final': 'Nota Final'})

# Adicionar linha de tendência
x_range = np.linspace(1, 10, 100)
y_pred = modelo.predict(np.column_stack((x_range, np.ones(100) * nota_anterior)))
fig2.add_scatter(x=x_range, y=y_pred, mode='lines', name='Linha de Regressão')

# Adicionar ponto da previsão
fig2.add_scatter(x=[horas_estudo], y=[previsao], mode='markers', 
                marker=dict(size=12, color='red'), name='Sua Previsão')

st.plotly_chart(fig2)

# Explicação do modelo
st.header("Interpretação do Modelo")
st.write(f"Intercepto: {modelo.intercept_:.4f}")
st.write(f"Coeficiente para horas de estudo: {modelo.coef_[0]:.4f}")
st.write(f"Coeficiente para nota anterior: {modelo.coef_[1]:.4f}")

st.write("""
Esta interpretação significa que:
- Para cada hora adicional de estudo, espera-se um aumento médio de {:.2f} pontos na nota final.
- Para cada ponto adicional na nota anterior, espera-se um aumento médio de {:.2f} pontos na nota final.
""".format(modelo.coef_[0], modelo.coef_[1]))
