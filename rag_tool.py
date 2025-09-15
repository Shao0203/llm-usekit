""" This module provides functions to retrieve information from given data. """
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import WikipediaLoader


loader = TextLoader('./hello.txt')
docs = loader.load()
# print(docs)


# load local pdf file
pdf_loader = PyPDFLoader('./demo.pdf')
pdf_docs = pdf_loader.load()
# print(pdf_docs)


# load online info from wikipedia
wiki_loader = WikipediaLoader(query='长城', lang='zh', load_max_docs=3)
wiki_docs = wiki_loader.load()
# print(wiki_docs)
