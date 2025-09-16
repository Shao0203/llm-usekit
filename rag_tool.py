""" This module provides functions to retrieve information from given data. """
import os
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import WikipediaLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory

# pip install pypdf wikipedia langchain-text-splitters langchain-huggingface sentence-transformers faiss-cpu

# ----- 1. Load the data from data source -----

# text_loader = TextLoader('./hello.txt')
# docs = text_loader.load()
# print(docs)

# load local pdf file
# pdf_loader = PyPDFLoader('./demo.pdf')
# pdf_docs = pdf_loader.load()
# print(pdf_docs)

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
model = ChatOpenAI(model='gpt-3.5-turbo')
memory = ConversationBufferMemory(
    return_messages=True, memory_key='chat_history', output_key='answer')
qa = ConversationalRetrievalChain.from_llm(
    llm=model,
    retriever=retriever,
    memory=memory,
    return_source_documents=True,
    chain_type='map_reduce'     # refine / map_rerank
)
result = qa.invoke({'chat_history': memory, 'question': '卢浮宫名字的由来'})
