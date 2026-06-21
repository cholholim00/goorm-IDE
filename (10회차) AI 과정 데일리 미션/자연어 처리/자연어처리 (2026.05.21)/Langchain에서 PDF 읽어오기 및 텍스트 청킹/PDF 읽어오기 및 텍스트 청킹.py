import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

os.environ["OPENAI_API_KEY"] = "your-openai-api-key"

# 1. 고성능 PyMuPDFLoader를 이용한 PDF 파싱
pdf_path = "sample_document.pdf"
loader = PyMuPDFLoader(pdf_path)
raw_documents = loader.load()

# 2. 길이 단위 Splitter 정의 (글자 수 기준)
length_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    length_function=len
)
length_chunks = length_splitter.split_documents(raw_documents)

# 3. 의미 단위 Splitter 정의 (임베딩 유사도 기준)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
semantic_splitter = SemanticChunker(
    embeddings,
    breakpoint_threshold_type="percentile"
)
semantic_chunks = semantic_splitter.split_documents(raw_documents)

print(f"📋 원본 페이지 수: {len(raw_documents)}")
print(f"🧩 길이 기반 청크 개수: {len(length_chunks)}")
print(f"🧠 의미 기반 청크 개수: {len(semantic_chunks)}")