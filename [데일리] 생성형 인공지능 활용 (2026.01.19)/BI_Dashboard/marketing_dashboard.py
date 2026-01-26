import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# 페이지 설정
st.set_page_config(
    page_title="마케팅 분석 대시보드",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 데이터 로드 함수
@st.cache_data
def load_marketing_data():
    """마케팅 데이터 로드 및 전처리"""
    file_path = Path(__file__).parent / "data" / "marketing_campaign_dataset.csv"
    df = pd.read_csv(file_path)
    
    # Acquisition_Cost 문자열을 숫자로 변환
    df['Acquisition_Cost'] = df['Acquisition_Cost'].str.replace('$', '').str.replace(',', '').astype(float)
    
    # Date 컬럼을 datetime으로 변환
    df['Date'] = pd.to_datetime(df['Date'])
    
    # 채널 한글 매핑
    channel_mapping = {
        'Google Ads': '구글 광고',
        'YouTube': '유튜브',
        'Instagram': '인스타그램',
        'Website': '웹사이트',
        'Facebook': '페이스북',
        'Twitter': '트위터',
        'LinkedIn': '링크드인'
    }
    df['Channel_Used'] = df['Channel_Used'].map(channel_mapping).fillna(df['Channel_Used'])
    
    # 캠페인 유형 한글 매핑
    campaign_type_mapping = {
        'Email': '이메일',
        'Influencer': '인플루언서',
        'Display': '디스플레이',
        'Search': '검색',
        'Social Media': '소셜 미디어'
    }
    df['Campaign_Type'] = df['Campaign_Type'].map(campaign_type_mapping).fillna(df['Campaign_Type'])
    
    # 고객 세그먼트 한글 매핑
    segment_mapping = {
        'Health & Wellness': '건강 및 웰니스',
        'Fashionistas': '패셔니스타',
        'Outdoor Adventurers': '아웃도어 모험가',
        'Foodies': '푸디',
        'Tech Enthusiasts': '기술 애호가'
    }
    df['Customer_Segment'] = df['Customer_Segment'].map(segment_mapping).fillna(df['Customer_Segment'])
    
    # 회사명 한글 매핑
    company_mapping = {
        'Innovate Industries': '혁신 산업',
        'NexGen Systems': '넥스젠 시스템',
        'Alpha Innovations': '알파 이노베이션',
        'DataTech Solutions': '데이터테크 솔루션',
        'TechCorp': '테크코프'
    }
    df['Company'] = df['Company'].map(company_mapping).fillna(df['Company'])
    
    return df

# 계산 함수
def calculate_avg_roi(df):
    """평균 ROI 계산"""
    if df.empty:
        return 0.0
    return df['ROI'].mean()


def summarize_channel_roi(df):
    """Channel별 평균 ROI / CVR / CPA 요약"""
    if df.empty:
        return None
    summary = (
        df.groupby('Channel_Used', dropna=False)
        .agg(
            Campaigns=('Campaign_ID', 'count'),
            Avg_ROI=('ROI', 'mean'),
            Avg_Conversion_Rate=('Conversion_Rate', 'mean'),
            Avg_Acquisition_Cost=('Acquisition_Cost', 'mean'),
        )
        .reset_index()
        .sort_values(['Avg_ROI', 'Campaigns'], ascending=[False, False])
    )
    return summary


def summarize_target_cvr(df):
    """Target Audience별 평균 전환율 / ROI / CPA"""
    if df.empty:
        return None
    summary = (
        df.groupby('Target_Audience', dropna=False)
        .agg(
            Campaigns=('Campaign_ID', 'count'),
            Avg_Conversion_Rate=('Conversion_Rate', 'mean'),
            Avg_ROI=('ROI', 'mean'),
            Avg_Acquisition_Cost=('Acquisition_Cost', 'mean'),
        )
        .reset_index()
        .sort_values(['Avg_Conversion_Rate', 'Campaigns'], ascending=[False, False])
    )
    return summary


def summarize_cpa_by_campaign_type(df):
    """Campaign Type별 평균/중앙 Acquisition_Cost"""
    if df.empty:
        return None
    summary = (
        df.groupby('Campaign_Type', dropna=False)
        .agg(
            Campaigns=('Campaign_ID', 'count'),
            Avg_Acquisition_Cost=('Acquisition_Cost', 'mean'),
            Median_Acquisition_Cost=('Acquisition_Cost', 'median'),
            Avg_ROI=('ROI', 'mean'),
        )
        .reset_index()
        .sort_values(['Avg_Acquisition_Cost', 'Campaigns'], ascending=[True, False])
    )
    return summary


def summarize_high_performance(df, roi_threshold: float = 7.0):
    """ROI가 threshold 이상인 고성과 캠페인 특징"""
    if df.empty:
        return None
    hi = df[df['ROI'] >= roi_threshold].copy()
    if hi.empty:
        return {
            'n_high': 0,
            'share_pct': 0.0,
            'avg_roi': 0.0,
            'top_channel': None,
            'top_language': None,
        }
    n_high = len(hi)
    share_pct = n_high / len(df) * 100
    avg_roi = hi['ROI'].mean()
    top_channel = hi['Channel_Used'].value_counts().idxmax()
    top_language = hi['Language'].value_counts().idxmax()
    return {
        'n_high': int(n_high),
        'share_pct': float(share_pct),
        'avg_roi': float(avg_roi),
        'top_channel': top_channel,
        'top_language': top_language,
    }

# 데이터 로드
marketing_df = load_marketing_data()

# 사이드바
with st.sidebar:
    st.title("📈 마케팅 분석 대시보드")
    st.markdown("**마케팅 현황 모니터링**")
    st.markdown("---")
    
    # 필터 섹션
    st.subheader("필터")
    
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
        max_value=max_date,
        format="YYYY-MM-DD"
    )
    
    # 날짜 정보 표시
    if isinstance(date_range, tuple) and len(date_range) == 2:
        st.caption(f"선택된 기간: {date_range[0].strftime('%Y년 %m월 %d일')} ~ {date_range[1].strftime('%Y년 %m월 %d일')}")
    elif date_range:
        st.caption(f"선택된 날짜: {date_range.strftime('%Y년 %m월 %d일')}")
    
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
st.header("📈 마케팅 분석 대시보드")

tab1, tab2 = st.tabs(["📊 지표/차트", "🧠 인사이트(마케팅 전략)"])

with tab1:
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

    # 채널별 평균 전환율
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

    # 데이터 샘플링 (너무 많은 데이터가 있으면 시각화가 어려움)
    if len(filtered_marketing_df) > 1000:
        sample_df = filtered_marketing_df.sample(n=1000, random_state=42)
        st.caption(f"※ 데이터가 많아 표본 {len(sample_df):,}개를 무작위로 표시합니다. (전체: {len(filtered_marketing_df):,}개)")
    else:
        sample_df = filtered_marketing_df

    # Conversion_Rate를 퍼센트로 변환하여 크기 조정
    sample_df = sample_df.copy()
    sample_df['Conversion_Rate_Percent'] = sample_df['Conversion_Rate'] * 100

    fig_scatter = px.scatter(
        sample_df,
        x='Acquisition_Cost',
        y='ROI',
        color='Channel_Used',
        size='Conversion_Rate_Percent',
        hover_data=['Company', 'Campaign_Type', 'Conversion_Rate'],
        title="획득 비용 대 ROI (채널별)",
        labels={
            'Acquisition_Cost': '획득 비용 ($)',
            'ROI': 'ROI',
            'Channel_Used': '채널',
            'Conversion_Rate_Percent': '전환율 (%)'
        },
        color_discrete_sequence=px.colors.qualitative.Set3,
        size_max=30
    )
    fig_scatter.update_layout(
        height=500,
        xaxis_title="획득 비용 ($)",
        yaxis_title="ROI",
        title_font_size=16,
        legend=dict(
            title="채널",
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02
        ),
        hovermode='closest'
    )
    fig_scatter.update_traces(
        marker=dict(
            line=dict(width=0.5, color='DarkSlateGrey'),
            opacity=0.7
        )
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with tab2:
    st.subheader("1) 채널별 ROI 인사이트")
    channel_roi_df = summarize_channel_roi(filtered_marketing_df)
    if channel_roi_df is not None and not channel_roi_df.empty:
        st.dataframe(
            channel_roi_df.style.format(
                {
                    "Avg_ROI": "{:.2f}",
                    "Avg_Conversion_Rate": "{:.4f}",
                    "Avg_Acquisition_Cost": "${:,.0f}",
                }
            ),
            use_container_width=True,
        )

        fig_channel_roi = px.bar(
            channel_roi_df,
            x="Channel_Used",
            y="Avg_ROI",
            title="채널별 평균 ROI (내림차순)",
            labels={"Channel_Used": "채널", "Avg_ROI": "평균 ROI"},
            color="Avg_ROI",
            color_continuous_scale="Greens",
        )
        fig_channel_roi.update_layout(
            height=400,
            showlegend=False,
            xaxis_title="채널",
            yaxis_title="평균 ROI",
            title_font_size=16,
        )
        st.plotly_chart(fig_channel_roi, use_container_width=True)

    st.markdown("---")

    st.subheader("2) 타겟별 전환율(CVR) 인사이트")
    target_cvr_df = summarize_target_cvr(filtered_marketing_df)
    if target_cvr_df is not None and not target_cvr_df.empty:
        st.dataframe(
            target_cvr_df.style.format(
                {
                    "Avg_Conversion_Rate": "{:.4f}",
                    "Avg_ROI": "{:.2f}",
                    "Avg_Acquisition_Cost": "${:,.0f}",
                }
            ),
            use_container_width=True,
        )
        best_target = target_cvr_df.iloc[0]["Target_Audience"]
        st.caption(f"현재 데이터 기준 **최고 반응 타겟(Target Audience)** 은 **{best_target}** 입니다.")

    st.markdown("---")

    st.subheader("3) 최고 전환 타겟의 Channel × Language")
    if target_cvr_df is not None and not target_cvr_df.empty:
        best_target = target_cvr_df.iloc[0]["Target_Audience"]
        cross_df = (
            filtered_marketing_df[filtered_marketing_df["Target_Audience"] == best_target]
            .groupby(["Channel_Used", "Language"], dropna=False)
            .agg(
                Campaigns=("Campaign_ID", "count"),
                Avg_Conversion_Rate=("Conversion_Rate", "mean"),
                Avg_ROI=("ROI", "mean"),
            )
            .reset_index()
            .sort_values(["Avg_Conversion_Rate", "Campaigns"], ascending=[False, False])
        )
        st.dataframe(
            cross_df.style.format(
                {"Avg_Conversion_Rate": "{:.4f}", "Avg_ROI": "{:.2f}"}
            ),
            use_container_width=True,
        )

    st.markdown("---")

    st.subheader("4) Campaign Type별 CPA(획득 비용)")
    cpa_df = summarize_cpa_by_campaign_type(filtered_marketing_df)
    if cpa_df is not None and not cpa_df.empty:
        st.dataframe(
            cpa_df.style.format(
                {
                    "Avg_Acquisition_Cost": "${:,.0f}",
                    "Median_Acquisition_Cost": "${:,.0f}",
                    "Avg_ROI": "{:.2f}",
                }
            ),
            use_container_width=True,
        )
        fig_cpa = px.bar(
            cpa_df,
            x="Campaign_Type",
            y="Avg_Acquisition_Cost",
            title="캠페인 유형별 평균 획득 비용(CPA)",
            labels={"Campaign_Type": "캠페인 유형", "Avg_Acquisition_Cost": "평균 획득 비용 ($)"},
            color="Avg_Acquisition_Cost",
            color_continuous_scale="Reds",
        )
        fig_cpa.update_layout(
            height=400,
            showlegend=False,
            xaxis_title="캠페인 유형",
            yaxis_title="평균 획득 비용 ($)",
            title_font_size=16,
        )
        st.plotly_chart(fig_cpa, use_container_width=True)

    st.markdown("---")

    st.subheader("5) 고성과 캠페인(ROI ≥ 7) 특징")
    hi_summary = summarize_high_performance(filtered_marketing_df)
    if hi_summary is not None and hi_summary["n_high"] > 0:
        st.markdown(
            f"- ROI ≥ 7 캠페인 수: **{hi_summary['n_high']:,}개** "
            f"(전체의 약 **{hi_summary['share_pct']:.2f}%**)\n"
            f"- 이들의 평균 ROI는 **{hi_summary['avg_roi']:.2f}** 수준입니다.\n"
            f"- 고성과 캠페인은 주로 **{hi_summary['top_channel']}** 채널과 "
            f"**{hi_summary['top_language']}** 언어 조합에서 많이 나타납니다."
        )
    else:
        st.caption("현재 필터 조건에서는 ROI ≥ 7인 고성과 캠페인이 없습니다.")
