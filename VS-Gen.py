import streamlit as st
from datetime import datetime
from utils.vsgen import Generator
from utils.sidebar import render_sidebar


lang, txt, model_provider = render_sidebar()

# page title
st.title(txt['vsg_title'])

# main content
subject = st.text_input(txt['subject'])
video_length = st.number_input(
    txt['video_length'], min_value=0.1, step=0.1, value=1.0)
creativity = st.slider(txt['creativity'], min_value=0.0,
                       max_value=1.0, step=0.1, value=0.3)

reference_prompt = ''
uploaded_file = st.file_uploader(txt['upload_file'], type=['txt'])
if uploaded_file:
    reference_prompt = uploaded_file.read().decode()

# disable button until all fields are valid
submit = st.button(
    txt['create_script'],
    type='primary',
    disabled=not (model_provider and subject)
)

# validate empty value
if submit and not model_provider:
    st.info(txt['select_model_info'])
    st.stop()
if submit and not subject:
    st.info(txt['enter_subject_info'])
    st.stop()

if submit:
    # generate results
    with st.spinner(txt['loading']):
        generator = Generator(model_provider, creativity)
        wiki_search, title, script = generator.generate_script(
            subject, video_length, lang, reference_prompt)
    # add generation history into session_state
    if 'history' not in st.session_state:
        st.session_state.history = []
    st.session_state.history.append({
        'subject': subject,
        'title': title,
        'time': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'model': model_provider,
    })
    # display the generated results
    st.success(txt['success'])
    st.subheader(txt['title_label'])
    st.write(title)
    st.subheader(txt['script_label'])
    st.write(script)
    with st.expander(txt['wiki_label']):
        st.info(wiki_search)

# print(st.session_state)
