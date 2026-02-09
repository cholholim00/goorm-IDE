import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os

# 1. 페이지 설정
st.set_page_config(
    page_title="대한민국 코로나19 통합 상황실",
    page_icon="🇰🇷",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { height: 50px; font-weight: bold; border-radius: 5px; }
    .stTabs [data-baseweb="tab"]:nth-of-type(1)[aria-selected="true"] { background-color: #1E88E5; color: white; }
    .stTabs [data-baseweb="tab"]:nth-of-type(2)[aria-selected="true"] { background-color: #43A047; color: white; }
    .stTabs [data-baseweb="tab"]:nth-of-type(3)[aria-selected="true"] { background-color: #FB8C00; color: white; }
    </style>
""", unsafe_allow_html=True)

# 2. 데이터 로드
@st.cache_data
def load_data():
    base_path = os.path.dirname(os.path.abspath(__file__))
    daily_path = os.path.join(base_path, 'data', 'daily_covid_data.csv')
    region_path = os.path.join(base_path, 'data', 'regional_covid_data.csv')
    
    if not os.path.exists(daily_path) or not os.path.exists(region_path):
        return None, None
    
    df_d = pd.read_csv(daily_path)
    df_d['date'] = pd.to_datetime(df_d['date'])
    df_r = pd.read_csv(region_path)
    df_r['date'] = pd.to_datetime(df_r['date'])
    return df_d, df_r

df_daily, df_region = load_data()

if df_daily is None:
    st.error("🚨 데이터가 없습니다! 'project_reset.py'를 먼저 실행해주세요.")
    st.stop()

# 3. 사이드바
with st.sidebar:
    st.header("🎛️ 분석 옵션")
    min_date, max_date = df_daily['date'].min(), df_daily['date'].max()
    start_date, end_date = st.date_input("분석 기간 선택", [min_date, max_date], min_value=min_date, max_value=max_date)
    st.divider()
    all_regions = [c for c in df_region.columns if c != 'date']
    selected_regions = st.multiselect("비교할 지역 (B팀)", all_regions, default=all_regions)

mask_d = (df_daily['date'] >= pd.to_datetime(start_date)) & (df_daily['date'] <= pd.to_datetime(end_date))
filtered_daily = df_daily.loc[mask_d]
mask_r = (df_region['date'] >= pd.to_datetime(start_date)) & (df_region['date'] <= pd.to_datetime(end_date))
filtered_region = df_region.loc[mask_r]

# 메인 화면
st.title("🦠 대한민국 코로나19 데이터 분석 대시보드")
st.markdown(f"📅 **분석 기간:** {start_date} ~ {end_date}")

col1, col2, col3 = st.columns(3)
col1.metric("신규 확진", f"{int(filtered_daily['new_cases'].sum()):,}명")
col2.metric("신규 사망", f"{int(filtered_daily['new_deaths'].sum()):,}명")
last_vac = filtered_daily['accumulated_vaccine_count'].iloc[-1] if 'accumulated_vaccine_count' in filtered_daily else 0
col3.metric("누적 백신 접종", f"{int(last_vac):,}건")

st.divider()

tab1, tab2, tab3 = st.tabs(["📈 A팀: 종합 추이", "🗺️ B팀: 지역별 변화", "💉 C팀: 백신 효과"])

# A팀
with tab1:
    st.subheader("📊 신규 및 누적 발생 현황")
    fig_a = make_subplots(rows=2, cols=1, shared_xaxes=True, specs=[[{"secondary_y": True}], [{"secondary_y": False}]], subplot_titles=("일별 신규", "누적 추이"))
    fig_a.add_trace(go.Scatter(x=filtered_daily['date'], y=filtered_daily['new_cases'], name="신규 확진", line=dict(color='#1E88E5')), row=1, col=1, secondary_y=False)
    fig_a.add_trace(go.Scatter(x=filtered_daily['date'], y=filtered_daily['new_deaths'], name="신규 사망", line=dict(color='#E53935')), row=1, col=1, secondary_y=True)
    fig_a.add_trace(go.Scatter(x=filtered_daily['date'], y=filtered_daily['cum_cases'], name="누적 확진", line=dict(color='#90CAF9', dash='dot')), row=2, col=1)
    fig_a.add_trace(go.Scatter(x=filtered_daily['date'], y=filtered_daily['cum_deaths'], name="누적 사망", line=dict(color='#EF9A9A', dash='dot')), row=2, col=1)
    fig_a.update_layout(height=700, template='plotly_white')
    st.plotly_chart(fig_a, use_container_width=True)

# B팀 (Racing Bar Fix)
with tab2:
    st.subheader("🗺️ 지역별 확진자 순위 변화 (Racing Bar)")
    if selected_regions:
        cols = ['date'] + [r for r in selected_regions if r in filtered_region.columns]
        df_melt = filtered_region[cols].melt(id_vars='date', var_name='Region', value_name='Confirmed')
        df_melt = df_melt[df_melt['Confirmed'] > 0]
        if not df_melt.empty:
            df_melt['date_str'] = df_melt['date'].dt.strftime('%Y-%m-%d')
            df_melt = df_melt.sort_values('date')
            fig_b = px.bar(df_melt, x='Confirmed', y='Region', color='Region', orientation='h', 
                           animation_frame='date_str', range_x=[0, df_melt['Confirmed'].max()*1.1])
            fig_b.update_layout(height=600, showlegend=False)
            st.plotly_chart(fig_b, use_container_width=True)
    else:
        st.warning("지역을 선택해주세요.")

# C팀
with tab3:
    st.subheader("💉 백신 접종과 사망률")
    fig_c = go.Figure()
    fig_c.add_trace(go.Bar(x=filtered_daily['date'], y=filtered_daily['new_deaths'], name='사망자', marker_color='#FF7043', opacity=0.4))
    fig_c.add_trace(go.Scatter(x=filtered_daily['date'], y=filtered_daily['accumulated_vaccine_count'], name='백신 접종', line=dict(color='#FB8C00', width=4), yaxis='y2'))
    fig_c.update_layout(title='접종 증가와 사망자 감소 패턴', yaxis2=dict(overlaying='y', side='right', showgrid=False), template='plotly_white')
    st.plotly_chart(fig_c, use_container_width=True)