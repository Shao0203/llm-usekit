from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_huggingface import HuggingFaceEmbeddings
import os
import tempfile

# 禁止 Hugging Face 的 tokenizers 库并行 warning
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

# ========== 全局缓存，避免重复加载 ==========
_vectorstore = None
_retriever = None
_store = {}  # 存 session -> chat history


def _get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    """管理多轮对话历史"""
    if session_id not in _store:
        _store[session_id] = InMemoryChatMessageHistory()
    return _store[session_id]


def _init_vectorstore(uploaded_file):
    """初始化向量数据库（只执行一次）"""
    global _vectorstore, _retriever
    if _vectorstore is not None and _retriever is not None:
        return _vectorstore, _retriever

    # 1. 加载用户上传的文件内容
    # 临时保存文件
    tmp_path = 'temp.pdf'
    with open(tmp_path, 'wb') as tmp_file:
        tmp_file.write(uploaded_file.read())

    # with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
    #     tmp_file.write(uploaded_file.read())    # 把二进制内容写入临时文件
    #     tmp_path = tmp_file.name

    # 加载 PDF
    text_loader = PyPDFLoader(tmp_path)
    docs = text_loader.load()

    # 2. 分割文本
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        separators=['\n', '。', '！', '？', '，', '、', '']
    )
    texts = text_splitter.split_documents(docs)

    # 3. 向量化 + 向量数据库
    embedding = HuggingFaceEmbeddings(
        model_name='BAAI/bge-small-zh-v1.5',
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    _vectorstore = FAISS.from_documents(texts, embedding)
    _retriever = _vectorstore.as_retriever(search_kwargs={"k": 3})  # 默认 top-3
    return _vectorstore, _retriever


def get_rag_response(question: str, uploaded_file, session_id: str = 'user1') -> str:
    """基于 PDF 文档 + RAG 的对话问答，支持多轮聊天记忆"""

    # 初始化向量数据库（只在第一次调用时执行）
    _, retriever = _init_vectorstore(uploaded_file)

    # 初始化 LLM
    llm = ChatOpenAI(
        model='deepseek-chat',
        base_url='https://api.deepseek.com/v1',
        api_key=os.getenv('DEEPSEEK_API_KEY')
    )

    # Prompt 模板
    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder('chat_history'),
        ('system', '你是一个智能文档分析助手。请基于以下参考文档回答问题。\n\n{context}'),
        ('human', '{question}')
    ])

    # RAG 链
    rag_runnable = {
        "chat_history": lambda x: x.get("chat_history", []),
        "context": lambda x: '\n'.join([doc.page_content for doc in retriever.invoke(x["question"])]),
        "question": lambda x: x['question'],
    }

    rag_chain = rag_runnable | prompt | llm

    # 带历史记忆的 RAG
    rag_conversation = RunnableWithMessageHistory(
        runnable=rag_chain,
        get_session_history=_get_session_history,
        input_messages_key='question',
        history_messages_key='chat_history',
    )

    # 获取答案
    return rag_conversation.invoke(
        {'question': question},
        config={'configurable': {'session_id': session_id}}
    ).content


# ======= 测试 =======
# if __name__ == "__main__":
    # print("#####: ", get_rag_response("Transformer的论文标题是什么?"))
    # print("@@@@@: ", get_rag_response("Transformer的论文链接是什么?"))
