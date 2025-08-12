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
