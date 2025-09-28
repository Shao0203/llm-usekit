import streamlit as st
import json


def render_sidebar():
    """Render the sidebar for each page"""

    # Initialize st.session_state with lang and model_provider only for the first time
    if "lang" not in st.session_state:
        st.session_state.lang = "Chinese"
    if "model_provider" not in st.session_state:
        st.session_state.model_provider = "DeepSeek"

    # multi-languages dictionary
    with open('texts.json', 'r', encoding='utf-8') as f:
        TEXTS = json.load(f)

    with st.sidebar:
        lang = st.radio(
            label='语言 / Language',
            options=['Chinese', 'English'],
            index=0 if st.session_state.lang == 'Chinese' else 1,
        )

        t = TEXTS[lang]  # define current language dictionary

        model_provider = st.selectbox(
            label=t['select_model'],
            options=['DeepSeek', 'Kimi', 'Qwen', 'OpenAI'],
            index=['DeepSeek', 'Kimi', 'Qwen', 'OpenAI'].index(
                st.session_state.model_provider),
        )

        # Set session_state values for lang and model to share among pages
        if lang:
            st.session_state.lang = lang
        if model_provider:
            st.session_state.model_provider = model_provider

        st.subheader(t['gen_history'])

        if 'history' in st.session_state:
            for idx, item in enumerate(st.session_state.history[::-1][:5]):
                st.caption(
                    f"{idx+1}: {item['subject']} - {item['title'][:50]}...")

    return lang, t, model_provider

    # st.divider()
    # with st.expander(t['apply_api_key']):
    #     st.markdown(t['get_openai_key'])
    #     st.markdown(t['get_deepseek_key'])
    #     st.markdown(t['get_kimi_key'])
    #     st.markdown(t['get_qwen_key'])
