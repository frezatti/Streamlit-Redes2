import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import io

# Configuração da página
st.set_page_config(
    page_title="Painel Multi-página",
    page_icon="📊",
    layout="wide"
)

# Inicializar session_state se necessário
if 'dados' not in st.session_state:
    st.session_state.dados = None
if 'pagina_atual' not in st.session_state:
    st.session_state.pagina_atual = "Upload de Dados"

# Função para carregar dados com cache
@st.cache_data
def processar_dados(df):
    """Função com cache para processar os dados"""
    # Simulando algum processamento pesado
    return df.copy()

# Função para calcular estatísticas com cache
@st.cache_data
def calcular_estatisticas(df):
    """Calcula estatísticas dos dados com cache"""
    estatisticas = {
        "contagem": df.count(),
        "media": df.mean(numeric_only=True),
        "mediana": df.median(numeric_only=True),
        "desvio_padrao": df.std(numeric_only=True),
        "minimo": df.min(numeric_only=True),
        "maximo": df.max(numeric_only=True),
        "correlacao": df.corr() if len(df.select_dtypes(include=[np.number]).columns) > 1 else None
    }
    return estatisticas

# Navegação na barra lateral
st.sidebar.title("Navegação")
paginas = ["Upload de Dados", "Análise Estatística", "Gráficos Interativos"]
st.session_state.pagina_atual = st.sidebar.radio("Selecione uma página:", paginas)

# Função para gerar dados de exemplo
def gerar_dados_exemplo():
    np.random.seed(42)
    datas = pd.date_range(start="2023-01-01", periods=100, freq="D")
    
    df = pd.DataFrame({
        "data": datas,
        "vendas": np.random.randint(100, 1000, size=100),
        "temperatura": np.random.normal(25, 5, size=100),
        "preco": np.random.uniform(10, 50, size=100),
        "regiao": np.random.choice(["Norte", "Sul", "Leste", "Oeste"], size=100)
    })
    
    return df

# Página 1: Upload e visualização de dados
if st.session_state.pagina_atual == "Upload de Dados":
    st.title("Upload e Visualização de Dados")
    
    # Opções para carregar dados
    opcao_upload = st.radio(
        "Escolha como carregar os dados:",
        ("Fazer upload de arquivo CSV", "Gerar dados de exemplo")
    )
    
    if opcao_upload == "Fazer upload de arquivo CSV":
        uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")
        
        if uploaded_file is not None:
            try:
                # Leitura do arquivo CSV
                df = pd.read_csv(uploaded_file)
                st.session_state.dados = processar_dados(df)
                st.success(f"Arquivo carregado com sucesso! {len(df)} linhas e {len(df.columns)} colunas.")
            except Exception as e:
                st.error(f"Erro ao ler o arquivo: {e}")
                
    else:  # Gerar dados de exemplo
        if st.button("Gerar Dados de Exemplo"):
            df = gerar_dados_exemplo()
            st.session_state.dados = processar_dados(df)
            st.success("Dados de exemplo gerados com sucesso!")
    
    # Visualização dos dados
    if st.session_state.dados is not None:
        st.subheader("Visualização dos Dados")
        
        # Opção para filtrar colunas
        all_columns = st.session_state.dados.columns.tolist()
        selected_columns = st.multiselect(
            "Selecione as colunas para visualizar:",
            all_columns,
            default=all_columns[:5]  # Mostrar até 5 colunas por padrão
        )
        
        # Exibir dados filtrados
        if selected_columns:
            st.dataframe(st.session_state.dados[selected_columns].head(50))
        else:
            st.info("Selecione pelo menos uma coluna para visualizar os dados.")
        
        # Informações do dataset
        st.subheader("Informações do Dataset")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Número de linhas:** {st.session_state.dados.shape[0]}")
            st.write(f"**Número de colunas:** {st.session_state.dados.shape[1]}")
        
        with col2:
            # Verificar tipos de dados
            tipos_dados = st.session_state.dados.dtypes.value_counts()
            st.write("**Tipos de dados:**")
            for tipo, contagem in tipos_dados.items():
                st.write(f"- {tipo}: {contagem} colunas")
        
        # Download dos dados processados
        if st.button("Download dos dados processados"):
            csv = st.session_state.dados.to_csv(index=False)
            st.download_button(
                label="Clique para baixar",
                data=csv,
                file_name="dados_processados.csv",
                mime="text/csv"
            )
    else:
        st.info("Carregue um arquivo CSV ou gere dados de exemplo para começar.")

# Página 2: Análise estatística dos dados
elif st.session_state.pagina_atual == "Análise Estatística":
    st.title("Análise Estatística dos Dados")
    
    if st.session_state.dados is not None:
        df = st.session_state.dados
        
        # Filtrar apenas colunas numéricas para análise
        colunas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if not colunas_numericas:
            st.warning("Não há colunas numéricas para análise estatística.")
        else:
            # Estatísticas básicas com cache
            estatisticas = calcular_estatisticas(df)
            
            # Seleção de colunas para análise
            col_analise = st.multiselect(
                "Selecione as colunas para análise:",
                colunas_numericas,
                default=colunas_numericas[:3]  # Até 3 colunas por padrão
            )
            
            if col_analise:
                # Resumo estatístico
                st.subheader("Resumo Estatístico")
                
                tab1, tab2, tab3 = st.tabs(["Estatísticas Básicas", "Distribuição", "Correlação"])
                
                with tab1:
                    resumo = pd.DataFrame({
                        "Média": estatisticas["media"][col_analise],
                        "Mediana": estatisticas["mediana"][col_analise],
                        "Desvio Padrão": estatisticas["desvio_padrao"][col_analise],
                        "Mínimo": estatisticas["minimo"][col_analise],
                        "Máximo": estatisticas["maximo"][col_analise]
                    })
                    st.dataframe(resumo)
                
                with tab2:
                    for col in col_analise:
                        fig = px.histogram(df, x=col, nbins=20, 
                                          title=f"Distribuição de {col}")
                        fig.update_layout(bargap=0.1)
                        st.plotly_chart(fig, use_container_width=True)
                
                with tab3:
                    if len(col_analise) > 1:
                        st.subheader("Matriz de Correlação")
                        # Criar matriz de correlação entre as colunas selecionadas
                        corr_matrix = df[col_analise].corr()
                        
                        # Plotar com heatmap
                        fig = px.imshow(
                            corr_matrix,
                            text_auto=True,
                            color_continuous_scale="RdBu_r",
                            title="Matriz de Correlação"
                        )
                        st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Selecione pelo menos uma coluna para análise.")
    else:
        st.warning("Não há dados carregados. Por favor, volte à página 'Upload de Dados'.")

# Página 3: Gráficos interativos
elif st.session_state.pagina_atual == "Gráficos Interativos":
    st.title("Gráficos Interativos")
    
    if st.session_state.dados is not None:
        df = st.session_state.dados
        
        # Filtrar tipos de colunas
        colunas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
        colunas_categoricas = df.select_dtypes(include=["object", "category"]).columns.tolist()
        colunas_data = df.select_dtypes(include=["datetime"]).columns.tolist()
        
        all_columns = colunas_numericas + colunas_categoricas + colunas_data
        
        # Tipo de gráfico
        tipo_grafico = st.selectbox(
            "Selecione o tipo de gráfico:",
            ["Gráfico de Dispersão", "Gráfico de Barras", "Gráfico de Linha", "Gráfico de Área", "Gráfico de Pizza"]
        )
        
        if tipo_grafico == "Gráfico de Dispersão":
            if len(colunas_numericas) >= 2:
                col1, col2 = st.columns(2)
                
                with col1:
                    x_col = st.selectbox("Eixo X:", colunas_numericas, index=0)
                
                with col2:
                    y_col = st.selectbox("Eixo Y:", colunas_numericas, index=min(1, len(colunas_numericas)-1))
                
                # Opções para cor e tamanho
                cor_col = st.selectbox("Cor (opcional):", ["Nenhuma"] + all_columns)
                tamanho_col = st.selectbox("Tamanho (opcional):", ["Nenhuma"] + colunas_numericas)
                
                # Criar gráfico
                fig = px.scatter(
                    df, 
                    x=x_col, 
                    y=y_col,
                    color=None if cor_col == "Nenhuma" else cor_col,
                    size=None if tamanho_col == "Nenhuma" else tamanho_col,
                    title=f"{y_col} vs {x_col}",
                    labels={x_col: x_col, y_col: y_col}
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("São necessárias pelo menos duas colunas numéricas para criar um gráfico de dispersão.")
        
        elif tipo_grafico == "Gráfico de Barras":
            if colunas_categoricas and colunas_numericas:
                col1, col2 = st.columns(2)
                
                with col1:
                    x_col = st.selectbox("Eixo X (Categoria):", colunas_categoricas + colunas_numericas)
                
                with col2:
                    y_col = st.selectbox("Eixo Y (Valor):", colunas_numericas)
                
                # Opção para agrupar
                agrupar = st.checkbox("Agrupar valores")
                
                if agrupar:
                    # Usar groupby para agregar dados
                    df_group = df.groupby(x_col)[y_col].mean().reset_index()
                    fig = px.bar(
                        df_group, 
                        x=x_col, 
                        y=y_col,
                        title=f"Média de {y_col} por {x_col}"
                    )
                else:
                    fig = px.bar(
                        df, 
                        x=x_col, 
                        y=y_col,
                        title=f"{y_col} por {x_col}"
                    )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("São necessárias colunas categóricas e numéricas para criar um gráfico de barras.")
        
        elif tipo_grafico == "Gráfico de Linha":
            if colunas_numericas:
                # Seleção de colunas para o eixo x (preferência para data)
                if colunas_data:
                    x_options = colunas_data + colunas_numericas
                    x_default = 0  # Primeira coluna de data
                else:
                    x_options = colunas_numericas
                    x_default = 0
                
                x_col = st.selectbox("Eixo X:", x_options, index=x_default)
                
                # Seleção de colunas para o eixo y
                y_cols = st.multiselect(
                    "Eixo Y (pode selecionar múltiplas):", 
                    colunas_numericas,
                    default=[colunas_numericas[0]]
                )
                
                if y_cols:
                    fig = px.line(
                        df, 
                        x=x_col, 
                        y=y_cols,
                        title=f"Gráfico de Linha"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Selecione pelo menos uma coluna para o eixo Y.")
            else:
                st.warning("São necessárias colunas numéricas para criar um gráfico de linha.")
        
        elif tipo_grafico == "Gráfico de Área":
            if colunas_numericas:
                # Similar ao gráfico de linha
                if colunas_data:
                    x_options = colunas_data + colunas_numericas
                    x_default = 0
                else:
                    x_options = colunas_numericas
                    x_default = 0
                
                x_col = st.selectbox("Eixo X:", x_options, index=x_default)
                
                y_cols = st.multiselect(
                    "Eixo Y (pode selecionar múltiplas):", 
                    colunas_numericas,
                    default=[colunas_numericas[0]]
                )
                
                if y_cols:
                    fig = px.area(
                        df, 
                        x=x_col, 
                        y=y_cols,
                        title=f"Gráfico de Área"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Selecione pelo menos uma coluna para o eixo Y.")
            else:
                st.warning("São necessárias colunas numéricas para criar um gráfico de área.")
        
        elif tipo_grafico == "Gráfico de Pizza":
            if colunas_categoricas and colunas_numericas:
                col1, col2 = st.columns(2)
                
                with col1:
                    labels_col = st.selectbox("Rótulos (Categoria):", colunas_categoricas)
                
                with col2:
                    values_col = st.selectbox("Valores:", colunas_numericas)
                
                # Agrupar dados para o gráfico de pizza
                df_group = df.groupby(labels_col)[values_col].sum().reset_index()
                
                fig = px.pie(
                    df_group,
                    values=values_col,
                    names=labels_col,
                    title=f"Distribuição de {values_col} por {labels_col}"
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("São necessárias colunas categóricas e numéricas para criar um gráfico de pizza.")
        
        # Opções de exportação do gráfico
        st.subheader("Exportar Gráfico")
        formato = st.radio("Selecione o formato:", ["PNG", "HTML"], horizontal=True)
        
        if st.button("Exportar Gráfico"):
            if formato == "PNG":
                # Nota: No Streamlit real, isso salvaria a imagem
                st.success("Função de exportação PNG disponível no Streamlit!")
            else:  # HTML
                # Nota: No Streamlit real, isso salvaria o HTML interativo
                st.success("Função de exportação HTML disponível no Streamlit!")
    else:
        st.warning("Não há dados carregados. Por favor, volte à página 'Upload de Dados'.")

# Informações na barra lateral
with st.sidebar:
    st.divider()
    st.info("""
    **Sobre o Dashboard**
    
    Este é um dashboard de análise de dados com:
    - Upload e visualização de dados
    - Análise estatística com cache
    - Gráficos interativos
    """)
    
    # Mostrar status dos dados carregados
    if st.session_state.dados is not None:
        st.success(f"✅ Dados carregados: {st.session_state.dados.shape[0]} linhas")
    else:
        st.error("❌ Nenhum dado carregado")
