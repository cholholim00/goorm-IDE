from transformers import AutoTokenizer, AutoModel

# 1. BGE-M3 토커나이저 및 모델 로드
bge_name = "BAAI/bge-m3"
bge_tokenizer = AutoTokenizer.from_pretrained(bge_name)
bge_model = AutoModel.from_pretrained(bge_name)

# 2. BGE-M3 전용 Dense 임베딩 추출 함수 정의
def get_bge_dense_embedding(texts):
    encoded = bge_tokenizer(texts, padding=True, truncation=True, max_length=512, return_tensors='pt')
    with torch.no_grad():
        outputs = bge_model(**encoded)
        # BGE-M3는 통상적으로 CLS 토큰([0]번 인덱스)을 대표 밀집 벡터로 활용합니다.
        dense_vecs = outputs.last_hidden_state[:, 0, :]
        # L2 정규화
        dense_vecs = torch.nn.functional.normalize(dense_vecs, p=2, dim=1)
    return dense_vecs.cpu().numpy()

# 3. 데이터 적재 및 HNSW 인덱스 빌드
bge_corpus_embeddings = get_bge_dense_embedding(corpus)
bge_dim = bge_corpus_embeddings.shape[1] # BGE-M3의 경우 1024 차원

bge_hnsw_index = faiss.IndexHNSWFlat(bge_dim, 16, faiss.METRIC_INNER_PRODUCT)
bge_hnsw_index.add(bge_corpus_embeddings)

# 4. BGE-M3 검색 테스트
bge_query = "눈 충혈되고 따가울 때 인공눈물 넣으면 되나"
bge_query_vector = get_bge_dense_embedding([bge_query])

scores, indices = bge_hnsw_index.search(bge_query_vector, k=1)
print(f"\n🚀 [BGE-M3 + FAISS HNSW 결과]")
print(f"질의어: {bge_query}")
print(f"가장 매칭되는 문서: {corpus[indices[0][0]]} (Score: {scores[0][0]:.4f})")