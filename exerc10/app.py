import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
import json

# Configuração da página
st.set_page_config(
    page_title="Explorador de Países",
    page_icon="🌍",
    layout="wide"
)

# Título do aplicativo
st.title("🌍 Explorador de Países")
st.markdown("""
Este aplicativo usa a API REST Countries para mostrar informações sobre os países do mundo.
Digite o nome de um país para explorar seus dados demográficos, econômicos e geográficos.
""")

# Função para buscar dados da API
@st.cache_data(ttl=3600)  # Cache por 1 hora
def buscar_paises():
    """Busca todos os países da API REST Countries"""
    try:
        url = "https://restcountries.com/v3.1/all"
        response = requests.get(url)
        response.raise_for_status()  # Verificar se a requisição foi bem-sucedida
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao acessar a API: {e}")
        return None

@st.cache_data(ttl=3600)  # Cache por 1 hora
def buscar_pais_por_nome(nome):
    """Busca um país específico pelo nome"""
    try:
        url = f"https://restcountries.com/v3.1/name/{nome}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao buscar dados do país: {e}")
        return None

# Carregar lista de países para o autocomplete
todos_paises = buscar_paises()

if todos_paises:
    # Extrair nomes dos países para o autocomplete
    nomes_paises = [pais.get('name', {}).get('common', '') for pais in todos_paises]
    nomes_paises = sorted([nome for nome in nomes_paises if nome])
    
    # Interface para buscar país
    col1, col2 = st.columns([3, 1])
    
    with col1:
        nome_pais = st.selectbox(
            "Selecione um país:",
            options=nomes_paises,
            index=nomes_paises.index("Brazil") if "Brazil" in nomes_paises else 0
        )
    
    with col2:
        buscar = st.button("Buscar Informações", type="primary")
    
    # Buscar e exibir informações do país
    if buscar or 'ultimo_pais' in st.session_state:
        # Atualizar país na sessão
        if buscar:
            st.session_state.ultimo_pais = nome_pais
        else:
            nome_pais = st.session_state.ultimo_pais
        
        # Buscar dados do país selecionado
        dados_pais = buscar_pais_por_nome(nome_pais)
        
        if dados_pais and len(dados_pais) > 0:
            pais = dados_pais[0]  # Pegar o primeiro resultado
            
            # Extrair dados principais
            bandeira_url = pais.get('flags', {}).get('png', '')
            nome_oficial = pais.get('name', {}).get('official', 'N/A')
            capital = pais.get('capital', ['N/A'])[0] if pais.get('capital') else 'N/A'
            regiao = pais.get('region', 'N/A')
            subregiao = pais.get('subregion', 'N/A')
            populacao = pais.get('population', 0)
            area = pais.get('area', 0)
            
            # Criando tabs para organizar a informação
            tab1, tab2, tab3 = st.tabs(["Informações Básicas", "Demografia", "Mapa"])
            
            # Tab 1: Informações Básicas
            with tab1:
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    if bandeira_url:
                        st.image(bandeira_url, caption=f"Bandeira de {nome_pais}", width=200)
                
                with col2:
                    st.subheader(nome_oficial)
                    st.write(f"**Capital:** {capital}")
                    st.write(f"**Região:** {regiao}")
                    st.write(f"**Sub-região:** {subregiao}")
                    
                    # Moedas
                    moedas = pais.get('currencies', {})
                    if moedas:
                        moedas_str = ", ".join([f"{info.get('name', 'N/A')} ({code})" 
                                              for code, info in moedas.items()])
                        st.write(f"**Moeda(s):** {moedas_str}")
                    
                    # Idiomas
                    idiomas = pais.get('languages', {})
                    if idiomas:
                        idiomas_str = ", ".join(idiomas.values())
                        st.write(f"**Idioma(s):** {idiomas_str}")
                    
                    # Fuso horário
                    fusos = pais.get('timezones', ['N/A'])
                    st.write(f"**Fuso(s) horário(s):** {', '.join(fusos)}")
                
                # Informações adicionais
                st.subheader("Detalhes Adicionais")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("População", f"{populacao:,}".replace(",", "."))
                
                with col2:
                    st.metric("Área", f"{area:,.1f} km²".replace(",", "."))
                
                with col3:
                    if populacao > 0 and area > 0:
                        densidade = populacao / area
                        st.metric("Densidade", f"{densidade:.1f} hab/km²".replace(".", ","))
            
            # Tab 2: Demografia
            with tab2:
                st.subheader("Dados Demográficos")
                
                # Criar dados comparativos com países da mesma região
                paises_regiao = [p for p in todos_paises if p.get('region') == regiao]
                
                # Dados para o gráfico de população
                df_pop = pd.DataFrame([
                    {
                        'pais': p.get('name', {}).get('common', ''),
                        'populacao': p.get('population', 0)
                    }
                    for p in paises_regiao
                ])
                
                # Ordenar e pegar os 15 maiores
                df_pop = df_pop.sort_values('populacao', ascending=False).head(15)
                
                # Destacar o país selecionado
                df_pop['destacado'] = df_pop['pais'] == nome_pais
                
                # Criar gráfico de barras para população
                fig_pop = px.bar(
                    df_pop,
                    x='pais',
                    y='populacao',
                    title=f"População dos Maiores Países da Região {regiao}",
                    color='destacado',
                    color_discrete_map={True: 'red', False: 'blue'},
                    labels={'pais': 'País', 'populacao': 'População'},
                    height=500
                )
                
                # Melhorar layout
                fig_pop.update_layout(
                    xaxis_title="País",
                    yaxis_title="População",
                    xaxis={'categoryorder': 'total descending'}
                )
                
                st.plotly_chart(fig_pop, use_container_width=True)
                
                # Gráfico de área
                df_area = pd.DataFrame([
                    {
                        'pais': p.get('name', {}).get('common', ''),
                        'area': p.get('area', 0)
                    }
                    for p in paises_regiao if p.get('area', 0) > 0
                ])
                
                # Ordenar e pegar os 15 maiores
                df_area = df_area.sort_values('area', ascending=False).head(15)
                
                # Destacar o país selecionado
                df_area['destacado'] = df_area['pais'] == nome_pais
                
                # Criar gráfico de barras para área
                fig_area = px.bar(
                    df_area,
                    x='pais',
                    y='area',
                    title=f"Área dos Maiores Países da Região {regiao} (km²)",
                    color='destacado',
                    color_discrete_map={True: 'red', False: 'green'},
                    labels={'pais': 'País', 'area': 'Área (km²)'},
                    height=500
                )
                
                # Melhorar layout
                fig_area.update_layout(
                    xaxis_title="País",
                    yaxis_title="Área (km²)",
                    xaxis={'categoryorder': 'total descending'}
                )
                
                st.plotly_chart(fig_area, use_container_width=True)
            
            # Tab 3: Mapa
            with tab3:
                st.subheader("Localização")
                
                # Extrair coordenadas do país
                lat = pais.get('latlng', [0, 0])[0] if pais.get('latlng') else 0
                lon = pais.get('latlng', [0, 0])[1] if pais.get('latlng') else 0
                
                # Criar DataFrame para o mapa
                df_mapa = pd.DataFrame({
                    'pais': [nome_pais],
                    'lat': [lat],
                    'lon': [lon],
                    'populacao': [populacao]
                })
                
                # Criar mapa com Plotly
                fig_mapa = px.scatter_geo(
                    df_mapa,
                    lat='lat',
                    lon='lon',
                    text='pais',
                    size='populacao',
                    projection='natural earth',
                    title=f"Localização de {nome_pais}",
                    size_max=30,
                    color_discrete_sequence=['red']
                )
                
                # Centralizar o mapa no país
                fig_mapa.update_geos(
                    center=dict(lat=lat, lon=lon),
                    projection_scale=3 if pais.get('area', 0) < 500000 else 2
                )
                
                st.plotly_chart(fig_mapa, use_container_width=True)
                
                # Informações de fronteiras
                fronteiras = pais.get('borders', [])
                if fronteiras:
                    # Buscar nomes dos países vizinhos
                    nomes_vizinhos = []
                    for codigo in fronteiras:
                        for p in todos_paises:
                            if p.get('cca3') == codigo:
                                nomes_vizinhos.append(p.get('name', {}).get('common', codigo))
                                break
                    
                    st.write(f"**Países Vizinhos:** {', '.join(sorted(nomes_vizinhos))}")
                else:
                    st.write("**País sem fronteiras terrestres**")
        else:
            st.error(f"Não foi possível encontrar dados para {nome_pais}")
else:
    st.error("Não foi possível carregar a lista de países. Verifique sua conexão com a internet e tente novamente.")

# Rodapé com informações
st.divider()
st.markdown("""
**Sobre este aplicativo:**
- Dados fornecidos pela API [REST Countries](https://restcountries.com)
- Visualizações criadas com Plotly e Streamlit
- Última atualização: Abril 2025
""")

# Adicionar cache para melhorar a performance
if "paises_cache" not in st.session_state:
    st.session_state.paises_cache = {}
