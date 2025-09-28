import streamlit as st
from datetime import datetime
from utils.vsgen import Generator
from utils.sidebar import render_sidebar

# Initialize session_state
# if 'lang' not in st.session_state:
#     st.session_state.lang = 'Chinese'
# if 'model_provider' not in st.session_state:
#     st.session_state.model_provider = 'DeepSeek'

lang, t, model_provider = render_sidebar()

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
    disabled=not (model_provider and subject)
)

# validate empty value
if submit and not model_provider:
    st.info(t['select_model_info'])
    st.stop()
if submit and not subject:
    st.info(t['enter_subject_info'])
    st.stop()

if submit:
    # generate results
    with st.spinner(t['loading']):
        generator = Generator(model_provider, creativity)
        wiki_search, title, script = generator.generate_script(
            subject, video_length, lang, reference_prompt)
    # add generation history into session_state
    if 'history' not in st.session_state:
        st.session_state.history = []
    st.session_state.history.append({
        'subject': subject,
        'title': title,
        'time': datetime.now().strftime('%Y-%m-%d %H:%M')
    })
    # display the generated results
    st.success(t['success'])
    st.subheader(t['title_label'])
    st.write(title)
    st.subheader(t['script_label'])
    st.write(script)
    with st.expander(t['wiki_label']):
        st.info(wiki_search)

print(st.session_state)
