import streamlit as st
from utils.rag_tool import get_rag_response
from utils.sidebar import render_sidebar


lang, t, model_provider = render_sidebar()

if 'sid' not in st.session_state:
    st.session_state.chat_history = []

st.title('📑 AI文档问答助手')

uploaded_file = st.file_uploader(
    '上传你的文件，AI将参考它回答你的问题', type=['txt', 'pdf', 'docx'])

left, right = st.columns([6, 1])
question = left.text_input(label='问题', label_visibility='collapsed',
                           placeholder='提出相关问题',  disabled=not uploaded_file)
submit = right.button('提交问题', disabled=not (uploaded_file and question))

if submit and uploaded_file and question:
    with st.spinner('AI is thinking...'):
        response = get_rag_response(question, uploaded_file)
    st.write('### 答案')
    st.write(response)
    st.session_state.chat_history.append(question)
    st.session_state.chat_history.append(response)

if st.session_state.chat_history:
    with st.expander('历史消息'):
        for i in range(0, len(st.session_state.chat_history), 2):
            st.write(f'{(i+2)//2}. ' + st.session_state.chat_history[i])
            st.write(st.session_state.chat_history[i+1])
            st.divider()

print(st.session_state)
