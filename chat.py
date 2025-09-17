from langchain_openai import ChatOpenAI
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import os


# 用一个 dict 存储不同 session 的对话历史（放在函数外）
# InMemoryChatMessageHistory 里通常存的是 BaseMessage 的对象（LangChain 的消息类）
# {"session_1": InMemoryChatMessageHistory([HumanMessage, AIMessage, ...]),
#  "session_2": InMemoryChatMessageHistory([HumanMessage, AIMessage, ...]),}
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

    # 创建模版：把RunnableWithMessageHistory里history 插进 prompt（MessagesPlaceholder）
    prompt = ChatPromptTemplate([
        MessagesPlaceholder('history'),   # 自动占位：历史消息会被插入到这里
        ('human', '{user_input}'),        # 模板把用户输入放在这里
    ])

    # 把 prompt 和 llm 串起来
    chain = prompt | llm

    # 目标：包装成支持多轮对话的 带历史的 runnable, 把“历史消息”拿到并注入到chain的输入里 然后再执行这个chain
    """
    包装器（RunnableWithMessageHistory）在内部做了哪些事:
    1. 从 config 中读出 session_id；
    2. 调用_get_session_history(session_id)，得到history_store（InMemoryChatMessageHistory 实例）；
    3. 从 history_store 取出消息列表（通常是 history_store.messages 或类似接口，返回 BaseMessage 的列表）；
    4. 构造要传给内部 chain 的输入字典，例如 {'history': [..messages..], 'user_input': prompt_text}；
    5. 调用内部 chain.invoke 或 chain.stream，把包含 history 的输入交给 prompt+LLM 去运行；
    6. 在内部运行结束后，包装器通常还会把新的用户消息和AI回复追加回history_store（即写入记忆），以便下一轮使用。
    """

    chat_runnable = RunnableWithMessageHistory(
        chain,
        _get_session_history,              # 调用函数 传入session_id 拿到历史记录
        input_messages_key='user_input',   # prompt的key, 表示用户的“本轮输入/新消息”
        history_messages_key='history',    # 把上面拿到的历史消息 放到key history里, 传给Prompt
    )

    # 完整响应：必须在 config 里提供 session_id
    # response = chat_runnable.invoke(
    #     {'user_input': prompt_text},
    #     config={'configurable': {'session_id': session_id}},
    # )
    # return response.content

    # 流式输出：必须在 config 里提供 session_id
    for chunk in chat_runnable.stream(
        {'user_input': prompt_text},
        config={'configurable': {'session_id': session_id}}
    ):
        if chunk.content:   # 有内容才输出
            yield chunk.content
