import torch
from FlagEmbedding import BGEM3FlagModel

# 1. 파인튜닝된 커스텀 BGE-M3 모델 로드
# use_fp16=True 설정을 통해 GPU 메모리를 절약하고 연산 속도를 높입니다.
model = BGEM3FlagModel('./fine_tuned_bge_m3', use_fp16=True)

# 2. 검색 대상 문서 코퍼스 (Passages)
corpus = [
    "안구건조증의 대표적인 증상으로 인공눈물을 자주 점안하고 실내 습도를 유지해야 합니다.",
    "시력 교정 수술인 라식과 라섹은 각막을 절삭하는 방식에서 차이가 있습니다.",
    "데코레이터 아래에 async def 키워드를 사용하여 라우트 함수를 작성합니다."
]

# 3. 코퍼스 임베딩 추출 (Dense, Lexical/Sparse, Multi-Vector 한 번에 계산)
corpus_embeddings = model.encode(
    corpus,
    return_dense=True,
    return_sparse=True,
    return_colbert_vecs=True
)

# 4. 질의문 입력 및 임베딩 추출
query = "눈이 너무 뻑뻑하고 이물감이 느껴집니다."
query_embedding = model.encode(
    query,
    return_dense=True,
    return_sparse=True,
    return_colbert_vecs=True
)

# 5. 각 메커니즘별 유사도 스코어 산출
# (1) Dense Score (내적 계산)
dense_scores = corpus_embeddings['dense_vecs'] @ query_embedding['dense_vecs']

# (2) Sparse/Lexical Score (어휘적 겹침 계산)
sparse_scores = []
for doc_lexical in corpus_embeddings['lexical_weights']:
    score = model.compute_lexical_matching_score(query_embedding['lexical_weights'], doc_lexical)
    sparse_scores.append(score)
sparse_scores = torch.tensor(sparse_scores)

# (3) Multi-Vector / ColBERT Score (토큰 레벨 후기 정렬 맥락 계산)
colbert_scores = []
for doc_colbert in corpus_embeddings['colbert_vecs']:
    score = model.compute_colbert_score(query_embedding['colbert_vecs'], doc_colbert)
    colbert_scores.append(score.item())
colbert_scores = torch.tensor(colbert_scores)

# 6. 다양한 가중치 조합을 통한 스코어 융합 (Hybrid Scoring)
# 태스크와 데이터 도메인에 맞게 alpha, beta, gamma 값을 튜닝할 수 있습니다.
alpha, beta, gamma = 0.4, 0.3, 0.3

hybrid_scores = (alpha * dense_scores) + (beta * sparse_scores) + (gamma * colbert_scores)

# 7. 최적의 결과 출력
best_doc_idx = torch.argmax(hybrid_scores).item()
print(f"--- 하이브리드 검색 결과 ---")
print(f"Query: {query}")
print(f"가장 유사한 문서: {corpus[best_doc_idx]}")
print(f"최종 융합 스코어: {hybrid_scores[best_doc_idx]:.4f}")