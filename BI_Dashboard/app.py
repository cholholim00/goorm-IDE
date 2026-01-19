import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from pathlib import Path

# 페이지 설정
st.set_page_config(
    page_title="BI 대시보드",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 데이터 로드 함수
@st.cache_data
def load_hr_data():
    """HR 데이터 로드 및 전처리"""
    file_path = Path(__file__).parent / "data" / "WA_Fn-UseC_-HR-Employee-Attrition.csv"
    df = pd.read_csv(file_path)
    return df

@st.cache_data
def load_marketing_data():
    """마케팅 데이터 로드 및 전처리"""
    file_path = Path(__file__).parent / "data" / "marketing_campaign_dataset.csv"
    df = pd.read_csv(file_path)
    
    # Acquisition_Cost 문자열을 숫자로 변환
    df['Acquisition_Cost'] = df['Acquisition_Cost'].str.replace('$', '').str.replace(',', '').astype(float)
    
    # Date 컬럼을 datetime으로 변환
    df['Date'] = pd.to_datetime(df['Date'])
    
    return df

# 계산 함수
def calculate_attrition_rate(df):
    """퇴사율 계산"""
    if df.empty:
        return 0.0
    total = len(df)
    attrition_count = len(df[df['Attrition'] == 'Yes'])
    return (attrition_count / total) * 100

def calculate_avg_roi(df):
    """평균 ROI 계산"""
    if df.empty:
        return 0.0
    return df['ROI'].mean()

# 데이터 로드
hr_df = load_hr_data()
marketing_df = load_marketing_data()

# 사이드바
with st.sidebar:
    st.title("📊 BI 대시보드")
    st.markdown("**사내 인사 및 마케팅 현황 통합 모니터링**")
    st.markdown("---")
    
    # 탭 선택
    selected_tab = st.radio(
        "대시보드 선택",
        ["HR 분석", "마케팅 분석"],
        index=0
    )
    
    st.markdown("---")
    
    # 필터 섹션
    st.subheader("필터")
    
    if selected_tab == "HR 분석":
        # HR 필터
        departments = ['전체'] + sorted(hr_df['Department'].unique().tolist())
        selected_dept = st.selectbox("부서", departments)
        
        genders = ['전체'] + sorted(hr_df['Gender'].unique().tolist())
        selected_gender = st.selectbox("성별", genders)
        
        # 필터 적용
        filtered_hr_df = hr_df.copy()
        if selected_dept != '전체':
            filtered_hr_df = filtered_hr_df[filtered_hr_df['Department'] == selected_dept]
        if selected_gender != '전체':
            filtered_hr_df = filtered_hr_df[filtered_hr_df['Gender'] == selected_gender]
    
    else:  # 마케팅 분석
        # 마케팅 필터
        companies = ['전체'] + sorted(marketing_df['Company'].unique().tolist())
        selected_company = st.selectbox("회사", companies)
        
        # 날짜 범위 필터
        min_date = marketing_df['Date'].min().date()
        max_date = marketing_df['Date'].max().date()
        date_range = st.date_input(
            "날짜 범위",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        # 필터 적용
        filtered_marketing_df = marketing_df.copy()
        if selected_company != '전체':
            filtered_marketing_df = filtered_marketing_df[filtered_marketing_df['Company'] == selected_company]
        if isinstance(date_range, tuple) and len(date_range) == 2:
            filtered_marketing_df = filtered_marketing_df[
                (filtered_marketing_df['Date'].dt.date >= date_range[0]) &
                (filtered_marketing_df['Date'].dt.date <= date_range[1])
            ]

# 메인 콘텐츠
if selected_tab == "HR 분석":
    st.header("👥 HR 분석 대시보드")
    
    # 퇴사율 KPI
    attrition_rate = calculate_attrition_rate(filtered_hr_df)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("전체 퇴사율", f"{attrition_rate:.2f}%")
    with col2:
        total_employees = len(filtered_hr_df)
        st.metric("총 직원 수", f"{total_employees:,}명")
    with col3:
        attrition_count = len(filtered_hr_df[filtered_hr_df['Attrition'] == 'Yes'])
        st.metric("퇴사자 수", f"{attrition_count:,}명")
    
    st.markdown("---")
    
    # 부서별 퇴사율 Bar 차트
    st.subheader("부서별 퇴사율")
    dept_attrition = filtered_hr_df.groupby('Department')['Attrition'].apply(
        lambda x: (x == 'Yes').sum() / len(x) * 100
    ).reset_index()
    dept_attrition.columns = ['Department', 'Attrition_Rate']
    dept_attrition = dept_attrition.sort_values('Attrition_Rate', ascending=False)
    
    fig_bar = px.bar(
        dept_attrition,
        x='Department',
        y='Attrition_Rate',
        title="부서별 퇴사율",
        labels={'Attrition_Rate': '퇴사율 (%)', 'Department': '부서'},
        color='Attrition_Rate',
        color_continuous_scale='Reds'
    )
    fig_bar.update_layout(
        height=400, 
        showlegend=False,
        xaxis_title="부서",
        yaxis_title="퇴사율 (%)",
        title_font_size=16
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    
    st.markdown("---")
    
    # 소득 관계 Box 차트
    st.subheader("퇴사 여부별 월 소득 분포")
    fig_box = px.box(
        filtered_hr_df,
        x='Attrition',
        y='MonthlyIncome',
        title="퇴사 여부별 월 소득 분포",
        labels={'MonthlyIncome': '월 소득 ($)', 'Attrition': '퇴사 여부'},
        color='Attrition',
        color_discrete_map={'Yes': '#ff4444', 'No': '#4444ff'}
    )
    fig_box.update_layout(
        height=400,
        xaxis_title="퇴사 여부",
        yaxis_title="월 소득 ($)",
        title_font_size=16
    )
    st.plotly_chart(fig_box, use_container_width=True)

else:  # 마케팅 분석
    st.header("📈 마케팅 분석 대시보드")
    
    # ROI KPI
    avg_roi = calculate_avg_roi(filtered_marketing_df)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("평균 ROI", f"{avg_roi:.2f}")
    with col2:
        total_campaigns = len(filtered_marketing_df)
        st.metric("총 캠페인 수", f"{total_campaigns:,}개")
    with col3:
        total_cost = filtered_marketing_df['Acquisition_Cost'].sum()
        st.metric("총 획득 비용", f"${total_cost:,.0f}")
    
    st.markdown("---")
    
    # 채널별 전환율 차트
    st.subheader("채널별 평균 전환율")
    channel_conversion = filtered_marketing_df.groupby('Channel_Used')['Conversion_Rate'].mean().reset_index()
    channel_conversion.columns = ['Channel_Used', 'Avg_Conversion_Rate']
    channel_conversion = channel_conversion.sort_values('Avg_Conversion_Rate', ascending=False)
    
    fig_channel = px.bar(
        channel_conversion,
        x='Channel_Used',
        y='Avg_Conversion_Rate',
        title="채널별 평균 전환율",
        labels={'Avg_Conversion_Rate': '평균 전환율', 'Channel_Used': '채널'},
        color='Avg_Conversion_Rate',
        color_continuous_scale='Blues'
    )
    fig_channel.update_layout(
        height=400, 
        showlegend=False,
        xaxis_title="채널",
        yaxis_title="평균 전환율",
        title_font_size=16
    )
    st.plotly_chart(fig_channel, use_container_width=True)
    
    st.markdown("---")
    
    # 예산 효율성 Scatter 차트
    st.subheader("예산 효율성 분석")
    fig_scatter = px.scatter(
        filtered_marketing_df,
        x='Acquisition_Cost',
        y='ROI',
        color='Channel_Used',
        size='Conversion_Rate',
        hover_data=['Company', 'Campaign_Type'],
        title="획득 비용 대 ROI (채널별)",
        labels={'Acquisition_Cost': '획득 비용 ($)', 'ROI': 'ROI'},
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_scatter.update_layout(
        height=500,
        xaxis_title="획득 비용 ($)",
        yaxis_title="ROI",
        title_font_size=16
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
