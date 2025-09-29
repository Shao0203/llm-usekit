import streamlit as st
from utils.rag_tool import get_rag_response
from utils.sidebar import render_sidebar


lang, txt, model_provider = render_sidebar()

if 'sid' not in st.session_state:
    st.session_state.chat_history = []

st.title(txt['qa_title'])

uploaded_file = st.file_uploader(
    txt['qa_upload_hint'], type=['txt', 'pdf', 'docx'])

left, right = st.columns([6, 1])
question = left.text_input(label='qa', label_visibility='collapsed',
                           placeholder=txt['qa_question_hint'],  disabled=not uploaded_file)
submit = right.button(txt['submit_question'],
                      disabled=not (uploaded_file and question))

if submit and uploaded_file and question:
    with st.spinner(txt['loading']):
        response = get_rag_response(question, uploaded_file)
    st.write(txt['qa_answer'])
    st.write(response)
    st.session_state.chat_history.append(question)
    st.session_state.chat_history.append(response)

if st.session_state.chat_history:
    with st.expander(txt['qa_history']):
        for i in range(0, len(st.session_state.chat_history), 2):
            st.write(f'{(i+2)//2}. ' + st.session_state.chat_history[i])
            st.write(st.session_state.chat_history[i+1])
            st.divider()

print(st.session_state)
