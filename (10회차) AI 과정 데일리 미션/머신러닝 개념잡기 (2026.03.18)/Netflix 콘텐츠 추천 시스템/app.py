import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 페이지 설정
st.set_page_config(page_title="Hana Netflix Recommender", layout="wide")

# 스타일 지정 (넷플릭스 느낌의 다크 모드)
st.markdown("""
    <style>
    .main { background-color: #141414; color: white; }
    .stButton>button { background-color: #E50914; color: white; border-radius: 5px; border: none; }
    h1 { color: #E50914; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv('dataset/netflix_titles.csv')
    features = ['director', 'cast', 'listed_in', 'description']
    for feature in features:
        df[feature] = df[feature].fillna('')
    # x 대신 df['description'] 처럼 직접 참조하도록 수정
    df['soup'] = (df['director'] + ' ') * 2 + (df['listed_in'] + ' ') * 2 + df['cast'] + ' ' + df['description']
    return df

df = load_data()

# 모델 학습 (캐싱하여 속도 최적화)
@st.cache_resource
def get_model(soup_series):
    tfidf = TfidfVectorizer(stop_words='english')
    matrix = tfidf.fit_transform(soup_series)
    sim = cosine_similarity(matrix, matrix)
    return sim

cosine_sim = get_model(df['soup'])
indices = pd.Series(df.index, index=df['title']).drop_duplicates()

# 메인 UI
st.image("https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg", width=200)
st.title("🎬 NETFLIX 콘텐츠 추천 서비스")
st.subheader("좋아하는 영화나 TV 쇼를 선택하세요!")

# 선택 상자
movie_list = df['title'].values
selected_movie = st.selectbox("콘텐츠 제목을 입력하거나 선택하세요", movie_list)

if st.button('추천 받기'):
    idx = indices[selected_movie]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:7] # 상위 6개만 표시
    
    movie_indices = [i[0] for i in sim_scores]
    recommendations = df.iloc[movie_indices]

    st.write(f"### '{selected_movie}'와(과) 비슷한 콘텐츠입니다:")
    
    # 넷플릭스 스타일 그리드 레이아웃 (3열씩)
    cols = st.columns(3)
    for i, (index, row) in enumerate(recommendations.iterrows()):
        with cols[i % 3]:
            st.image(f"https://picsum.photos/seed/{row['title']}/300/450", use_column_width=True)
            st.info(f"**{row['title']}**")
            st.caption(f"📅 {row['release_year']} | 📂 {row['listed_in']}")
            with st.expander("줄거리 보기"):
                st.write(row['description'])