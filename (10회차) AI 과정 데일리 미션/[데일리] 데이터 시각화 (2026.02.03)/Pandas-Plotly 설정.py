import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# 1. Pandas 시각화 백엔드를 Plotly로 설정 (이후 df.plot 사용 가능)
pd.options.plotting.backend = "plotly"
# 샘플 데이터 생성
np.random.seed(42)
df = pd.DataFrame({
    "날짜": pd.date_range(start="2026-01-01", periods=100),
    "기온": np.random.normal(20, 5, 100).cumsum(),
    "습도": np.random.normal(50, 10, 100).cumsum(),
    "도시": np.random.choice(["서울", "부산"], 100)
})

# 2. Pandas 백엔드 방식을 사용하여 그래프 생성
# 이 방식은 Plotly Express의 파라미터를 그대로 사용할 수 있습니다.
fig = df.plot(
    kind="line", 
    x="날짜", 
    y=["기온", "습도"],
    title="[데일리] 데이터 시각화 (2026.02.03)",
    labels={"value": "수치", "variable": "항목"}
)

# 3. 템플릿(Template) 설정
# 'plotly', 'plotly_white', 'plotly_dark', 'ggplot2', 'seaborn', 'none' 중 선택 가능
fig.update_layout(template="plotly_white")

# 4. 범례 상세 설정 
fig.update_layout(
    showlegend=True,
    legend=dict(
        orientation="h",        # 범례 방향: 가로(h), 세로(v)
        yanchor="bottom",       # y축 기준점: 하단
        y=1.02,                 # 그래프 위로 배치 (1.0이 그래프 끝)
        xanchor="right",        # x축 기준점: 오른쪽
        x=1,                    # 오른쪽 끝에 배치
        bgcolor="rgba(255, 255, 255, 0.5)", # 범례 배경색 (투명도 포함)
        bordercolor="Black",    # 범례 테두리 색상
        borderwidth=1,          # 범례 테두리 두께
        font=dict(
            family="Malgun Gothic", # 폰트 설정
            size=12,
            color="black"
        ),
        title_text="데이터 종류"  # 범례 제목
    )
)

# 5. 축 및 그리드 추가 설정 (보너스)
fig.update_xaxes(showgrid=True, gridcolor='lightgray')
fig.update_yaxes(showgrid=True, gridcolor='lightgray')

# 그래프 출력
fig.show()