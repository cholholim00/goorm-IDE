# ============================================
# 📦 필요한 라이브러리
# ============================================
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

# ============================================
# 🎨 페이지 설정
# ============================================
st.set_page_config(
    page_title="코로나19 데이터 분석 종합 대시보드",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main {padding: 0rem 1rem;}
    .stMetric {
        background-color: #1e1e1e;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #333;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================
# 📂 데이터 로딩
# ============================================
@st.cache_data
def load_daily_data():
    """일별 발생 데이터 로드"""
    df = pd.read_csv('일별_발생_성별_통합.csv', encoding='utf-8-sig')
    df['날짜'] = pd.to_datetime(df['날짜'])
    df['new_cases'] = df['국내발생'] + df['해외유입']
    df['new_deaths'] = df['사망']
    df['cum_cases'] = df['new_cases'].cumsum()
    df['cum_deaths'] = df['new_deaths'].cumsum()
    df['date'] = df['날짜']
    return df

@st.cache_data
def load_regional_data():
    """지역별 데이터 로드"""
    df = pd.read_csv('시군구별_월별_확진자_사망_발생현황_통합.csv', encoding='utf-8-sig')
    df['날짜'] = pd.to_datetime(df['날짜'])
    return df

@st.cache_data
def load_vaccination_data():
    """백신 접종 데이터 로드"""
    df = pd.read_csv('예방접종_통계_통합_현황_통합.csv', encoding='utf-8-sig')
    df['날짜'] = pd.to_datetime(df['날짜'])
    return df

# 데이터 로딩 실행
try:
    daily_df = load_daily_data()
    regional_df = load_regional_data()
    vaccination_df = load_vaccination_data()
except Exception as e:
    st.error(f"❌ 데이터 로딩 오류: {e}")
    st.info("💡 CSV 파일들이 같은 폴더에 있는지 확인해주세요!")
    st.stop()

# ============================================
# 🎯 사이드바 필터
# ============================================
st.sidebar.title("🔍 데이터 필터")
st.sidebar.markdown("---")

st.sidebar.subheader("📅 분석 기간")
min_date = daily_df['date'].min().date()
max_date = daily_df['date'].max().date()

start_date = st.sidebar.date_input("시작 날짜", value=min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("종료 날짜", value=max_date, min_value=min_date, max_value=max_date)

st.sidebar.markdown("---")
st.sidebar.subheader("📍 지역")
all_regions = sorted(regional_df['시도명'].unique())
selected_regions = st.sidebar.multiselect("시도 선택", options=all_regions, default=all_regions[:5])

filtered_daily = daily_df[
    (daily_df['date'] >= pd.to_datetime(start_date)) & 
    (daily_df['date'] <= pd.to_datetime(end_date))
]

filtered_regional = regional_df[
    (regional_df['시도명'].isin(selected_regions)) &
    (regional_df['날짜'] >= pd.to_datetime(start_date)) & 
    (regional_df['날짜'] <= pd.to_datetime(end_date))
]

st.sidebar.markdown("---")
st.sidebar.info(f"""
**📊 필터 결과**
- 기간: {(pd.to_datetime(end_date) - pd.to_datetime(start_date)).days + 1}일
- 지역: {len(selected_regions)}개
- 데이터: {len(filtered_daily):,}건
""")

# ============================================
# 🏠 메인 헤더
# ============================================
st.title("🦠 코로나19 데이터 분석 종합 대시보드")

# ============================================
# 📊 KPI 카드
# ============================================
st.subheader("📈 핵심 지표")

if len(filtered_daily) > 0:
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_cases = filtered_daily['cum_cases'].iloc[-1]
    total_deaths = filtered_daily['cum_deaths'].iloc[-1]
    latest_new = filtered_daily['new_cases'].iloc[-1]
    avg_new = filtered_daily['new_cases'].mean()
    fatality = (total_deaths / total_cases * 100) if total_cases > 0 else 0
    
    with col1:
        st.metric("🧮 총 누적 확진자", f"{total_cases:,.0f} 명", f"+{latest_new:,.0f}")
    
    with col2:
        st.metric("☠️ 총 누적 사망자", f"{total_deaths:,.0f} 명", f"{fatality:.2f}%")
    
    with col3:
        st.metric("📅 일평균 확진자", f"{avg_new:,.0f} 명")
    
    with col4:
        male_total = filtered_daily['남자'].sum()
        female_total = filtered_daily['여자'].sum()
        male_pct = (male_total/(male_total+female_total)*100) if (male_total+female_total)>0 else 0
        st.metric("👨 남성 비율", f"{male_pct:.1f}%")
    
    with col5:
        female_pct = 100 - male_pct
        st.metric("👩 여성 비율", f"{female_pct:.1f}%")

st.markdown("---")

# ============================================
# 📊 탭 구성
# ============================================
tab1, tab2, tab3 = st.tabs(["📈 종합 추이", "🗺️ 지역별 분석", "👥 성별 분석"])

# ============================================
# 탭 1: 종합 추이
# ============================================
with tab1:
    st.header("📊 국내 코로나19 확진 및 사망 추이")
    
    subtab1, subtab2 = st.tabs(["일일/누적 통합 지표", "확진자/사망자 추이"])
    
    # === 서브탭 1: 일일/누적 통합 지표 ===
    with subtab1:
        st.subheader("일일/누적 확진자 및 사망자 통합 추이")
        
        fig_a = go.Figure()
        
        fig_a.add_trace(go.Scatter(
            x=filtered_daily['date'], y=filtered_daily['new_cases'],
            mode='lines', name='● 일일 확진자', line=dict(color='#FF6B6B', width=2)
        ))
        
        fig_a.add_trace(go.Scatter(
            x=filtered_daily['date'], y=filtered_daily['new_deaths'],
            mode='lines', name='● 일일 사망자', line=dict(color='#FF4757', width=2)
        ))
        
        fig_a.add_trace(go.Scatter(
            x=filtered_daily['date'], y=filtered_daily['cum_cases'],
            mode='lines', name='● 누적 확진자', line=dict(color='#5F27CD', width=2)
        ))
        
        fig_a.add_trace(go.Scatter(
            x=filtered_daily['date'], y=filtered_daily['cum_deaths'],
            mode='lines', name='● 누적 사망자', line=dict(color='#341F97', width=2)
        ))
        
        fig_a.update_layout(
            title="대한민국 코로나19 전국 확진자 및 사망자 통합 추이",
            height=600, template='plotly_dark',
            margin=dict(l=60, r=60, t=100, b=60),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            xaxis_title="날짜", yaxis_title="건수", hovermode='x unified'
        )
        
        st.plotly_chart(fig_a, use_container_width=True)
    
    # === 서브탭 2: 확진자/사망자 추이 ===
    with subtab2:
        st.subheader("신규 확진자 vs 사망자 비교")
        
        fig_b = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig_b.add_trace(
            go.Scatter(x=filtered_daily['date'], y=filtered_daily['new_cases'],
                      name='신규 확진자', mode='lines', line=dict(color='#48dbfb', width=2)),
            secondary_y=False
        )
        
        fig_b.add_trace(
            go.Scatter(x=filtered_daily['date'], y=filtered_daily['new_deaths'],
                      name='신규 사망자', mode='lines', line=dict(color='#ff6348', width=2)),
            secondary_y=True
        )
        
        fig_b.update_layout(
            title="국내 신규 확진자/사망자 추이", title_font_size=20,
            template='plotly_dark', height=600,
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
            hovermode="x unified"
        )
        
        fig_b.update_xaxes(title_text="날짜", showgrid=False)
        fig_b.update_yaxes(title_text="확진자 수", secondary_y=False, showgrid=False)
        fig_b.update_yaxes(title_text="사망자 수", secondary_y=True, showgrid=False)
        
        st.plotly_chart(fig_b, use_container_width=True)

# ============================================
# 탭 2: 지역별 분석
# ============================================
with tab2:
    st.header("🗺️ 지역별 확진자 분석")
    
    regional_confirmed = filtered_regional[filtered_regional['유형'] == '확진자']
    regional_summary = regional_confirmed.groupby('시도명')['값'].sum().reset_index()
    regional_summary = regional_summary.sort_values('값', ascending=False)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_region = px.bar(
            regional_summary, x='시도명', y='값',
            title='시도별 총 확진자 수', labels={'시도명': '지역', '값': '확진자 수'},
            color='값', color_continuous_scale='Reds', text='값'
        )
        fig_region.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        fig_region.update_layout(template='plotly_dark', height=500)
        st.plotly_chart(fig_region, use_container_width=True)
    
    with col2:
        fig_pie = px.pie(regional_summary, values='값', names='시도명', title='지역별 비율')
        fig_pie.update_layout(template='plotly_dark', height=500)
        st.plotly_chart(fig_pie, use_container_width=True)

# ============================================
# 탭 3: 성별 분석
# ============================================
with tab3:
    st.header("⚥ 성별 확진자 비교")
    
    gender_data = pd.DataFrame({
        '성별': ['남자', '여자'],
        '확진자': [filtered_daily['남자'].sum(), filtered_daily['여자'].sum()]
    })
    
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        fig_gender = px.pie(
            gender_data, values='확진자', names='성별', title='성별 확진자 비율',
            color='성별', color_discrete_map={'남자': '#3498db', '여자': '#e91e63'}
        )
        fig_gender.update_layout(template='plotly_dark')
        st.plotly_chart(fig_gender, use_container_width=True)
    
    with col_g2:
        fig_bar = px.bar(
            gender_data, x='성별', y='확진자', title='성별 확진자 수',
            color='성별', color_discrete_map={'남자': '#3498db', '여자': '#e91e63'}, text='확진자'
        )
        fig_bar.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        fig_bar.update_layout(template='plotly_dark')
        st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")