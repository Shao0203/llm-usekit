# def my_decorator(func):
#     def wrapper():
#         print('调用前...')
#         func()
#         print('调用后...')
#     return wrapper


# @my_decorator
# def say_hello():
#     print('Hello!')


# # say_hello = my_decorator(say_hello)
# say_hello()


# # ----------------------------------------------------------------------
# # from langchain.memory import ConversationBufferMemory

# # memory = ConversationBufferMemory(return_messages=True)

# # memory.save_context(
# #     {'input': '你好，我是亮亮'},
# #     {'output': '你好，亮亮!'}
# # )
# # memory.save_context(
# #     {'input': '我是一个程序员'},
# #     {'output': '好的，我记住了'}
# # )

# # print('#####', memory.load_memory_variables({}))


# # ----------------------------------------------------------------------
# # 推荐写法：PromptTemplate + LLM -> chain -> RunnableWithMessageHistory
# from langchain_openai import ChatOpenAI
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_core.runnables.history import RunnableWithMessageHistory
# from langchain_core.chat_history import InMemoryChatMessageHistory
# import os

# # 1) 简单的 in-memory session store（生产可换 DB/file）
# _store = {}


# def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
#     if session_id not in _store:
#         _store[session_id] = InMemoryChatMessageHistory()
#     return _store[session_id]


# # 2) LLM
# # llm = ChatOpenAI(model="gpt-3.5-turbo")
# # llm = ChatOpenAI(
# #     model='deepseek-chat',
# #     base_url='https://api.deepseek.com/v1',
# #     api_key=os.getenv('DEEPSEEK_API_KEY')
# # )

# llm = ChatOpenAI(
#     model='kimi-k2-0711-preview',
#     base_url='https://api.moonshot.cn/v1',
#     api_key=os.getenv('KIMI_API_KEY')
# )

# # 3) PromptTemplate：把 history 插进 prompt（MessagesPlaceholder）
# prompt = ChatPromptTemplate([
#     MessagesPlaceholder("history"),    # 自动占位：历史消息会被插入到这里
#     ("human", "{input}"),              # 模板把用户输入放在这里
# ])

# # 4) 把 prompt 串到 llm 上（prompt -> llm）
# chain = prompt | llm

# # 5) 包装成带历史的 runnable
# chat_runnable = RunnableWithMessageHistory(
#     chain,
#     get_session_history,
#     input_messages_key="input",     # 传入 object 的 key（我们用 "input"）
#     history_messages_key="history"  # 模板中 MessagesPlaceholder 使用的名字
# )


# # 6) 使用：必须在 config 里提供 session_id
# def get_chat_response(prompt_text, session_id="user1"):
#     result = chat_runnable.invoke(
#         {"input": prompt_text},
#         config={"configurable": {"session_id": session_id}},
#     )
#     return result.content  # 返回 LLM 的文本


# print('111:', get_chat_response('我是亮亮，你是什么模型?(回答20字以内)', session_id='bright'))
# print('222:', get_chat_response('我刚才的问题是什么？我的名字是什么？', session_id='bright'))
# print('333:', get_chat_response('我的名字是什么？', 'shao'))  # 换session_id, 无记忆


# # ----------------------------------------------------------------------流式输出
# import os
# from langchain_openai import ChatOpenAI
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_core.chat_history import InMemoryChatMessageHistory
# from langchain_core.runnables.history import RunnableWithMessageHistory

# # 存储不同 session 的聊天历史
# store = {}


# def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
#     """返回指定 session 的聊天历史，如果没有就新建"""
#     if session_id not in store:
#         store[session_id] = InMemoryChatMessageHistory()
#     return store[session_id]


# def get_chat_response_stream(prompt_text, session_id="user1"):
#     # 初始化 LLM
#     llm = ChatOpenAI(
#         model='kimi-k2-0711-preview',
#         base_url='https://api.moonshot.cn/v1',
#         api_key=os.getenv('KIMI_API_KEY')
#     )

#     # 定义 prompt
#     prompt = ChatPromptTemplate.from_messages([
#         MessagesPlaceholder(variable_name="history"),
#         ("human", "{input}"),
#     ])

#     # 串联 prompt 和 llm
#     chain = prompt | llm

#     # 包装成支持多轮对话的 runnable
#     chat_chain = RunnableWithMessageHistory(
#         chain,
#         get_session_history,
#         input_messages_key="input",
#         history_messages_key="history",
#     )

#     # 用 stream 实现流式输出
#     for chunk in chat_chain.stream(
#         {"input": prompt_text},
#         config={"configurable": {"session_id": session_id}},
#     ):
#         if chunk.content:
#             print(chunk.content, end="", flush=True)

#     print()  # 换行
# get_chat_response_stream("你好，我是Bob，请问如何学习大模型开发？?")
# get_chat_response_stream("上一个问题是什么?")
# get_chat_response_stream("你是否记得我是谁？")


# # ------ R A G old ----------------------------------------------------------------
# pip install pypdf wikipedia langchain-text-splitters langchain-huggingface
# sentence-transformers faiss-cpu

# import os
# from langchain_community.document_loaders import TextLoader
# from langchain_community.document_loaders import PyPDFLoader
# from langchain_community.document_loaders import Docx2txtLoader
# from langchain_community.document_loaders import WikipediaLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_openai import OpenAIEmbeddings
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain.chains import ConversationalRetrievalChain
# from langchain_openai import ChatOpenAI
# from langchain.memory import ConversationBufferMemory

# ----- 1. Load the data from data source -----

# load txt plain text file
# text_loader = TextLoader('./hello.txt')
# text_docs = text_loader.load()
# print(docs)

# load local pdf file
# pdf_loader = PyPDFLoader('./demo.pdf')
# pdf_docs = pdf_loader.load()
# print(pdf_docs)

# load local docx file
# docx_loader = Docx2txtLoader('./demo.docx')
# docx_docs = docx_loader.load()

# load online info from wikipedia
# wiki_loader = WikipediaLoader(query='长城', lang='zh', load_max_docs=3)
# wiki_docs = wiki_loader.load()
# print(wiki_docs)

# ----- 2. Split the data into chunks -----

# RecursiveCharacterTextSplitter   字符递归分割器(根据一句话结尾的符号进行分隔，比如! . \n)
# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=500,
#     chunk_overlap=40,
#     separators=['\n\n', '\n', '。', '！', '？', '，', '、', ', ', '']
# )
# split_loader = TextLoader('./demo.txt')
# split_docs = split_loader.load()
# texts = text_splitter.split_documents(split_docs)
# print('###', len(texts), texts)

# ----- 3. Embedding: text chunk -> vector -----

# embeddings_model = OpenAIEmbeddings(model='text-embedding-3-large', dimensions=1024)

# embeddings_model = HuggingFaceEmbeddings(
#     model_name="BAAI/bge-small-zh-v1.5",
#     model_kwargs={"device": "cpu"},
#     encode_kwargs={"normalize_embeddings": True}
# )

# embedded_result = embeddings_model.embed_documents(['Hello!', 'Hey bro'])
# print(len(embedded_result))
# print(embedded_result)
# print(len(embedded_result[0]))

# ----- 4. Store vectors into Vector database

# ... split documents texts + embedding model
# db = FAISS.from_documents(texts, embeddings_model)
# retriever = db.as_retriever()
# retrieved_docs = retriever.invoke('卢浮宫名字由来')
# print('####', retrieved_docs[0].page_content)
# retrieved_docs = retriever.invoke('卢浮宫在哪年被命名为中央艺术博物馆')
# print('@@@@', retrieved_docs[0].page_content)


# ----- 5. Retrieve related data + user's input = ConversationalRetrievalChain

# model = ChatOpenAI(model='gpt-3.5-turbo')
# retriever = db.as_retriever()
# memory = ConversationBufferMemory(
#     return_messages=True, memory_key='chat_history', output_key='answer')
# qa = ConversationalRetrievalChain.from_llm(
#     llm=model,
#     retriever=retriever,
#     memory=memory,
#     return_source_documents=True,
#     chain_type='map_reduce'     # refine / map_rerank
# )
# result = qa.invoke({'chat_history': memory, 'question': '卢浮宫名字的由来'})


# # ------ R A G - new ----------------------------------------------------------------
# import os
# from langchain_openai import ChatOpenAI
# from langchain_community.document_loaders import PyPDFLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_openai import OpenAIEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain.chains import ConversationalRetrievalChain
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain.memory import ConversationBufferMemory


# def retrieve_info(memory, question):
#     model = ChatOpenAI(
#         api_key=os.getenv('DEEPSEEK_API_KEY'),
#         base_url='https://api.deepseek.com/v1',
#         model='deepseek-chat'
#     )

#     # 1. Load file content
#     docs = PyPDFLoader('thesis.pdf').load()

#     # 2. Create text_splitter to split text into chunks
#     text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size=1000,
#         chunk_overlap=100,
#         separators=["\n", "。", "！", "？", "，", "、", ""]
#     )
#     texts = text_splitter.split_documents(docs)

#     # 3. Create embeddings_model    embed_model = OpenAIEmbeddings()
#     embed_model = HuggingFaceEmbeddings(
#         model_name="BAAI/bge-small-zh-v1.5",
#         model_kwargs={"device": "cpu"},
#         encode_kwargs={"normalize_embeddings": True}
#     )

#     # 4. Create vector store
#     db = FAISS.from_documents(texts, embed_model)
#     retriever = db.as_retriever()

#     # 5. Retrieve data
#     qa = ConversationalRetrievalChain.from_llm(
#         llm=model,
#         retriever=retriever,
#         memory=memory
#     )

#     response = qa.invoke({'chat_history': memory, 'question': question})
#     return response


# memory = ConversationBufferMemory(
#     return_messages=True,
#     memory_key='chat_history',
#     output_key='answer'
# )
# res = retrieve_info(memory, 'Transformer的论文标题是什么?')
# print('#####', res)
# res2 = retrieve_info(memory, '它的论文连接是什么?')
# print('$$$$$', res2)

# {'chat_history': [HumanMessage(content='Transformer的论文标题是什么?', additional_kwargs={}, response_metadata={}),
#                   AIMessage(content='Transformer的论文标题是《Attention Is All You Need》。', additional_kwargs={}, response_metadata={})],
#  'question': 'Transformer的论文标题是什么?',
#  'answer': 'Transformer的论文标题是《Attention Is All You Need》。'}


# # ========= Few shot chat message prompt template ===========
# from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
# from langchain_openai import ChatOpenAI
# import os

# llm = ChatOpenAI(model='kimi-k2-0711-preview',
#                  base_url='https://api.moonshot.cn/v1', api_key=os.getenv('KIMI_API_KEY'))

# example_prompt = ChatPromptTemplate.from_messages([
#     ('human',
#      '格式化以下客户信息: \n姓名 -> {customer_name}\n年龄 -> {customer_age}\n城市 -> {customer_city}'),
#     ('ai',
#      '##客户信息:\n- 客户姓名: {formatted_name}\n- 客户年龄: {formatted_age}\n- 客户所在地: {formatted_city}'),
# ])

# examples = [
#     {
#         "customer_name": "张三",
#         "customer_age": "27",
#         "customer_city": "长沙",
#         "formatted_name": "张三先生",
#         "formatted_age": "27周岁",
#         "formatted_city": "湖南省长沙市"
#     },
#     {
#         "customer_name": "李四",
#         "customer_age": "42",
#         "customer_city": "广州",
#         "formatted_name": "李四先生",
#         "formatted_age": "42周岁",
#         "formatted_city": "广东省广州市"
#     },
# ]

# few_shot_chat_prompt = FewShotChatMessagePromptTemplate(
#     example_prompt=example_prompt,
#     examples=examples,
# )

# final_prompt = ChatPromptTemplate.from_messages([
#     ('system', '你是一个智能问答助手，请模仿示例来回答问题.'),
#     few_shot_chat_prompt,
#     ('user', '{user_input}')
# ])

# response = (final_prompt | llm).invoke(
#     {'user_input': '格式化以下客户信息：\n姓名 -> 王五\n年龄 -> 31\n 城市 -> 郑州'}
# ).content

# print(response)

#  prompt(chat_history + rag + few_shot) - llm - parser
#  model - memroy - chain - retriever - agent


# ===== Langchain Agent: llm有限制，通过agent补齐模型能力短板
# ===== Agent 文本字数计算工具 ===== ReAct - Reason Action Observe Tool
# 模型提示词 需要包含上述信息内容(手动麻烦，用langchain hub 包含用户上传的用于各种目的的提示词)
# pip install langchainhub  (新版本langchain默认包含 不用额外安装)
# agent的运行需要：模型（大脑） + 提示词（告诉模型遵循ReAct） + 工具(自创和现成工具组合)
# 之后实际执行通过代理执行器agent_executor.invoke
# 2. 借用现有工具1，PAL: Program-Aided Language Models 程序辅助语言模型
# pip install langchain_experimental
# 3. 现有工具2分析csv文档，pip install tabulate pandas

import os
from langchain_openai import ChatOpenAI
from langchain.tools import BaseTool
from langchain import hub
from langchain.agents import create_structured_chat_agent, AgentExecutor
from langchain.memory import ConversationBufferMemory

from langchain_experimental import PythonREPLTool   # 2. python交互式解释器，deprecated
from langchain_experimental.agents.agent_toolkits import create_python_agent
from langchain_experimental.agents.agent_toolkits import create_csv_agent   # 3. csv agent
from langchain.tools import Tool    # 4. 整合多个tool


# 1 自建tool - 计算文字数量
class TextLengthTool(BaseTool):
    name: str = 'text length calculator'
    description: str = 'use this tool when calclulating the length of texts.'

    def _run(self, text):
        return len(text)


tools = [TextLengthTool()]

prompt = hub.pull('hwchase17/structured-chat-agent')

llm = ChatOpenAI(
    model='deepseek-chat',
    base_url='https://api.deepseek.com/v1',
    api_key=os.getenv('DEEPSEEK_API_KEY'),
    temperature=0,
)

agent = create_structured_chat_agent(
    llm=llm,
    prompt=prompt,
    tools=tools,    # 告诉agent有哪些工具可以使用
)

memory = ConversationBufferMemory(  # 如果想连续对话也可以加入记忆memroy
    memory_key='chat_history',
    return_messages=True
)

calc_agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,     # 在这里才是实际调用工具
    memory=memory,
    handle_parsing_errors=True,  # 把发生的错误作为观察，返还给大模型自行处理错误
    verbose=True,   # 详尽模式 - 打印出过程，比如选择哪歌工具
)

# response = calc_agent_executor.invoke({'input': '"君不见黄河之水天上来奔流到海不复回", 这句话的字数是多少？'})
# print('#####', response['output'])
# response = calc_agent_executor.invoke({'input': '地球上最高点在哪？'})   # 不调用工具，因为不是查字数
# print('@@@@@', response['output'])


# 2. 用现成的AI工具执行python代码 -- 废弃了
python_agent_executor = create_python_agent(
    llm=llm,
    tool=PythonREPLTool(),
    verbose=True,
    agent_executor_kwargs={'handle_parsing_errors': True},
)
# response = python_agent_executor.invoke({'input': '斐波那契数列第12个数字是什么？'})


# 3. 现成的分析csv文档
csv_agent_executor = create_csv_agent(
    llm=llm,
    path='house_price.csv',
    verbose=True,
    agent_executor_kwargs={'handle_parsing_errors': True},
    allow_dangerous_code=True,
)
# response = csv_agent_executor.invoke({'input': '数据集里所有房子的价格平均值是多少？'})
# print('$$$$$', response)

# 4. 组合调用多个工具 自建文字查数 + python解释器 + csv分析器
tools = [
    Tool(
        name='python代码工具',
        description='''当你需要借助python解释器时，使用这个工具。
        用自然语言把要求给这个工具，它会生成Python代码并返回代码执行的结果。''',
        func=python_agent_executor.invoke,
    ),
    Tool(
        name='csv分析工具',
        description='''当你需要回答有关house_price.csv文件的问题时，使用次工具。
        它接受完整的问题作为输入，在使用Pandas库计算后，返回答案。''',
        func=csv_agent_executor.invoke,
    ),
    TextLengthTool(),
]

agent = create_structured_chat_agent(
    llm=llm,
    prompt=prompt,
    tools=tools,
)

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    memory=memory,
    handle_parsing_errors=True,
    verbose=True,
)

# agent_executor.invoke({'input': '这里可以问问题关于1.查文字数；2.让python运行代码；3.处理csv})
