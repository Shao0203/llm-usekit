import streamlit as st
from utils import generate_script

# multi-languages dictionary
TEXTS = {
    '中文': {
        'title': '🎬 视频脚本生成器',
        'select_model': '请选择模型',
        'enter_api_key': '请输入你的密钥',
        'get_openai_key': '[获取OpenAI密钥](https://platform.openai.com/api-keys)',
        'get_deepseek_key': '[获取DeepSeek密钥](https://platform.deepseek.com/api-keys)',
        'get_kimi_key': '[获取Kimi密钥](https://platform.moonshot.cn/api-keys)',
        'subject': '💡 请输入视频主题',
        'video_length': '⏰ 请输入视频时长（分钟）',
        'creativity': '🌟 请输入视频创造力',
        'generate_script': '生成脚本',
        'select_model_info': '请选择模型',
        'enter_api_key_info': '请输入你的API密钥',
        'enter_subject_info': '请输入视频主题',
        'loading': 'AI正在思考中 ~ 请稍等...',
        'success': '视频脚本已生成！',
        'title_label': '🔥 标题：',
        'script_label': '📝 视频脚本：',
        'wiki_label': '维基百科相关信息 👀'
    },
    'English': {
        'title': '🎬 Video Script Generator',
        'select_model': 'Select a Model',
        'enter_api_key': 'Enter your API key',
        'get_openai_key': '[Get OpenAI API Key](https://platform.openai.com/api-keys)',
        'get_deepseek_key': '[Get DeepSeek API Key](https://platform.deepseek.com/api-keys)',
        'get_kimi_key': '[Get Kimi API Key](https://platform.moonshot.cn/api-keys)',
        'subject': '💡 Enter the video topic',
        'video_length': '⏰ Enter video length (minutes)',
        'creativity': '🌟 Enter creativity level',
        'generate_script': 'Generate Script',
        'select_model_info': 'Please select a model.',
        'enter_api_key_info': 'Please enter your API key.',
        'enter_subject_info': 'Please enter a video topic.',
        'loading': 'AI is thinking... Please wait...',
        'success': 'Video script generated!',
        'title_label': '🔥 Title:',
        'script_label': '📝 Video Script:',
        'wiki_label': 'Wikipedia Related Info 👀'
    }
}

# sidebar
with st.sidebar:
    lang = st.radio(label='', options=['中文', 'English'])
    t = TEXTS[lang]  # define current language dictionary

    st.divider()
    model_provider = st.selectbox(
        t['select_model'], ['OpenAI', 'DeepSeek', 'KIMI'], index=None)
    api_key = st.text_input(t['enter_api_key'], type='password')
    st.divider()
    st.markdown(t['get_openai_key'])
    st.markdown(t['get_deepseek_key'])
    st.markdown(t['get_kimi_key'])

# page title
st.title(t['title'])

# main content
subject = st.text_input(t['subject'])
video_length = st.number_input(
    t['video_length'], min_value=0.1, step=0.1, value=1.0)
creativity = st.slider(t['creativity'], min_value=0.0,
                       max_value=1.0, step=0.1, value=0.3)
submit = st.button(t['generate_script'], type='primary')

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

# generate script
if submit:
    with st.spinner(t['loading']):
        wiki_search, title, script = generate_script(
            subject, video_length, creativity, api_key, model_provider, lang
        )
    st.success(t['success'])

    st.subheader(t['title_label'])
    st.write(title)
    st.subheader(t['script_label'])
    st.write(script)
    with st.expander(t['wiki_label']):
        st.info(wiki_search)
