from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain.prompts import ChatPromptTemplate

# 1. 创建 LLM
llm = ChatOpenAI(model="gpt-3.5-turbo")

# 2. 加载 PDF
docs = PyPDFLoader("thesis.pdf").load()

# 3. 分割文本
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(docs)

# 4. 向量化 + 向量数据库
embedding = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(texts, embedding)
retriever = vectorstore.as_retriever()

# 5. Prompt 模板（带 context）
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个有帮助的学术助手。请基于以下参考文档回答问题。\n\n{context}"),
    ("human", "{question}")
])

# 6. 定义 RAG 链
rag_chain = (
    {"context": retriever, "question": lambda x: x["question"]}
    | prompt
    | llm
)

# 7. 使用 RunnableWithMessageHistory 管理对话记忆
store = {}  # 存 session -> chat history


def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


conversational_rag = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="chat_history",
)

# 8. 测试问答
config = {"configurable": {"session_id": "user_123"}}

response1 = conversational_rag.invoke(
    {"question": "Transformer的论文标题是什么?"}, config=config)
print("#####", response1.content)

response2 = conversational_rag.invoke(
    {"question": "它的论文链接是什么?"}, config=config)
print("$$$$$", response2.content)
