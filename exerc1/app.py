import streamlit as st
import pandas as pd

st.title("Exercicio 1")
uploaded_file = st.file_uploader("upload csv file for analises","csv",False,)
if uploaded_file is not None :
    string_file = uploaded_file.getvalue().decode("utf-8")
    st.write(string_file)


