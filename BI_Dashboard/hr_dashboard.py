import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# 페이지 설정
st.set_page_config(
    page_title="HR 분석 대시보드",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 데이터 로드 함수
@st.cache_data
def load_hr_data():
    """HR 데이터 로드 및 전처리"""
    file_path = Path(__file__).parent / "data" / "WA_Fn-UseC_-HR-Employee-Attrition.csv"
    df = pd.read_csv(file_path)
    
    # 부서 한글 매핑
    dept_mapping = {
        'Sales': '영업',
        'Research & Development': '연구개발',
        'Human Resources': '인사'
    }
    df['Department'] = df['Department'].map(dept_mapping).fillna(df['Department'])
    
    # 성별 한글 매핑
    gender_mapping = {
        'Female': '여성',
        'Male': '남성'
    }
    df['Gender'] = df['Gender'].map(gender_mapping).fillna(df['Gender'])
    
    return df

# 계산 함수
def calculate_attrition_rate(df):
    """퇴사율 계산"""
    if df.empty:
        return 0.0
    total = len(df)
    attrition_count = len(df[df['Attrition'] == 'Yes'])
    return (attrition_count / total) * 100

# 데이터 로드
hr_df = load_hr_data()

# 사이드바
with st.sidebar:
    st.title("👥 HR 분석 대시보드")
    st.markdown("**사내 인사 현황 모니터링**")
    st.markdown("---")
    
    # 필터 섹션
    st.subheader("필터")
    
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

# 메인 콘텐츠
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
