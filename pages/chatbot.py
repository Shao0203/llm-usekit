import streamlit as st
from utils.chat import get_chat_response_stream


left_column, right_column = st.columns([4, 1])
left_column.title('💬智能聊天助手')
submit = right_column.button('清空聊天')
# 点击按钮时，清空聊天并切换到新的 session_id
if submit:
    st.session_state.messages = []
    st.session_state.session_counter += 1
    st.session_state.session_id = f'session_{st.session_state.session_counter}'

# 初始化 session_id 和计数器
if 'session_id' not in st.session_state:
    st.session_state.messages = [{'role': 'ai', 'content': '你好, 我是你的AI助手!'}]
    st.session_state.session_counter = 1
    st.session_state.session_id = f'session_{st.session_state.session_counter}'

for message in st.session_state.messages:
    st.chat_message(message['role']).write(message['content'])

prompt_text = st.chat_input()

if prompt_text:
    st.session_state.messages.append({'role': 'human', 'content': prompt_text})
    st.chat_message('human').write(prompt_text)

    # 流式输出
    with st.chat_message('ai'):
        placeholder = st.empty()  # 占位符
        placeholder.markdown("🤔 AI is thinking...")  # 初始提示

        response_text = ""  # 累积AI的回复
        for chunk in get_chat_response_stream(prompt_text, st.session_state.session_id):
            response_text += chunk
            placeholder.markdown(response_text)  # 动态替换内容

    # 最终完整的内容保存下来
    st.session_state.messages.append({'role': 'ai', 'content': response_text})

    # 一次性等待完整回复
    # with st.spinner('AI is thinking...'):
    #     response = get_chat_response(prompt_text, st.session_state.session_id)
    # st.session_state.messages.append({'role': 'ai', 'content': response})
    # st.chat_message('ai').write(response)
