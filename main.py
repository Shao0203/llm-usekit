import streamlit as st
from utils import generate_script

st.title('🎬 视频脚本生成器~')

# 获取api密钥
with st.sidebar:
    api_key = st.text_input('请输入你的密钥', type='password')
    st.markdown('[获取OpenAI密钥](https://platform.openai.com/api-keys)')

# 获取视频主题，时长，创造力
subject = st.text_input('💡 请输入视频主题')
video_length = st.number_input(
    '⏰ 请输入视频时长（分钟）',  min_value=0.1, step=0.1, value=1.0)
creativity = st.slider('🌟 请输入视频创造力', min_value=0.0,
                       max_value=1.0, step=0.1, value=0.3)
submit = st.button('生成脚本', type='primary')

# 校验非空
if submit and not api_key:
    st.info('请输入你的API密钥')
    st.stop()
if submit and not subject:
    st.info('请输入视频主题')
    st.stop()

# 获取并展示脚本
if submit:
    with st.spinner('AI正在思考中 ~ 请稍等...'):
        wiki_search, title, script = generate_script(
            subject, video_length, creativity, api_key)
    st.success('视频脚本已生成！')

    st.subheader('🔥 标题：')
    st.write(title)
    st.subheader('📝 视频脚本：')
    st.write(script)
    with st.expander('维基百科相关信息 👀'):
        st.info(wiki_search)
