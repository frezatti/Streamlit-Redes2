import streamlit as st

st.title("Formulário com Validação e Resultados")

# Função para limpar o formulário
def limpar_formulario():
    st.session_state.nome = ""
    st.session_state.idade = 18
    st.session_state.cores = []
    st.session_state.submit_pressed = False

# Inicializar o estado da sessão
if 'submit_pressed' not in st.session_state:
    st.session_state.submit_pressed = False

# Criar o formulário
with st.form("form_cadastro"):
    st.subheader("Preencha seus dados")
    
    # Campo de nome
    nome = st.text_input(
        "Nome",
        key="nome",
        placeholder="Digite seu nome completo"
    )
    
    # Campo de idade
    idade = st.number_input(
        "Idade",
        min_value=0,
        max_value=120,
        value=18,
        step=1,
        key="idade"
    )
    
    # Preferência de cores
    cores_opcoes = ["Vermelho", "Azul", "Verde", "Amarelo", "Roxo", "Laranja", "Preto", "Branco"]
    cores = st.multiselect(
        "Quais são suas cores favoritas?",
        options=cores_opcoes,
        key="cores"
    )
    
    # Botões
    col1, col2 = st.columns(2)
    with col1:
        submit_button = st.form_submit_button("Enviar")
    with col2:
        clear_button = st.form_submit_button("Limpar", on_click=limpar_formulario)
    
    # Verificar se o botão enviar foi pressionado
    if submit_button:
        st.session_state.submit_pressed = True

# Função para validar o formulário
def validar_form(nome, idade, cores):
    erros = []
    
    if not nome.strip():
        erros.append("O nome é obrigatório.")
    elif len(nome.strip()) < 3:
        erros.append("O nome deve ter pelo menos 3 caracteres.")
    
    if idade < 0 or idade > 120:
        erros.append("A idade deve estar entre 0 e 120 anos.")
    
    if not cores:
        erros.append("Selecione pelo menos uma cor favorita.")
    
    return erros

# Exibir resultados ou erros após submissão
if st.session_state.submit_pressed:
    erros = validar_form(
        st.session_state.nome,
        st.session_state.idade,
        st.session_state.cores
    )
    
    if erros:
        st.error("Por favor, corrija os seguintes erros:")
        for erro in erros:
            st.write(f"- {erro}")
    else:
        st.success("Formulário enviado com sucesso!")
        
        # Exibir resultado personalizado
        st.subheader("Resultado")
        
        msg = f"Olá, {st.session_state.nome}, com {st.session_state.idade} anos, "
        
        if len(st.session_state.cores) == 1:
            msg += f"sua cor favorita é {st.session_state.cores[0]}!"
        else:
            cores_formatadas = ", ".join(st.session_state.cores[:-1]) + f" e {st.session_state.cores[-1]}"
            msg += f"suas cores favoritas são {cores_formatadas}!"
        
        st.write(msg)
        
        # Exibir um cartão colorido para cada cor selecionada
        st.subheader("Suas cores favoritas:")
        
        cores_html = ""
        for cor in st.session_state.cores:
            cor_lower = cor.lower()
            cores_html += f"""
            <div style="
                background-color: {cor_lower};
                color: {'white' if cor_lower in ['preto', 'azul', 'roxo', 'vermelho'] else 'black'};
                padding: 10px;
                border-radius: 5px;
                margin: 5px;
                text-align: center;
                font-weight: bold;
                display: inline-block;
                width: 120px;
            ">
                {cor}
            </div>
            """
        
        st.markdown(cores_html, unsafe_allow_html=True)
