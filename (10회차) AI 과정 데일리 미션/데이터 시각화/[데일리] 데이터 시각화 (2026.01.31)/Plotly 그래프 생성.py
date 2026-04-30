# Plotly에서 그래프를 그리는 과정은 포토샵에서 레이어를 쌓는 것과 비슷합니다.
# 기본 도화지(Figure)를 만듭니다.
# 그 위에 데이터 레이어(Trace)를 하나씩 추가합니다.

# 시나리오1 - 빈 도화지부터 시작해서 하나씩 쌓아 올리기 (가장 정석적인 방법)
# 이 방법은 plotly.graph_objects를 사용하여 빈 Figure를 만들고, 
# 그 위에 add_trace() 메서드로 데이터를 추가하는 방식입니다. 구조를 이해하기 가장 좋습니다.
import plotly.graph_objects as go

# 1. 빈 Figure 생성
fig = go.Figure()

# 데이터 준비
x_values = [1, 2, 3, 4, 5]
y_data1 = [10, 15, 13, 17, 22]
y_data2 = [5, 8, 7, 9, 12]
y_data3 = [20, 18, 25, 23, 30]

# 2. 첫번째 Trace 추가 (산점도)
# go.Scatter를 사용하여 점을 찍는다.
fig.add_trace(
    go.Scatter(
        x=x_values,
        y=y_data1,
        mode='markers', # 점 모드
        name='데이터 1 (점)',  # 범례 이름
        marker=dict(color='Blue', size=12)
    )
)

# 3. 두번째 Trace 추가 (선 그래프)
# 같은 x축에 위에 다른 y 데이터 선으로 표현
fig.add_trace(
    go.Scatter(
        x=x_values,
        y=y_data2,
        mode='lines+markers', # 선과 점을 같이 표시 모드
        name='데이터 2 (선)',  # 범례 이름
        line=dict(color='Red', width=3)
    )
)

# 4. 세번째 Trace 추가 (막대 그래프)
# 산점도와 선 그래프 위에 막대 그래프 추가
fig.add_trace(
    go.Bar(
        x=x_values,
        y=y_data3,
        name='데이터 3 (막대)',  # 범례 이름
        marker_color='lightgreen',
        opacity=0.5 # 투명도 주어 뒤에 있는 점들이 보이게 함
    )
)

# 레이아웃 다듬기
fig.update_layout(
    title="Plotly Trace 추가 실습: 점, 선, 막대 혼합")

# 5. 그래프 출력
fig.show() 
# 하나의 그래프 안에 파란색 점, 빨간색 선, 연두색 막대가 모두 겹쳐서 표현됩니다. 범례(Legend)를 클릭하면 각 Trace를 끄거나 켤 수 있습니다.
# ============================================================================================================================

# 시나리오2 - plotly.express로 기본 그래프를 만들고, 그 위에 추가하기 
# 이 방법은 plotly.express로 기본 그래프를 만든 후,
# update_traces() 메서드로 스타일을 변경하거나, add_trace()로 새로운 데이터를 추가하는 방식입니다.
import plotly.express as px
import plotly.graph_objects as go # Trace를 추가하려면 go가 필요합니다.
import pandas as pd

# 1. 샘플 데이터 생성
df = pd.DataFrame({
    '날짜' : pd.date_range(start='2023-01-01', periods=10),
    '매출' : [100, 120, 90, 150, 270, 80, 200, 210, 130, 160]
})
sum_data = df['매출'].mean()

# 2. plotly Express로 기본 그래프 생성 (바 차트)
fig = px.bar(df, x='날짜', y='매출', title="일별 매출과 평균선")

# --- 여기까지가 기본 그패프입니다. ---

# 3. Trace 추가 - 평균선 추가 (가로선)
fig.add_trace(
    go.Scatter(
        x=df['날짜'],          # x축은 동일하게
        y=[sum_data]*len(df), # Y축은 평균값으로 채운 리스트 [141, 141, ...]
        mode='lines',         # 선 모드
        name='평균 매출선',      # 범례 이름
        line=dict(color='red', width=2, dash='dash') # 빨간색 점선
    )
)

# 4. 그래프 출력
fig.show()
# 핵심 요약
# fig.add_trace(...)는 기존 그래프 위에 새로운 데이터 층을 올리는 명령어입니다.
# add_trace 안에는 go.Scatter, go.Bar, go.Box 등 구체적인 그래프 객체(plotly.graph_objects)가 들어가야 합니다.
# plotly.express로 쉽고 빠르게 베이스를 만들고, 디테일한 추가 요소는 go와 add_trace로 보강하는 방식이 매우 효율적입니다.
