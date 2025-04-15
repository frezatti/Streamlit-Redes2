import streamlit as st
import pandas as pd
from io import StringIO as io 

st.title("Exercicio 1")
uploaded_file = st.file_uploader("upload csv file for analises","csv",False,)
if uploaded_file is not None :

    dataframe = pd.read_csv(uploaded_file)
    st.dataframe(dataframe)
    selection_columns =  [""] + list(dataframe.columns)
    selection = st.selectbox("Select column",selection_columns)

    if selection != "":
        column =  dataframe[selection]
        if pd.api.types.is_numeric_dtype(column):
            column.mean()
            column.std()
            column.median()
