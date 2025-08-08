import streamlit as st

st.write('## Hello!')

name = st.text_input('please input your name.')
if name:
    st.write(f'Welcome {name} ~')

password = st.text_input('please enter your password', type='password')

intro = st.text_area('Please introduce yourself:')

age = st.number_input('Please enter your age:', value=20,
                      min_value=0, max_value=150, step=1)
st.write(f'You are {age} years old.')

is_agreed = st.checkbox('Agree')
if is_agreed:
    st.write('Thanks!')

st.divider()

is_submitted = st.button('Submit', type='primary')
if is_submitted:
    st.write('Submitted Successfully!')
