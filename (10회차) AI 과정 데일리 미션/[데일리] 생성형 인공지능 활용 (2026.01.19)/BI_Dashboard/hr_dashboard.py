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


def calculate_overtime_impact(df):
    """야근(OverTime)별 퇴사율 요약 (대시보드용)"""
    if df.empty:
        return pd.DataFrame(columns=["OverTime", "Employees", "Leavers", "AttritionRate"])
    tmp = (
        df.groupby("OverTime", dropna=False)
        .agg(
            Employees=("Attrition", "size"),
            Leavers=("Attrition", lambda x: int((x == "Yes").sum())),
        )
        .reset_index()
    )
    tmp["AttritionRate"] = (tmp["Leavers"] / tmp["Employees"]) * 100
    return tmp


def calculate_income_gap(df):
    """퇴사 여부별 월소득 차이(평균/중앙값)"""
    if df.empty:
        return None
    g = df.groupby("Attrition")["MonthlyIncome"].agg(["count", "mean", "median"]).reset_index()
    g.columns = ["Attrition", "n", "mean", "median"]
    if set(g["Attrition"]) >= {"Yes", "No"}:
        yes_mean = float(g.loc[g["Attrition"] == "Yes", "mean"].iloc[0])
        no_mean = float(g.loc[g["Attrition"] == "No", "mean"].iloc[0])
        diff = yes_mean - no_mean
        diff_pct = (diff / no_mean) * 100 if no_mean else 0.0
        return g, diff, diff_pct
    return g, None, None

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

tab1, tab2 = st.tabs(["📊 지표/차트", "🧠 인사이트(경영진용)"])

with tab1:
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

with tab2:
    st.subheader("핵심 인사이트 요약")
    st.markdown(
        "- **야근(OverTime)은 퇴사 위험을 크게 증폭**시키는 신호입니다.\n"
        "- **영업 부서가 최고 위험 부서**로 확인됩니다.\n"
        "- **주니어(입사 1~3년차) + 만족도 낮음(1~2점)** 세그먼트에서 퇴사율이 크게 상승합니다.\n"
        "- 퇴사자는 재직자 대비 **월소득 수준이 유의미하게 낮은 편**으로 나타납니다."
    )

    st.markdown("---")

    st.subheader("1) 야근 영향(요약)")
    ot = calculate_overtime_impact(filtered_hr_df)
    st.dataframe(ot.style.format({"AttritionRate": "{:.2f}"}), use_container_width=True)
    if set(ot["OverTime"].astype(str)) >= {"Yes", "No"}:
        try:
            yes_rate = float(ot.loc[ot["OverTime"] == "Yes", "AttritionRate"].iloc[0])
            no_rate = float(ot.loc[ot["OverTime"] == "No", "AttritionRate"].iloc[0])
            if no_rate > 0:
                st.caption(f"야근자 퇴사율은 비야근 대비 약 **{yes_rate / no_rate:.2f}배** 수준입니다(단순비교).")
        except Exception:
            pass

    st.subheader("2) 급여 격차(요약)")
    income = calculate_income_gap(filtered_hr_df)
    if income is not None:
        income_table, diff, diff_pct = income
        st.dataframe(income_table.style.format({"mean": "{:,.0f}", "median": "{:,.0f}"}), use_container_width=True)
        if diff is not None:
            st.caption(f"퇴사자 평균 월소득은 재직자 대비 **{diff:,.0f}** 낮고(약 **{diff_pct:.2f}%**), 급여 요인이 이탈의 촉매로 작동할 가능성이 있습니다.")

    st.subheader("3) 실행 제안(Top 3)")
    st.markdown(
        "1. **영업 Retention 패키지(4~8주)**: 목표/코칭 표준화 + 보상 구조 점검(저소득/야근자 우선)\n"
        "2. **야근 감축(8~12주)**: 업무량 재설계, 반복업무 자동화, OverTime 경보 지표 운영\n"
        "3. **주니어 조기경보(12주+)**: 만족도 1~2점 즉시 개입(멘토링/업무조정/성장플랜)"
    )
