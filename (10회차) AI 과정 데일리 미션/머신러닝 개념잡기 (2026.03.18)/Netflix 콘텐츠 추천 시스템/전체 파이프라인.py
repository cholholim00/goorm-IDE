# 데이터 로드부터 전처리, 유사도 계산, 그리고 최종 추천 함수까지 한 번에 실행할 수 있는 전체 파이프라인 코드

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. 데이터 로드 (Kaggle에서 받은 netflix_titles.csv 파일)
try:
    df = pd.read_csv('dataset/netflix_titles.csv')
    print("데이터 로드 성공!")
except FileNotFoundError:
    print("파일을 찾을 수 없습니다. 경로를 확인해주세요.")

# 2. 데이터 전처리 (결측치 처리 및 텍스트 통합)
# 추천에 영향을 줄 수 있는 주요 특성들을 선택합니다.
features = ['director', 'cast', 'listed_in', 'description']

# 결측치를 빈 문자열로 대체
for feature in features:
    df[feature] = df[feature].fillna('')

# 모든 텍스트 데이터를 하나의 'soup'으로 합치는 함수
def create_soup(x):
    return x['director'] + ' ' + x['cast'] + ' ' + x['listed_in'] + ' ' + x['description']

df['soup'] = df.apply(create_soup, axis=1)

# 3. TF-IDF 벡터화
# 영문 불용어(the, a, is 등)를 제거하고 텍스트를 수치 행렬로 변환합니다.
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['soup'])

# 4. 코사인 유사도 계산
# 모든 콘텐츠 간의 유사도 거리를 계산합니다. (메모리 사용량 주의)
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# 영화 제목을 입력하면 해당 인덱스를 빠르게 찾기 위한 매핑 테이블
indices = pd.Series(df.index, index=df['title']).drop_duplicates()

# 5. 추천 함수 정의
def get_recommendations(title, cosine_sim=cosine_sim):
    # 입력한 제목이 데이터에 있는지 확인
    if title not in indices:
        return "데이터셋에 해당 제목이 없습니다."
    
    # 해당 영화의 인덱스 가져오기
    idx = indices[title]

    # 모든 영화와의 유사도를 가져와 (인덱스, 유사도) 형태로 저장
    sim_scores = list(enumerate(cosine_sim[idx]))

    # 유사도(x[1])를 기준으로 내림차순 정렬
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # 자기 자신을 제외한 상위 10개 영화 선택
    sim_scores = sim_scores[1:11]

    # 선택된 10개 영화의 인덱스 추출
    movie_indices = [i[0] for i in sim_scores]

    # 결과 출력 (제목, 장르, 개봉연도 포함 가능)
    return df[['title', 'listed_in', 'release_year']].iloc[movie_indices]

# 6. 실행 테스트
print("\n--- 'Stranger Things'과 비슷한 추천 목록 ---")
print(get_recommendations('Stranger Things'))

print("\n--- 'Inception'과 비슷한 추천 목록 ---")
print(get_recommendations('Inception'))