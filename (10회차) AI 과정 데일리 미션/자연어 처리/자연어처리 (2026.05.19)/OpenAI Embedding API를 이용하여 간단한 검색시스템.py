import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS

# 1. API 키 인증 및 환경 설정
os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# 2. 가상의 지식 베이스(도메인 문서) 정의
raw_documents = [
    "BridgeBoard 프로젝트는 PyTorch와 klue/roberta-large 모델을 활용해 한국어 감정을 7가지 카테고리로 분류하는 풀스택 플랫폼입니다.",
    "BART 모델은 양방향 인코더와 자동회귀 디코더를 결합하여 Denoising Autoencoder 방식으로 사전학습을 진행하는 Transformer 구조입니다.",
    "T5 모델은 모든 자연어 처리 태스크를 Text-to-Text 프레임워크로 처리하며, 입력 단에 'summarize: '와 같은 Prefix를 요구하는 특성이 있습니다.",
    "OpenAI의 GPT-5.5 모델은 1M 토큰 컨텍스트 윈도우를 지원하며 에이전트 태스크 및 복잡한 추론 연산에 최적화된 최신 플래그십 AI 모델입니다."
]

# 3. 임베딩 모델 정의 및 벡터 저장소(FAISS) 구축
# 가장 범용적이고 고성능인 text-embedding-3-large 혹은 text-embedding-3-small 활용
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vector_store = FAISS.from_texts(raw_documents, embedding=embeddings)

# 검색기(Retriever) 설정 (가장 유사한 문서 상위 2개 추출)
retriever = vector_store.as_retriever(search_kwargs={"k": 2})

# 4. GPT-5.5를 연동한 LangChain LLM 객체 생성
llm = ChatOpenAI(
    model="gpt-5.5",
    temperature=0.3
)

# 5. 시스템 지시사항이 포함된 프롬프트 템플릿 설계
rag_prompt = ChatPromptTemplate.from_messages([
    ("developer", "당신은 주어진 참고 컨텍스트(Context)만을 바탕으로 정직하게 답변하는 조수입니다. 만약 컨텍스트에서 정보를 찾을 수 없다면 지셔내지 말고 모른다고 답변하세요."),
    ("user", "Context:\n{context}\n\nQuestion: {question}")
])

# 6. 문서 포맷팅 함수 정의
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# 7. LCEL(LangChain Expression Language)을 활용한 체인 바인딩
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)

# 🏃‍♂️ RAG 시스템 테스트 실행
query = "GPT-5.5 모델의 특징과 컨텍스트 창 크기에 대해 설명해줘."
print(f"❓ 질문: {query}\n")

response = rag_chain.invoke(query)
print("🤖 RAG 기반 GPT-5.5 답변:\n", response)