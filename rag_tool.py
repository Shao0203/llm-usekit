""" This module provides RAG functions to retrieve information from uploaded file. """

import os
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.memory import ConversationBufferMemory


def retrieve_info(memory, question):
    model = ChatOpenAI(
        api_key=os.getenv('DEEPSEEK_API_KEY'),
        base_url='https://api.deepseek.com/v1',
        model='deepseek-chat'
    )

    # 1. Load file content
    docs = PyPDFLoader('thesis.pdf').load()

    # 2. Create text_splitter to split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=50,
        separators=["\n", "。", "！", "？", "，", "、", ""]
    )
    texts = text_splitter.split_documents(docs)

    # 3. Create embeddings_model    embed_model = OpenAIEmbeddings()
    embed_model = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-zh-v1.5",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

    # 4. Create vector store
    db = FAISS.from_documents(texts, embed_model)
    retriever = db.as_retriever()

    # 5. Retrieve data
    qa = ConversationalRetrievalChain.from_llm(
        llm=model,
        retriever=retriever,
        memory=memory
    )

    response = qa.invoke({'chat_history': memory, 'question': question})
    return response


memory = ConversationBufferMemory(
    return_messages=True,
    memory_key='chat_history',
    output_key='answer'
)
res = retrieve_info(memory, 'Transformer的论文标题是什么?')
print('#####', res['question'])
print('#####', res['answer'])
res2 = retrieve_info(memory, '它的论文连接是什么?')
print('$$$$$', res2['question'])


{'chat_history': [HumanMessage(content='Transformer的论文标题是什么?', additional_kwargs={}, response_metadata={}), AIMessage(content='Transformer的论文标题是《Attention Is All You Need》。',
                                                                                                                      additional_kwargs={}, response_metadata={})], 'question': 'Transformer的论文标题是什么?', 'answer': 'Transformer的论文标题是《Attention Is All You Need》。'}
