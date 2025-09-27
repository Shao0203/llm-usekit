import streamlit as st
from utils.vsgen import Generator
from datetime import datetime
import json

# multi-languages dictionary
with open('texts.json', 'r', encoding='utf-8') as f:
    TEXTS = json.load(f)

# sidebar
with st.sidebar:
    lang = st.radio(label='选择语言', options=['Chinese', 'English'])
    t = TEXTS[lang]  # define current language dictionary

    model_provider = st.selectbox(
        t['select_model'], ['OpenAI', 'DeepSeek', 'KIMI'], index=1)
    api_key = st.text_input(t['enter_api_key'], type='password')
    remember = st.checkbox(t['remember'])
    st.divider()

    st.markdown(t['get_openai_key'])
    st.markdown(t['get_deepseek_key'])
    st.markdown(t['get_kimi_key'])

    st.subheader(t['gen_history'])
    if 'history' in st.session_state:
        for idx, item in enumerate(st.session_state.history[::-1][:5]):
            st.caption(f"{idx+1}: {item['subject']} - {item['title'][:50]}...")

# page title
st.title(t['title'])

# main content
subject = st.text_input(t['subject'])
video_length = st.number_input(
    t['video_length'], min_value=0.1, step=0.1, value=1.0)
creativity = st.slider(t['creativity'], min_value=0.0,
                       max_value=1.0, step=0.1, value=0.3)

reference_prompt = ''
uploaded_file = st.file_uploader(t['upload_file'], type=['txt'])
if uploaded_file:
    reference_prompt = uploaded_file.read().decode()

# disable button until all fields are valid
submit = st.button(
    t['create_script'],
    type='primary',
    disabled=not (model_provider and api_key and subject)
)

# validate empty value
if submit and not model_provider:
    st.info(t['select_model_info'])
    st.stop()
if submit and not api_key:
    st.info(t['enter_api_key_info'])
    st.stop()
if submit and not subject:
    st.info(t['enter_subject_info'])
    st.stop()

if submit:
    # generate results
    with st.spinner(t['loading']):
        generator = Generator(api_key, model_provider, creativity)
        wiki_search, title, script = generator.generate_script(
            subject, video_length, lang, reference_prompt)
    # add history and config into session_state
    if 'history' not in st.session_state:
        st.session_state.history = []
    st.session_state.history.append({
        'subject': subject,
        'title': title,
        'time': datetime.now().strftime('%Y-%m-%d %H:%M')
    })
    if remember:
        st.session_state.config = {
            'lang': lang,
            'model_provider': model_provider,
            'subject': subject,
            'video_length': video_length,
            'creativity': creativity
        }
    # display the generated results
    st.success(t['success'])
    st.subheader(t['title_label'])
    st.write(title)
    st.subheader(t['script_label'])
    st.write(script)
    with st.expander(t['wiki_label']):
        st.info(wiki_search)

# print(st.session_state)
