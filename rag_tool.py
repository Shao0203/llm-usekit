""" This module provides functions to retrieve information from given data. """
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import WikipediaLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# pip install pypdf / wikipedia / langchain-text-splitters

# ----- loading the data from data source -----

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


# ----- split the data into chunks -----
# RecursiveCharacterTextSplitter   字符递归分割器(根据一句话结尾的符号进行分隔，比如! . \n)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=40,
    separators=['\n\n', '\n', '。', '！', '？', '，', '、', ', ', '']
)
split_loader = TextLoader('./demo.txt')
split_docs = split_loader.load()
texts = text_splitter.split_documents(split_docs)
print('###', len(texts), texts)
