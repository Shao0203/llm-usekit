import streamlit as st

st.write('## Hello!')

with st.sidebar:
    name = st.text_input('please input your name.')
    if name:
        st.write(f'Welcome {name} ~')

column1, column2, column3 = st.columns([1, 2, 1])
with column1:
    password = st.text_input('please enter your password', type='password')

with column2:
    intro = st.text_area('Please introduce yourself:')

with column3:
    age = st.number_input('Please enter your age:', value=20,
                          min_value=0, max_value=150, step=1)
    st.write(f'You are {age} years old.')

st.divider()

is_agreed = st.checkbox('Agree')

is_submitted = st.button('Submit', type='primary')
if is_submitted:
    st.write('Submitted Successfully!')
