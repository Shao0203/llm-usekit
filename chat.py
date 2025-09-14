from langchain_openai import ChatOpenAI
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import os


# 用一个 dict 存储不同 session 的对话历史（放在函数外）
_store = {}


def _get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    """返回指定 session 的聊天历史，如果没有就新建"""
    if session_id not in _store:
        _store[session_id] = InMemoryChatMessageHistory()
    return _store[session_id]


def get_chat_response_stream(prompt_text, session_id='user1'):
    """根据历史聊天记录做出回答"""
    # 初始化 LLM
    llm = ChatOpenAI(
        model='deepseek-chat',
        base_url='https://api.deepseek.com/v1',
        api_key=os.getenv('DEEPSEEK_API_KEY')
    )

    # PromptTemplate：把 history 插进 prompt（MessagesPlaceholder）
    prompt = ChatPromptTemplate([
        MessagesPlaceholder('history'),   # 自动占位：历史消息会被插入到这里
        ('human', '{input}'),                           # 模板把用户输入放在这里
    ])

    # 把 prompt 和 llm 串起来
    chain = prompt | llm

    # 包装成支持多轮对话的 带历史的 runnable
    chat_chain = RunnableWithMessageHistory(
        chain,
        _get_session_history,
        input_messages_key='input',        # prompt 的 key
        history_messages_key='history',    # 历史的 key
    )

    # 获取一次对话的响应：必须在 config 里提供 session_id
    # response = chat_chain.invoke(
    #     {'input': prompt_text},
    #     config={'configurable': {'session_id': session_id}},
    # )
    # return response.content

    # 流式输出
    for chunk in chat_chain.stream(
        {'input': prompt_text},
        config={'configurable': {'session_id': session_id}}
    ):
        if chunk.content:   # 有内容才输出
            yield chunk.content

# # 示例对话
# print('111:', get_chat_response('我是Tom。你是谁?(回答20字以内)'))
# print('222:', get_chat_response('上一个问题是什么？我的名字是什么？'))
# print('333:', get_chat_response('你能记住我们之前的对话吗？'))
