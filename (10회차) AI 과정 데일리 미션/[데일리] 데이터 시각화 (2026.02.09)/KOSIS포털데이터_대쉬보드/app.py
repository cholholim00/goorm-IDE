import streamlit as st
import pandas as pd
import plotly.express as px  # 👈 인터랙티브 차트의 끝판왕

# 페이지 기본 설정 (브라우저 탭 이름 등)
st.set_page_config(
    page_title="KOSIS 인구 통계 대시보드",
    page_icon="🏙️",
    layout="wide"
)

st.title("🏙️ 주민등록 세대수 대시보드")

# 1. 데이터 로드
@st.cache_data
def load_data():
    try:
        # 파일이 없으면 에러 처리를 위해 try-except 사용
        df = pd.read_csv("행정구역_시군구_별_주민등록세대수_20260213012948.csv", encoding="cp949") 
    except:
        df = pd.read_csv("행정구역_시군구_별_주민등록세대수_20260213012948.csv", encoding="utf-8")
    return df

try:
    df = load_data()

    # 2. 데이터 전처리 (Wide -> Long)
    # 멜트(Melt) 함수로 가로로 긴 데이터를 세로로 변환
    df_melted = df.melt(id_vars=['행정구역(시군구)별'], var_name='연월', value_name='세대수')
    
    # 연월 데이터를 정렬하기 위해 문자열 처리 (예: '2025.10' -> 날짜형식으로 인식되게)
    # (여기서는 간단히 문자열 그대로 둡니다)

    # 3. 사이드바 구성
    with st.sidebar:
        st.header("⚙️ 컨트롤 패널")
        region_list = df['행정구역(시군구)별'].unique()
        selected_region = st.selectbox("지역 선택", region_list, index=0)
        st.info("KOSIS 국가통계포털 데이터 기반")

    # 4. 데이터 필터링
    region_data = df_melted[df_melted['행정구역(시군구)별'] == selected_region]

    # 5. 핵심 지표 (KPI) 보여주기 - 예쁜 박스 형태
    current = region_data.iloc[-1]['세대수']
    prev = region_data.iloc[-2]['세대수']
    diff = current - prev
    
    # 3단 컬럼으로 지표 배치
    col1, col2, col3 = st.columns(3)
    col1.metric("선택 지역", selected_region)
    col2.metric("최신 세대수", f"{current:,.0f} 세대")
    col3.metric("전월 대비 증감", f"{diff:,.0f} 세대", delta_color="normal")
    
    st.divider() # 구분선

    # 6. 탭(Tabs) 구조 도입 👈 여기가 핵심!
    tab1, tab2 = st.tabs(["📊 차트 분석", "📋 상세 데이터"])

    with tab1:
        st.subheader(f"{selected_region} 세대수 변화 추이")
        
        # Plotly로 고급 라인 차트 그리기
        fig = px.line(region_data, x='연월', y='세대수', markers=True, 
                      title=f"{selected_region} 월별 추이",
                      template="plotly_white") # 깔끔한 흰색 배경
        
        # 차트의 선 색상과 툴팁 커스터마이징
        fig.update_traces(line_color='#FF4B4B', line_width=3)
        
        # Streamlit에 Plotly 차트 표시 (컨테이너 폭에 맞춤)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("데이터 원본")
        # 데이터를 다운로드할 수 있게 버튼 제공
        csv = region_data.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 데이터 다운로드 (CSV)",
            data=csv,
            file_name=f"{selected_region}_data.csv",
            mime="text/csv"
        )
        st.dataframe(region_data, use_container_width=True)

except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
    st.warning("파일 이름이 '행정구역_시군구_별_주민등록세대수_20260213012948.csv'가 맞는지 확인해주세요.")