import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------------------------------------------------
# 1. 페이지 설정 및 데이터 로드
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Game Market Intelligence", layout="wide", page_icon="🎮")

@st.cache_data
def load_data():
    # 업로드된 CSV 파일명과 일치해야 합니다.
    df = pd.read_csv('data/gaming_industry_trends.csv')
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("❌ 'gaming_industry_trends.csv' 파일을 찾을 수 없습니다. 같은 폴더에 파일을 넣어주세요.")
    st.stop()

# -----------------------------------------------------------------------------
# 2. 사이드바 (필터링)
# -----------------------------------------------------------------------------
st.sidebar.header("🔍 필터 옵션")

# 장르 필터
unique_genres = sorted(df['Genre'].unique())
selected_genres = st.sidebar.multiselect("장르 선택", unique_genres, default=unique_genres[:3])

# 플랫폼 필터
unique_platforms = sorted(df['Platform'].unique())
selected_platforms = st.sidebar.multiselect("플랫폼 선택", unique_platforms, default=unique_platforms)

# 출시 연도 슬라이더
min_year = int(df['Release Year'].min())
max_year = int(df['Release Year'].max())
selected_years = st.sidebar.slider("출시 연도 범위", min_year, max_year, (2010, max_year))

# 데이터 필터링 적용
filtered_df = df[
    (df['Genre'].isin(selected_genres)) &
    (df['Platform'].isin(selected_platforms)) &
    (df['Release Year'] >= selected_years[0]) &
    (df['Release Year'] <= selected_years[1])
]

# -----------------------------------------------------------------------------
# 3. 메인 대시보드 (KPI)
# -----------------------------------------------------------------------------
st.title("🎮 Gaming Industry Trends Dashboard")
st.markdown("### 주요 성과 지표 (Key Performance Indicators)")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

total_revenue = filtered_df['Revenue (Millions $)'].sum()
total_players = filtered_df['Players (Millions)'].sum()
avg_metacritic = filtered_df['Metacritic Score'].mean()
top_game = filtered_df.loc[filtered_df['Revenue (Millions $)'].idxmax()]['Game Title'] if not filtered_df.empty else "-"

kpi1.metric("총 매출 (Total Revenue)", f"${total_revenue:,.0f}M")
kpi2.metric("총 플레이어 수", f"{total_players:,.0f}M")
kpi3.metric("평균 메타크리틱 점수", f"{avg_metacritic:.1f}")
kpi4.metric("최고 매출 게임", top_game)

st.markdown("---")

# -----------------------------------------------------------------------------
# 4. 차트 시각화
# -----------------------------------------------------------------------------

# [Row 1] 장르별 매출 & 플랫폼별 플레이어 점유율
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 장르별 총 매출 (Revenue by Genre)")
    # 데이터 집계
    genre_rev = filtered_df.groupby('Genre')['Revenue (Millions $)'].sum().reset_index()
    fig_bar = px.bar(genre_rev, x='Genre', y='Revenue (Millions $)', 
                     color='Revenue (Millions $)', 
                     color_continuous_scale='Viridis',
                     text_auto='.2s')
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.subheader("🍰 플랫폼별 유저 분포 (Players by Platform)")
    platform_players = filtered_df.groupby('Platform')['Players (Millions)'].sum().reset_index()
    fig_pie = px.pie(platform_players, values='Players (Millions)', names='Platform', 
                     hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_pie, use_container_width=True)

# [Row 2] 연도별 트렌드 & 상관관계 분석
col3, col4 = st.columns(2)

with col3:
    st.subheader("📈 연도별 평균 동시접속자 추이")
    yearly_trend = filtered_df.groupby('Release Year')['Peak Concurrent Players'].mean().reset_index()
    fig_line = px.line(yearly_trend, x='Release Year', y='Peak Concurrent Players',
                       markers=True, line_shape='spline')
    fig_line.update_traces(line_color='#00CC96')
    st.plotly_chart(fig_line, use_container_width=True)

with col4:
    st.subheader("🧩 메타크리틱 점수 vs 매출 상관관계")
    fig_scatter = px.scatter(filtered_df, x='Metacritic Score', y='Revenue (Millions $)',
                             color='Genre', size='Players (Millions)',
                             hover_data=['Game Title'],
                             opacity=0.7)
    st.plotly_chart(fig_scatter, use_container_width=True)

# -----------------------------------------------------------------------------
# 5. 상세 데이터 보기
# -----------------------------------------------------------------------------
with st.expander("📂 원본 데이터 보기 (Click to expand)"):
    st.dataframe(filtered_df)