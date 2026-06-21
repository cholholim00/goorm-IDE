import numpy as np
import torch
import faiss
from sentence_transformers import SentenceTransformer

# 1. 문장 임베딩 모델 및 가상 지식 데이터 정의
embed_model = SentenceTransformer('jhgan/ko-sroberta-multitask')

corpus = [
    "안구건조증 치료에는 인공눈물 점안과 실내 습도 유지가 중요합니다.",
    "FastAPI에서 비동기 라우터 핸들러를 만들 때는 async def를 사용합니다.",
    "BGE-M3 모델은 Dense와 Sparse 검색 점수를 모두 융합할 수 있습니다.",
    "파이썬에서 가상환경을 만들 때는 Miniconda나 venv를 주로 활용합니다.",
    "FAISS는 페이스북에서 만든 초고속 벡터 유사도 검색 라이브러리입니다.",
    "라식 수술은 각막 절편을 만든 후 엑시머 레이저로 각막을 깎는 방식입니다."
]

# 2. 임베딩 추출 및 정규화
# (내적 연산인 Inner Product를 코사인 유사도처럼 사용하기 위해 L2 정규화를 수행합니다.)
corpus_embeddings = embed_model.encode(corpus, convert_to_numpy=True)
faiss.normalize_L2(corpus_embeddings)
dimension = corpus_embeddings.shape[1] # sroberta의 경우 768 차원

# ==========================================
# 3. 다양한 FAISS 인덱스 생성 및 적재
# ==========================================

# [Model A] IndexFlatIP (기본 전수 조사 방식)
index_flat = faiss.IndexFlatIP(dimension)
index_flat.add(corpus_embeddings)

# [Model B] IndexIVFFlat (클러스터 분할 검색 가속 방식)
nlist = 2  # 데이터가 수천~수만 건 이상일 때는 보통 100~1000 이상으로 설정합니다.
quantizer = faiss.IndexFlatIP(dimension)
index_ivf = faiss.IndexIVFFlat(quantizer, dimension, nlist, faiss.METRIC_INNER_PRODUCT)
index_ivf.train(corpus_embeddings)  # IVF는 클러스터 중심점을 잡는 사전 학습이 필수적입니다.
index_ivf.add(corpus_embeddings)
index_ivf.nprobe = 1                # 탐색을 수행할 근접 클러스터 수

# [Model C] IndexHNSWFlat (초고속 계층형 그래프 탐색 방식 - 강력 추천)
M = 16  # 각 노드가 가질 수 있는 최대 연결 링크 수
index_hnsw = faiss.IndexHNSWFlat(dimension, M, faiss.METRIC_INNER_PRODUCT)
index_hnsw.add(corpus_embeddings)

# ==========================================
# 4. 통합 검색 함수 및 테스트
# ==========================================
def search_engine(query, faiss_index, top_k=2):
    query_vector = embed_model.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(query_vector)

    # 유사도 점수(D)와 해당 문서의 인덱스 번호(I) 반환
    scores, indices = faiss_index.search(query_vector, top_k)

    print(f"\n🔮 [질의어]: {query}")
    for i in range(top_k):
        idx = indices[0][i]
        score = scores[0][i]
        if idx == -1: continue
        print(f"Top-{i+1} (유사도 점수: {score:.4f}): {corpus[idx]}")

# 실행 테스트
test_query = "FastAPI 웹 서버 코딩하는 방법 알려줘"
print("--- [1] IndexFlatIP 완전 탐색 결과 ---")
search_engine(test_query, index_flat)

print("\n--- [2] IndexHNSWFlat 그래프 탐색 결과 ---")
search_engine(test_query, index_hnsw)