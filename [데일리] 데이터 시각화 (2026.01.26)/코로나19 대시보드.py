import streamlit as st
import pandas as pd
import plotly.express as px

st.title("코로나19 실시간 대시보드")

# 샘플 데이터 (실제 프로젝트에선 API나 CSV 연동)
data = {
    'Date': pd.date_range(start='2023-01-01', periods=10),
    'Confirmed': [100, 150, 200, 180, 250, 300, 350, 400, 380, 450]
}
df = pd.DataFrame(data)

# 사이드바 설정
st.sidebar.header("필터 설정")
date_range = st.sidebar.date_input("날짜 범위 선택")

# 선 그래프 출력
fig = px.line(df, x='Date', y='Confirmed', title="일별 확진자 추이")
st.plotly_chart(fig)

# 요약 지표
st.metric(label="누적 확진자", value="450명", delta="70명")