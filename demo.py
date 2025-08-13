import streamlit as st


# 1. 异常处理增强
try:
    search_result = WikipediaAPIWrapper().run(subject)
except Exception as e:
    search_result = f"维基百科查询失败: {str(e)}" if lang == "中文" else f"Wikipedia search failed: {str(e)}"

# main.py 生成脚本时
try:
    wiki_search, title, script = generate_script(...)
except Exception as e:
    st.error(f"{t['error']}: {str(e)}")
    st.stop()


# 2. 流式输出体验
# utils.py 修改为流式响应
from langchain_core.runnables import RunnableLambda


def stream_script(chain_input):
    for chunk in script_chain.stream(chain_input):
        yield chunk.content


# main.py 中替换
if submit:
    with st.spinner(t['loading']):
        # ... 获取title等

        st.subheader(t['script_label'])
        script_placeholder = st.empty()
        full_script = ""
        for chunk in stream_script({...}):  # 传入参数
            full_script += chunk
            script_placeholder.markdown(full_script)


# 3. 历史记录功能
# main.py 顶部初始化
if 'history' not in st.session_state:
    st.session_state.history = []

# 生成成功后
if submit:
    # ...生成代码...
    st.session_state.history.append({
        'subject': subject,
        'title': title,
        'time': datetime.now().strftime("%Y-%m-%d %H:%M")
    })

# 侧边栏显示历史
with st.sidebar:
    st.subheader("📚 生成历史" if lang == "中文" else "📚 History")
    for idx, item in enumerate(st.session_state.history[::-1]):
        if st.button(f"{idx+1}. {item['title']}", key=f"hist_{idx}"):
            st.session_state.prefill = item  # 实现点击填充


# 4. 配置保存功能
# 在sidebar添加
remember = st.checkbox("记住我的配置" if lang == "中文" else "Remember my settings")

if remember:
    st.session_state.config = {
        'model_provider': model_provider,
        'lang': lang,
        'creativity': creativity
    }

# 页面初始化时
if 'config' in st.session_state:
    conf = st.session_state.config
    lang = conf['lang']
    model_provider = conf['model_provider']
    creativity = conf['creativity']


# 1. 异常处理增强 utils.py 修改generate_script函数开头
def generate_script(...):
    try:
        # 原有代码
    except Exception as e:
        error_msg = {
            "中文": f"生成失败: {str(e)}",
            "English": f"Generation failed: {str(e)}"
        }[lang]
        return None, error_msg, ""


# main.py 修改submit部分
if submit:
    with st.spinner(t['loading']):
        wiki_search, title, script = generate_script(...)
        if title is None:  # 判断是否出错
            st.error(script)  # 此时script是错误信息
            st.stop()


# 2. 流式输出体验
# utils.py 新增
def stream_script(subject, video_length, creativity, api_key, model_provider, lang):
    # ...保留原有model_options和title_template...
    title = title_chain.invoke(...).content

    # 流式生成脚本
    script_template = ...  # 原有模板
    for chunk in script_chain.stream({
        'lang': lang,
        'title': title,
        'duration': video_length,
        'wikipedia_search': search_result
    }):
        yield title, chunk.content


# main.py 修改
if submit:
    script_placeholder = st.empty()
    full_script = ""
    for title, chunk in stream_script(...):  # 调用流式函数
        if not full_script:  # 首次收到数据时显示标题
            st.subheader(t['title_label'])
            st.write(title)
            st.subheader(t['script_label'])
        full_script += chunk
        script_placeholder.markdown(full_script)


# 3. 快速历史记录（15分钟）
# main.py 在submit成功后添加
if submit and title:  # 确保成功生成
    if 'history' not in st.session_state:
        st.session_state.history = []
    st.session_state.history.append({
        'subject': subject,
        'title': title[:30] + "..."  # 缩略标题
    })

# 侧边栏显示
with st.sidebar:
    if 'history' in st.session_state:
        st.divider()
        st.write("📚 历史记录" if lang == "中文" else "📚 History")
        for item in st.session_state.history[-5:][::-1]:  # 显示最近5条
            st.button(item['title'], key=f"hist_{id(item)}")
