import streamlit as st
from rag_tool import get_rag_response


if 'session_id' not in st.session_state:
    st.session_state.session_id = 'session_1'
    st.session_state.session_counter = 1
    st.session_state.chat_history = []

st.title('📑 AI文档问答助手')

uploaded_file = st.file_uploader('上传你的文件', type=['txt', 'pdf'])

question = st.text_input('提出相关问题', disabled=not uploaded_file)

if uploaded_file and question:
    with st.spinner('AI is thinking...'):
        response = get_rag_response(
            question, uploaded_file, st.session_state.session_id)
