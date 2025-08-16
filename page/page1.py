import streamlit as st
import pandas as pd


st.write('## *Hello world* !!!')

st.image('./pages/Rabbit.jpeg', width=200)

['apple', 'pear', 'orange']

{'name': 'Tom', 'age': 20, 'gender': 'male', 'hobby': 'sports'}

2**10

df = pd.DataFrame({
    'name': ['Bob', 'Candy', 'Dave', 'Eddy'],
    'id': ['01', '02', '03', '04'],
    'class': ['one', 'two', 'three', 'four'],
    'grade': [60, 70, 80, 90],
})

df
st.divider()
st.dataframe(df)
st.table(df)
