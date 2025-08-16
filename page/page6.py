import streamlit as st
from streamlit import session_state as ss


print('Start: ', st.session_state)

if 'num' not in st.session_state:
    st.session_state.num = 0
clicked = st.button('Plus 1')
if clicked:
    st.session_state.num += 1
st.write(st.session_state.num)

print('End: ', st.session_state)
