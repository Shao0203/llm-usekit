from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_huggingface import HuggingFaceEmbeddings
import os

# 禁止Hugging Face 的 tokenizers 库并行的 warning
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

# 创建一个dict {} 用来存储不同session的聊天记录chat_history
_store = {}  # 存 session -> chat history


def _get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in _store:
        _store[session_id] = InMemoryChatMessageHistory()
    return _store[session_id]


def get_rag_response(question: str, session_id: str = 'user1') -> str:
    """基于 PDF 文档 + RAG 的对话问答，支持多轮聊天记忆"""

    # 1. 初始化 LLM
    llm = ChatOpenAI(model='deepseek-chat', base_url='https://api.deepseek.com/v1',
                     api_key=os.getenv('DEEPSEEK_API_KEY'))

    # 2. 加载 PDF
    text_loader = PyPDFLoader('thesis.pdf')
    docs = text_loader.load()

    # 3. 分割文本
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=100, separators=['\n', '。', '！', '？', '，', '、', ''])
    texts = text_splitter.split_documents(docs)

    # 4. 向量化 + 向量数据库
    embedding = HuggingFaceEmbeddings(
        model_name='BAAI/bge-small-zh-v1.5',
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    vectorstore = FAISS.from_documents(texts, embedding)
    retriever = vectorstore.as_retriever()

    # 5. Prompt 模板（带context，即文档里检索出来的内容 retriever.invoke -> context）
    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder('chat_history'),
        ('system', '你是一个智能文档分析助手。请基于以下参考文档回答问题。\n\n{context}'),
        ('human', '{question}')
    ])

    # 6. 定义 RAG 链
    rag_chain = (
        {
            "context": lambda x: '\n\n'.join([doc.page_content for doc in retriever.invoke(x["question"])]),
            "question": lambda x: x['question'],
            "chat_history": lambda x: x.get("chat_history", [])
        }
        | prompt
        | llm
    )

    # 7. 包装成带多轮记忆的 runnable
    conversational_rag = RunnableWithMessageHistory(
        runnable=rag_chain,
        get_session_history=_get_session_history,
        input_messages_key='question',
        history_messages_key='chat_history',
    )

    # 8. 调用 runnable 获取回答
    response = conversational_rag.invoke(
        {'question': question},
        config={'configurable': {'session_id': session_id}}
    )

    return response.content


# 8. 测试问答
print('#####: ', get_rag_response('Transformer的论文标题和论文链接分别是什么?'))
