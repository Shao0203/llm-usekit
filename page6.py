import streamlit as st
from streamlit import session_state as ss


# print(st.session_state)
# if 'num' not in st.session_state:
#     st.session_state.num = 0
# clicked = st.button('Plus 1')
# if clicked:
#     st.session_state.num += 1
# st.write(st.session_state.num)

# print(st.session_state)


# sss = st.session_state
# print(sss)
# if 'num' not in sss:
#     sss.num = 0
# clicked = st.button('Plus 1')
# if clicked:
#     sss.num += 1
# st.write(sss.num)

# print(sss)


print('up', ss)
if 'num' not in ss:
    ss.num = 0

clicked = st.button('Plus 1')
if clicked:
    ss.num += 1

st.write(ss.num)
print('down', ss)
